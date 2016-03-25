######################## BEGIN LICENSE BLOCK ########################
# The Original Code is Mozilla Universal charset detector code.
#
# The Initial Developer of the Original Code is
# Netscape Communications Corporation.
# Portions created by the Initial Developer are Copyright (C) 2001
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Mark Pilgrim - port to Python
#   Shy Shalom - original C code
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301  USA
######################### END LICENSE BLOCK #########################

import constants
import sys
# multi-byte character sets
from pyicqt.chardet_utf.mbcsgroupprober import MBCSGroupProber
import re

MINIMUM_THRESHOLD = 0.20
ePureAscii = 0
eEscAscii = 1
eHighbyte = 2


class UniversalDetector:

    def __init__(self):
        self._controlDetector = re.compile(r'[\x00-\x1F]')
        self._highBitDetector = re.compile(r'[\x80-\xFF]')
        self._escDetector = re.compile(r'(\033|~{)')
        self._mCharSetProbers = []
        self.reset()

    def reset(self):
        self.result = {'encoding': None, 'confidence': 0.0}
        self.done = constants.False
        self._mStart = constants.True
        self._mGotData = constants.False
        self._mInputState = ePureAscii
        self._mLastChar = ''
        for prober in self._mCharSetProbers:
            prober.reset()

    def feed(self, aBuf):
        if self.done:
            return

        aLen = len(aBuf)
        if not aLen:
            return

        if not self._mGotData:
            # If the data starts with BOM, we know it is UTF
            if aBuf[:3] == '\xEF\xBB\xBF':
                # EF BB BF  UTF-8 with BOM
                self.result = {'encoding': 'utf-8', 'confidence': 1.0}
            elif aBuf[:2] == '\xFF\xFE':
                # FF FE  UTF-16, little endian BOM
                self.result = {'encoding': 'utf-16le', 'confidence': 1.0}
            elif aBuf[:2] == '\xFE\xFF':
                # FE FF  UTF-16, big endian BOM
                self.result = {'encoding': 'utf-16be', 'confidence': 1.0}

        self._mGotData = constants.True
        if self.result['encoding'] and (self.result['confidence'] > 0.0):
            self.done = constants.True
            return

        if self._mInputState == ePureAscii:
            # this way should works in most real cases
            if self._controlDetector.search(aBuf):
                controlCount = 0
                for i in aBuf:
                    if ord(i) in xrange(0x00, 0x1F):
                        controlCount += 1
                coeff = float(controlCount) / float(len(aBuf))
                # if more than 3% of control characters in text then it's
                # utf-16
                if coeff > 0.03:
                    pos = 0
                    odd = 0
                    even = 0
                    while pos + 1 < len(aBuf):
                        if ord(aBuf[pos]) in xrange(0x00, 0x1F):
                            odd += 1
                        if ord(aBuf[pos + 1]) in xrange(0x00, 0x1F):
                            even += 1
                        pos += 2
                    if odd > even:
                        coeff_e = float(even) / float(odd)
                        self.result = {'encoding': 'utf-16be',
                                       'confidence': (coeff * 2 - coeff_e) * 0.8}
                    else:
                        coeff_e = float(odd) / float(even)
                        self.result = {'encoding': 'utf-16le',
                                       'confidence': (coeff * 2 - coeff_e) * 0.8}
                    self.done = constants.True
            if self._highBitDetector.search(aBuf):
                self._mInputState = eHighbyte
            elif (self._mInputState == ePureAscii) and self._escDetector.search(self._mLastChar + aBuf):
                self._mInputState = eEscAscii

        self._mLastChar = aBuf[-1]

        if self._mInputState == eEscAscii:
            self.result = {'encoding': None,
                           'confidence': 0.0}
            self.done = constants.True
        if self._mInputState == eHighbyte:
            if not self._mCharSetProbers:
                self._mCharSetProbers = [MBCSGroupProber()]
            for prober in self._mCharSetProbers:
                if prober.feed(aBuf) == constants.eFoundIt:
                    self.result = {'encoding': prober.get_charset_name(),
                                   'confidence': prober.get_confidence()}
                    self.done = constants.True
                    break

    def close(self):
        if self.done:
            return
        if not self._mGotData:
            if constants._debug:
                sys.stderr.write('no data received!\n')
            return
        self.done = constants.True

        if self._mInputState == ePureAscii:
            self.result = {'encoding': 'ascii', 'confidence': 1.0}
            return self.result

        if self._mInputState == eHighbyte:
            proberConfidence = None
            maxProberConfidence = 0.0
            maxProber = None
            for prober in self._mCharSetProbers:
                if not prober:
                    continue
                proberConfidence = prober.get_confidence()
                if proberConfidence > maxProberConfidence:
                    maxProberConfidence = proberConfidence
                    maxProber = prober
            if maxProber and (maxProberConfidence > MINIMUM_THRESHOLD):
                self.result = {'encoding': maxProber.get_charset_name(),
                               'confidence': maxProber.get_confidence()}
                return self.result

        if constants._debug:
            sys.stderr.write('no probers hit minimum threshhold\n')
            for prober in self._mCharSetProbers[0].mProbers:
                if not prober:
                    continue
                sys.stderr.write('%s confidence = %s\n' %
                                 (prober.get_charset_name(),
                                  prober.get_confidence()))
