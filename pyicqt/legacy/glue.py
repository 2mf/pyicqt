# -*- coding: utf-8 -*-
# Copyright 2004-2006 Daniel Henninger <jadestorm@nc.rr.com>
# Licensed for distribution under the GPL version 2, check COPYING for details

from twisted.words.xish.domish import Element
from twisted.internet import protocol, reactor, defer, task
from pyicqt import imgmanip
from pyicqt import utils
from pyicqt.tlib import oscar, socks5, sockserror
from pyicqt.legacy import icqt
from pyicqt import config
from pyicqt.debug import LogEvent, INFO, WARN, ERROR
from pyicqt import lang
from pyicqt import avatar

import sys
import warnings
import pprint
import os.path
import re
import time
import binascii
import md5
import random

from twisted.python import log

# The name of the transport
name = "ICQ Transport"

# The transport's version
version = "0.8.1.5"

# URL of the transport's web site
url = "http://pyicqt.googlecode.com/"

# This should be set to the identity of the gateway
id = "icq"

if not config.disableAvatars:
    # Load the default AIM and ICQ avatars
    f = open(os.path.join("data", "defaultAIMAvatar.png"))
    defaultAIMAvatarData = f.read()
    f.close()
    defaultAIMAvatar = avatar.AvatarCache().setAvatar(defaultAIMAvatarData)

    f = open(os.path.join("data", "defaultICQAvatar.png"))
    defaultICQAvatarData = f.read()
    f.close()
    defaultICQAvatar = avatar.AvatarCache().setAvatar(defaultICQAvatarData)

    defaultAvatar = defaultAIMAvatar
    defaultAvatarData = defaultAIMAvatarData
else:
    defaultAvatar = None
    defaultAvatarData = None

# This function translates an ICQ screen name to a JID


def icq2jid(icqid):
    if icqid:
        retstr = icqid.lower().replace(' ', '')
        return retstr.replace('@', '%') + "@" + config.jid
    else:
        return config.jid

# This function translates a JID to an ICQ screen name


def jid2icq(jid):
    return unicode(jid[:jid.find('@')].replace('%', '@'))

# This function is called to handle legacy id translation to a JID
translateAccount = icq2jid


############################################################################
# This class handles most interaction with ICQ
############################################################################
class LegacyConnection:
    """ A glue class that connects to the legacy network """

    def __init__(self, username, password, session):
        import buddies

        self.username = username
        self.password = password
        self.session = session
        self.legacyList = buddies.BuddyList(self.session)
        self.savedShow = None
        self.savedFriendly = None
        self.savedURL = None
        self.reactor = reactor
        self.userinfoCollection = {}
        self.userinfoID = 0
        self.deferred = defer.Deferred()
        self.deferred.addErrback(self.errorCallback)
        hostport = (config.icqServer, config.icqPort)
        LogEvent(INFO, self.session.jabberID, "Creating")
        if config.socksProxyServer and config.socksProxyPort:
            self.oa = icqt.OA
            self.creator = socks5.ProxyClientCreator(
                self.reactor, self.oa, self.username, self.password, self, deferred=self.deferred, icq=1)
            LogEvent(INFO, self.session.jabberID, "Connect via socks proxy")
            self.creator.connectSocks5Proxy(
                config.icqServer, config.icqPort, config.socksProxyServer, config.socksProxyPort, "ICQCONN")
        else:
            self.oa = icqt.OA
            self.creator = protocol.ClientCreator(
                self.reactor, self.oa, self.username, self.password, self, deferred=self.deferred, icq=1)
            LogEvent(INFO, self.session.jabberID, "Connect via direct tcp")
            self.creator.connectTCP(*hostport)

        LogEvent(INFO, self.session.jabberID, "Created!")

    def removeMe(self):
        from glue import icq2jid
        LogEvent(INFO, self.session.jabberID)
        try:
            self.bos.stopKeepAlive()
            self.bos.disconnect()
        except AttributeError:
            pass
        self.legacyList.removeMe()
        self.legacyList = None
        self.session = None
        utils.mutilateMe(self)

    def jidRes(self, resource):
        to = self.session.jabberID
        if resource:
            to += "/" + resource
        return to

    def highestResource(self):
        """ Returns highest priority resource """
        return self.session.highestResource()

    def setURL(self, URL=None):
        LogEvent(INFO, self.session.jabberID, "setURL %s" % URL)
        try:
            self.bos.setURL(utils.utf8encode(URL))
        except AttributeError:
            # self.alertUser(lang.get("sessionnotactive", config.jid)
            pass

    def sendMessage(self, target, resource, message, noerror, xhtml, autoResponse=0, jabber_mid=None):
        LogEvent(INFO, self.session.jabberID)
        from glue import jid2icq
        try:
            self.session.pytrans.serviceplugins[
                'Statistics'].stats['OutgoingMessages'] += 1
            self.session.pytrans.serviceplugins['Statistics'].sessionUpdate(
                self.session.jabberID, 'OutgoingMessages', 1)
            uin = jid2icq(target)
            wantIcon = 0
            if self.bos.requesticon.has_key(uin):
                LogEvent(
                    INFO, self.session.jabberID, "Going to ask for target's icon.")
                wantIcon = 1
                del self.bos.requesticon[uin]
            offline = 1
            try:
                if self.legacyList.ssicontacts[uin]['presence'] != "unavailable":
                    offline = 0
            except:
                # well then they're online in some way
                pass

            iconSum = None
            iconLen = None
            iconStamp = None
            if hasattr(self, "myavatar"):
                iconSum = oscar.getIconSum(self.myavatar)
                iconLen = len(self.myavatar)
                iconStamp = time.time()
                LogEvent(INFO, self.session.jabberID, "Going to send info about our icon, length %d, cksum %d" % (
                    iconLen, iconSum))

            LogEvent(INFO, self.session.jabberID)
            if uin[0].isdigit():  # ICQ users
                if jabber_mid and int(self.bos.selfSettings['msgconfirm_recvmode']) == 1 and self.legacyList.hasCapability(uin, 'serv_rel'):
                    cookie = ''.join(
                        [chr(random.randrange(0, 127)) for i in xrange(8)])  # cookie
                    c_time = int(time.time())
                    uvars = {}
                    msg_query = self.getUserVarValue(
                        uin, 'wait_for_confirm_msg_query')
                    if len(msg_query) == 0:
                        msg_query = dict([])
                    elif len(msg_query) > 4:  # query already too long
                        del_msg_query = dict([])
                        for every in msg_query:
                            e_id, e_res, e_time = msg_query[every]
                            # sent more than 60 second ago and receiving not
                            # confirmed
                            if int(c_time) > int(e_time) + 60:
                                # message was lost
                                del_msg_query[every] = msg_query[every]
                        if len(del_msg_query):
                            for every in del_msg_query:
                                del msg_query[every]
                    msg_query[cookie] = (jabber_mid, resource, c_time)
                    # update query
                    uvars['wait_for_confirm_msg_query'] = msg_query
                    self.legacyList.setUserVars(uin, uvars)
                    log.msg('Waiting for confirmations msg query: %s' %
                            msg_query)
                else:
                    cookie = None

                # if contact uses utf-8 via serv_rel and necessary see on it
                # or if contact has unicode & serl_rel caps and utf-8 via
                # serv_rel preferred
                if (str(self.getUserVarValue(uin, 'utf8_msg_using')) == '1' and int(self.bos.selfSettings['utf8_messages_sendmode']) == 1) or (self.legacyList.hasCapability(uin, 'serv_rel') and self.legacyList.hasCapability(uin, 'unicode') and int(self.bos.selfSettings['utf8_messages_sendmode']) == 2 and not offline):
                    # send as type-2 message
                    self.bos.sendMessageType2(uin, message, cookie=cookie)
                else:  # send as usual message, choose encoding
                    # Unicode for offline messages
                    if offline and int(self.bos.settingsOptionValue('offline_messages_sendenc')) == 0:
                        charset = 'unicode'  # utf-16be
                    # local encoding for offline messages
                    elif offline and int(self.bos.settingsOptionValue('offline_messages_sendenc')) == 1:
                        charset = 'custom'  # single-byte encoding
                    else:  # autodetect (both for offline and online messages)
                        # contact has unicode cap
                        if self.legacyList.hasCapability(uin, 'unicode'):
                            charset = 'unicode'  # utf-16be
                        else:
                            charset = 'custom'  # single-byte encoding
                    self.bos.sendMessage(uin, [[message, charset]], offline=offline, wantIcon=wantIcon,
                                         autoResponse=autoResponse, iconSum=iconSum, iconLen=iconLen, iconStamp=iconStamp, cookie=cookie)
                self.session.sendArchive(
                    target, self.session.jabberID, message)
            else:  # AIM users
                if xhtml and not config.disableXHTML:
                    xhtml = utils.xhtml_to_aimhtml(xhtml)
                    self.bos.sendMessage(
                        uin, xhtml, wantIcon=wantIcon, autoResponse=autoResponse, iconSum=iconSum, iconLen=iconLen, iconStamp=iconStamp)
                    self.session.sendArchive(
                        target, self.session.jabberID, message)
                else:
                    htmlized = oscar.html(message)
                    self.bos.sendMessage(
                        uin, htmlized, wantIcon=wantIcon, autoResponse=autoResponse, iconSum=iconSum, iconLen=iconLen, iconStamp=iconStamp)
                    self.session.sendArchive(
                        target, self.session.jabberID, message)
        except AttributeError:
            self.alertUser(lang.get("sessionnotactive", config.jid))

    def newResourceOnline(self, resource):
        from glue import icq2jid
        LogEvent(INFO, self.session.jabberID)
        try:
            for c in self.legacyList.ssicontacts.keys():
                LogEvent(INFO, self.session.jabberID, "Resending buddy %r" % c)
                jid = icq2jid(c)
                show = self.legacyList.ssicontacts[c]['show']
                status = self.legacyList.ssicontacts[c]['status']
                ptype = self.legacyList.ssicontacts[c]['presence']
                url = self.legacyList.ssicontacts[c]['url']
                # FIXME, needs to be contact based updatePresence
                self.session.sendPresence(
                    to=self.session.jabberID, fro=jid, show=show, status=status, ptype=ptype, url=url)
        except AttributeError:
            return

    def setAway(self, awayMessage=None):
        LogEvent(INFO, self.session.jabberID)
        try:
            self.bos.awayResponses = {}
            self.bos.setAway(utils.xmlify(awayMessage))
        except AttributeError:
            #self.alertUser(lang.get("sessionnotactive", config.jid))
            pass

    def setBack(self, backMessage=None):
        LogEvent(INFO, self.session.jabberID)
        try:
            self.bos.awayResponses = {}
            self.bos.setExtendedStatusRequest(utils.utf8encode(backMessage))
        except AttributeError:
            #self.alertUser(lang.get("sessionnotactive", config.jid))
            pass

    def sendShowStatus(self, jid=None):
        if not self.session:
            return
        if not jid:
            jid = self.jabberID
        self.session.sendPresence(
            to=jid, fro=config.jid, show=self.savedShow, status=self.savedFriendly)

    def setStatus(self, nickname, show, friendly, url=None):
        LogEvent(INFO, self.session.jabberID)

        if show:
            if show in ('away', 'dnd', 'xa', 'chat'):
                if not friendly:
                    friendly = lang.get('status_%s' % show)
            else:
                show = None

        self.savedShow = show
        self.savedFriendly = friendly
        self.savedURL = url

        if not self.session.ready:
            return

        self.setICQStatus(show)
        self.setAway(friendly)
        self.session.sendPresence(
            to=self.session.jabberID, fro=config.jid, show=show, status=friendly, url=url)

    def setProfile(self, profileMessage=None):
        LogEvent(INFO, self.session.jabberID)
        try:
            self.bos.setProfile(profileMessage)
        except AttributeError:
            #self.alertUser(lang.get("sessionnotactive", config.jid))
            pass

    def setICQStatus(self, status):
        LogEvent(INFO, self.session.jabberID)
        try:
            self.bos.setICQStatus(status)
        except AttributeError:
            # self.alertUser(lang.get(config.jid).sessionnotactive)
            pass

    def buildFriendly(self, status):
        friendly = self.jabberID[:self.jabberID.find('@')]
        if status and len(status) > 0:
            friendly += " - "
            friendly += status
        if len(friendly) > 127:
            friendly = friendly[:124] + "..."
        return friendly

    def sendTypingNotify(self, type, dest):
        from tlib.oscar import MTN_FINISH, MTN_IDLE, MTN_BEGIN
        from glue import jid2icq
        try:
            username = jid2icq(dest)
            LogEvent(INFO, self.session.jabberID)
            if type == "begin":
                self.bos.sendTypingNotification(username, MTN_BEGIN)
            elif type == "idle":
                self.bos.sendTypingNotification(username, MTN_IDLE)
            elif type == "finish":
                self.bos.sendTypingNotification(username, MTN_FINISH)
        except AttributeError:
            self.alertUser(lang.get("sessionnotactive", config.jid))

    def userTypingNotification(self, dest, resource, composing):
        LogEvent(INFO, self.session.jabberID)
        if composing:
            self.sendTypingNotify("begin", dest)
        else:
            self.sendTypingNotify("finish", dest)

    def chatStateNotification(self, dest, resource, state, withmessage=False):
        LogEvent(INFO, self.session.jabberID)
        from glue import jid2icq
        user = jid2icq(dest)
        prev_legacy_state = self.getUserVarValue(user, 'last_chatstate_event')
        if prev_legacy_state not in ('begin', 'idle', 'finish'):
            prev_legacy_state = 'finish'

        legacy_state = None
        if state == 'composing' and prev_legacy_state in ('finish', 'idle'):
            legacy_state = 'begin'
        elif state in ('paused', 'inactive') and prev_legacy_state == 'begin':
            legacy_state = 'idle'
        elif (state == 'gone' or withmessage) and prev_legacy_state in ('begin', 'idle'):
            legacy_state = 'finish'

        if legacy_state:
            self.sendTypingNotify(legacy_state, dest)
            uvars = dict([])
            uvars['last_chatstate_event'] = legacy_state
            self.legacyList.setUserVars(user, uvars)

    def jabberVCardRequest(self, vcard, user):
        LogEvent(INFO, self.session.jabberID)
        return self.getvCard(vcard, user)

    def getvCardNotInList(self, vcard, jid):
        try:
            LogEvent(INFO, self.session.jabberID)
        except AttributeError:
            pass

        user = jid.split('@')[0]
        return self.getvCard(vcard, user)

    def resourceOffline(self, resource):
        LogEvent(INFO, self.session.jabberID)
        from glue import icq2jid
        try:
            show = None
            status = None
            ptype = "unavailable"
            for c in self.legacyList.ssicontacts.keys():
                LogEvent(INFO, self.session.jabberID, "Sending offline %r" % c)
                jid = icq2jid(c)

                self.session.sendPresence(
                    to=self.session.jabberID + "/" + resource, fro=jid, ptype=ptype, show=show, status=status)
            self.session.sendPresence(
                to=self.session.jabberID + "/" + resource, fro=config.jid, ptype=ptype, show=show, status=status)
        except AttributeError:
            return

    def updateAvatar(self, av=None):
        """ Called whenever a new avatar needs to be set. Instance of avatar.Avatar is passed """
        if config.disableAvatars:
            return
        imageData = ""
        if av:
            imageData = av.getImageData()
        else:
            if not config.disableDefaultAvatar:
                global defaultAvatarData
                imageData = defaultAvatarData
            else:
                imageData = None

        self.changeAvatar(imageData)

    def changeAvatar(self, imageData):
        if config.disableAvatars:
            return
        if imageData:
            try:
                self.myavatar = imgmanip.convertToJPG(imageData)
                self.myavatarlen = len(self.myavatar)
                m = md5.new()
                m.update(self.myavatar)
                self.myavatarsum = m.digest()
                self.myavatarstamp = time.time()
            except:
                LogEvent(
                    INFO, self.session.jabberID, "Unable to convert avatar to JPEG")
                return
        if hasattr(self, "bos") and self.session.ready:
            if not imageData:
                if hasattr(self, "myavatar"):
                    del self.myavatar
                if len(self.bos.ssiiconsum) > 0:
                    self.bos.startModifySSI()
                    for i in self.bos.ssiiconsum:
                        LogEvent(INFO, self.session.jabberID, "Removing icon %s (u:%d g:%d)" % (
                            i.name, i.buddyID, i.groupID))
                        de = self.bos.delItemSSI(i)
                    self.bos.endModifySSI()
                return
            if len(self.bos.ssiiconsum) > 0 and self.bos.ssiiconsum[0]:
                LogEvent(
                    INFO, self.session.jabberID, "Replacing existing icon")
                self.bos.ssiiconsum[0].updateIcon(imageData)
                self.bos.startModifySSI()
                self.bos.modifyItemSSI(self.bos.ssiiconsum[0])
                self.bos.endModifySSI()
            else:
                LogEvent(INFO, self.session.jabberID, "Adding new icon")
                newBuddySum = oscar.SSIIconSum()
                newBuddySum.updateIcon(imageData)
                self.bos.startModifySSI()
                self.bos.addItemSSI(newBuddySum)
                self.bos.endModifySSI()

    def doSearch(self, form, iq):
        LogEvent(INFO, self.session.jabberID)
        # TEST self.bos.sendInterestsRequest()
        email = utils.getDataFormValue(form, "email")
        first = utils.getDataFormValue(form, "first")
        middle = utils.getDataFormValue(form, "middle")
        last = utils.getDataFormValue(form, "last")
        maiden = utils.getDataFormValue(form, "maiden")
        nick = utils.getDataFormValue(form, "nick")
        address = utils.getDataFormValue(form, "address")
        city = utils.getDataFormValue(form, "city")
        state = utils.getDataFormValue(form, "state")
        zip = utils.getDataFormValue(form, "zip")
        country = utils.getDataFormValue(form, "country")
        interest = utils.getDataFormValue(form, "interest")
        try:
            d = defer.Deferred()
            self.bos.sendDirectorySearch(email=email, first=first, middle=middle, last=last, maiden=maiden, nickname=nick, address=address, city=city,
                                         state=state, zip=zip, country=country, interest=interest).addCallback(self.gotSearchResults, iq, d).addErrback(self.gotSearchError, d)
            return d
        except AttributeError:
            self.alertUser(lang.get("sessionnotactive", config.jid))

    def gotSearchResults(self, results, iq, d):
        LogEvent(INFO, self.session.jabberID)
        from glue import icq2jid

        x = None
        for query in iq.elements():
            if query.name == "query":
                for child in query.elements():
                    if child.name == "x":
                        x = child
                        break
                break

        if x:
            for r in results:
                if r.has_key("screenname"):
                    r["jid"] = icq2jid(r["screenname"])
                else:
                    r["jid"] = "Unknown"
                item = x.addElement("item")
                for k in ["jid", "first", "middle", "last", "maiden", "nick", "email", "address", "city", "state", "country", "zip", "region"]:
                    item.addChild(
                        utils.makeDataFormElement(None, k, value=r.get(k, None)))
        d.callback(iq)

    def gotSearchError(self, error, d):
        LogEvent(INFO, self.session.jabberID)
        # d.callback(vcard)

    def getvCard(self, vcard, user):
        try:
            LogEvent(INFO, self.session.jabberID)
        except AttributeError:
            pass
        if (not user.isdigit()):
            try:
                d = defer.Deferred()
                self.bos.getProfile(user).addCallback(
                    self.gotAIMvCard, user, vcard, d).addErrback(self.gotnovCard, user, vcard, d)
                return d
            except AttributeError:
                self.alertUser(lang.get("sessionnotactive", config.jid))
        else:
            try:
                d = defer.Deferred()
                #self.bos.getMetaInfo(user).addCallback(self.gotvCard, user, vcard, d)
                self.userinfoID = (self.userinfoID + 1) % 256
                self.userinfoCollection[self.userinfoID] = UserInfoCollector(
                    self.userinfoID, d, vcard, user)
                # .addCallback(self.gotvCard, user, vcard, d)
                self.bos.getMetaInfo(user, self.userinfoID)
                return d
            except AttributeError:
                self.alertUser(lang.get("sessionnotactive", config.jid))

    def gotAIMvCard(self, profile, user, vcard, d):
        from glue import icq2jid

        LogEvent(INFO, self.session.jabberID)

        cutprofile = oscar.dehtml(profile)
        nickname = vcard.addElement("NICKNAME")
        nickname.addContent(utils.xmlify(user))
        jabberid = vcard.addElement("JABBERID")
        jabberid.addContent(icq2jid(user))
        desc = vcard.addElement("DESC")
        desc.addContent(utils.xmlify(cutprofile))

        d.callback(vcard)

    def getAutoAwayMessage(self, userHandle):
        LogEvent(INFO, self.session.jabberID)
        if userHandle in self.legacyList.usercustomstatuses:
            customStatus = self.legacyList.usercustomstatuses[userHandle]
            if 'autoaway message' in customStatus:
                return customStatus['autoaway message']
        return ''

    def getXStatus(self, userHandle, mood_pref=False):
        # returns text of x-status icon
        # sample: 'Working','Typing', ''
        LogEvent(INFO, self.session.jabberID)
        if userHandle in self.legacyList.usercustomstatuses:
            customStatus = self.legacyList.usercustomstatuses[userHandle]
            if not mood_pref:  # 'x-status' field preferred
                if 'x-status' in customStatus:
                    return customStatus['x-status']
                elif 'icqmood' in customStatus:
                    return customStatus['icqmood']
            else:  # 'icqmood' field preferred
                if 'icqmood' in customStatus:
                    return customStatus['icqmood']
                elif 'x-status' in customStatus:
                    return customStatus['x-status']
        return ''

    def getXStatusDetails(self, userHandle):
        # returns title and description of x-status message
        LogEvent(INFO, self.session.jabberID)
        title = ''
        desc = ''
        if userHandle in self.legacyList.usercustomstatuses:
            customStatus = self.legacyList.usercustomstatuses[userHandle]
            if 'x-status title' in customStatus:
                title = customStatus['x-status title']
            if 'x-status desc' in customStatus:
                desc = customStatus['x-status desc']
        return title, desc

    def getPersonalEvents(self, userHandle):
        # returns mood and activity
        LogEvent(INFO, self.session.jabberID)
        mood = None
        activity = None
        subactivity = None
        text = None
        usetune = False
        if userHandle in self.legacyList.usercustomstatuses:
            customStatus = self.legacyList.usercustomstatuses[userHandle]
            if 'mood' in customStatus:
                mood = customStatus['mood']
            if 'activity' in customStatus:
                activity = customStatus['activity']
            if 'subactivity' in customStatus:
                subactivity = customStatus['subactivity']
            if 'text' in customStatus:
                text = customStatus['text']
            if 'usetune' in customStatus:
                usetune = customStatus['usetune']
        return mood, activity, subactivity, text, usetune

    def setPersonalEvents(self, userHandle, mood=None, activity=None, subactivity=None, text=None, usetune=False):
        # sets mood and activity
        LogEvent(INFO, self.session.jabberID)
        if userHandle not in self.legacyList.usercustomstatuses:
            self.legacyList.usercustomstatuses[userHandle] = {}
        if userHandle in self.legacyList.usercustomstatuses:
            customStatus = self.legacyList.usercustomstatuses[userHandle]
            if mood:
                customStatus['mood'] = mood
            else:
                if 'mood' in customStatus:
                    del customStatus['mood']
            if activity:
                customStatus['activity'] = activity
            else:
                if 'activity' in customStatus:
                    del customStatus['activity']
            if subactivity:
                customStatus['subactivity'] = subactivity
            else:
                if 'subactivity' in customStatus:
                    del customStatus['subactivity']
            if text:
                customStatus['text'] = text
            else:
                if 'text' in customStatus:
                    del customStatus['text']
            if usetune:
                customStatus['usetune'] = usetune
            else:
                if 'usetune' in customStatus:
                    del customStatus['usetune']

    def setSavedSnac(self, userHandle, snac):
        LogEvent(INFO, self.session.jabberID)
        self.legacyList.saved_snacs[userHandle] = snac

    def getSavedSnac(self, userHandle):
        LogEvent(INFO, self.session.jabberID)
        if self.legacyList.saved_snacs.has_key(userHandle):
            return self.legacyList.saved_snacs[userHandle]
        else:
            return ''

    def getUserVarValue(self, userHandle, key):
        LogEvent(INFO, self.session.jabberID)
        if userHandle in self.legacyList.uservars:
            uvars = self.legacyList.uservars[userHandle]
            if key in uvars:
                return uvars[key]
        return ''

    def getSelfPersonalEvents(self):
        # returns mood and activity
        LogEvent(INFO, self.session.jabberID)
        mood = None
        activity = None
        subactivity = None
        text = None
        usetune = False
        if self.bos.selfCustomStatus:
            customStatus = self.bos.selfCustomStatus
            if 'mood' in customStatus:
                mood = customStatus['mood']
            if 'activity' in customStatus:
                activity = customStatus['activity']
            if 'subactivity' in customStatus:
                subactivity = customStatus['subactivity']
            if 'text' in customStatus:
                text = customStatus['text']
            if 'usetune' in customStatus:
                usetune = customStatus['usetune']
        return mood, activity, subactivity, text, usetune

    def setSelfPersonalEvents(self, mood=None, activity=None, subactivity=None, text=None, usetune=False):
        # sets mood and activity
        LogEvent(INFO, self.session.jabberID)
        if self.bos.selfCustomStatus:
            customStatus = self.bos.selfCustomStatus
            if mood:
                customStatus['mood'] = mood
            else:
                if 'mood' in customStatus:
                    del customStatus['mood']
            if activity:
                customStatus['activity'] = activity
            else:
                if 'activity' in customStatus:
                    del customStatus['activity']
            if subactivity:
                customStatus['subactivity'] = subactivity
            else:
                if 'subactivity' in customStatus:
                    del customStatus['subactivity']
            if text:
                customStatus['text'] = text
            else:
                if 'text' in customStatus:
                    del customStatus['text']
            if usetune:
                customStatus['usetune'] = usetune
            else:
                if 'usetune' in customStatus:
                    del customStatus['usetune']

    def delSelfCustomStatus(self, delmask=None, savemask=None):
        LogEvent(INFO, self.session.jabberID)
        if self.bos.selfCustomStatus:  # if custom status exists
            if savemask == None:  # erase all
                del self.bos.selfCustomStatus
            else:  # save only some keys
                delmask = list()
                for key in self.bos.selfCustomStatus:
                    if key not in savemask:
                        delmask.append(key)  # need erase this key
            if delmask != None:  # erase only some keys
                for key in delmask:
                    if key in self.bos.selfCustomStatus:
                        del self.bos.selfCustomStatus[key]

    def gotvCard(self, usercol):
        from glue import icq2jid

        LogEvent(INFO, self.session.jabberID)

        if usercol != None and usercol.valid:
            vcard = usercol.vcard
            fn = vcard.addElement("FN")
            fn.addContent(utils.xmlify(usercol.first + " " + usercol.last))
            n = vcard.addElement("N")
            given = n.addElement("GIVEN")
            given.addContent(utils.xmlify(usercol.first))
            family = n.addElement("FAMILY")
            family.addContent(utils.xmlify(usercol.last))
            middle = n.addElement("MIDDLE")
            nickname = vcard.addElement("NICKNAME")
            nickname.addContent(utils.xmlify(usercol.nick))
            if usercol.nick:
                self.legacyList.updateNickname(usercol.userinfo, usercol.nick)
            bday = vcard.addElement("BDAY")
            bday.addContent(utils.xmlify(usercol.birthday))
            desc = vcard.addElement("DESC")
            desc.addContent(utils.xmlify(usercol.about))
            try:
                c = self.legacyList.ssicontacts[usercol.userinfo]
                desc.addContent(utils.xmlify("\n\n-----\n" + c['lanipaddr'] + '/' + c[
                                'ipaddr'] + ':' + "%s" % (c['lanipport']) + ' v.' + "%s" % (c['icqprotocol'])))
            except:
                pass

            url = vcard.addElement("URL")
            url.addContent(utils.xmlify(usercol.homepage))

            # Home address
            adr = vcard.addElement("ADR")
            adr.addElement("HOME")
            street = adr.addElement("STREET")
            street.addContent(utils.xmlify(usercol.homeAddress))
            locality = adr.addElement("LOCALITY")
            locality.addContent(utils.xmlify(usercol.homeCity))
            region = adr.addElement("REGION")
            region.addContent(utils.xmlify(usercol.homeState))
            pcode = adr.addElement("PCODE")
            pcode.addContent(utils.xmlify(usercol.homeZIP))
            ctry = adr.addElement("CTRY")
            ctry.addContent(utils.xmlify(usercol.homeCountry))
            # home number
            tel = vcard.addElement("TEL")
            tel.addElement("VOICE")
            tel.addElement("HOME")
            telNumber = tel.addElement("NUMBER")
            telNumber.addContent(utils.xmlify(usercol.homePhone))
            tel = vcard.addElement("TEL")
            tel.addElement("FAX")
            tel.addElement("HOME")
            telNumber = tel.addElement("NUMBER")
            telNumber.addContent(utils.xmlify(usercol.homeFax))
            tel = vcard.addElement("TEL")
            tel.addElement("CELL")
            tel.addElement("HOME")
            number = tel.addElement("NUMBER")
            number.addContent(utils.xmlify(usercol.cellPhone))
            # email
            email = vcard.addElement("EMAIL")
            email.addElement("INTERNET")
            email.addElement("PREF")
            emailid = email.addElement("USERID")
            emailid.addContent(utils.xmlify(usercol.email))

            # work
            adr = vcard.addElement("ADR")
            adr.addElement("WORK")
            street = adr.addElement("STREET")
            street.addContent(utils.xmlify(usercol.workAddress))
            locality = adr.addElement("LOCALITY")
            locality.addContent(utils.xmlify(usercol.workCity))
            region = adr.addElement("REGION")

            region.addContent(utils.xmlify(usercol.workState))
            pcode = adr.addElement("PCODE")
            pcode.addContent(utils.xmlify(usercol.workZIP))
            ctry = adr.addElement("CTRY")
            ctry.addContent(utils.xmlify(usercol.workCountry))

            tel = vcard.addElement("TEL")
            tel.addElement("WORK")
            tel.addElement("VOICE")
            number = tel.addElement("NUMBER")
            number.addContent(utils.xmlify(usercol.workPhone))
            tel = vcard.addElement("TEL")
            tel.addElement("WORK")
            tel.addElement("FAX")
            number = tel.addElement("NUMBER")
            number.addContent(utils.xmlify(usercol.workFax))

            jabberid = vcard.addElement("JABBERID")
            jabberid.addContent(
                utils.xmlify(usercol.userinfo + "@" + config.jid))

            usercol.d.callback(vcard)
        elif usercol:
            usercol.d.callback(usercol.vcard)
        else:
            self.session.sendErrorMessage(self.session.jabberID, uin + "@" + config.jid,
                                          "cancel", "undefined-condition", "", "Unable to retrieve user information")
            # error of some kind

    def gotnovCard(self, profile, user, vcard, d):
        from glue import icq2jid
        LogEvent(INFO, self.session.jabberID)

        nickname = vcard.addElement("NICKNAME")
        nickname.addContent(utils.xmlify(user))
        jabberid = vcard.addElement("JABBERID")
        jabberid.addContent(icq2jid(user))
        desc = vcard.addElement("DESC")
        desc.addContent("User is not online.")

        d.callback(vcard)

    def icq2uhandle(self, icqid):
        retstr = icqid.replace(' ', '')
        return retstr.lower()

    def updatePresence(self, userHandle, ptype):  # Convenience
        from glue import icq2jid
        to = icq2jid(userHandle)
        self.session.sendPresence(
            to=self.session.jabberID, fro=to, ptype=ptype)

    def addContact(self, userHandle):
        LogEvent(INFO, self.session.jabberID)

        def cb(arg=None):
            self.updatePresence(userHandle, "subscribed")

        try:
            for g in self.bos.ssigroups:
                for u in g.users:
                    icqHandle = self.icq2uhandle(u.name)
                    if icqHandle == userHandle:
                        if not u.authorizationRequestSent and not u.authorized:
                            self.bos.sendAuthorizationRequest(
                                userHandle, "Please authorize me!")
                            u.authorizationRequestSent = True
                            return
                        else:
                            cb()
                            return

            savethisgroup = None
            groupName = "PyICQ-t Buddies"
            for g in self.bos.ssigroups:
                if g.name == groupName:
                    LogEvent(
                        INFO, self.session.jabberID, "Located group %s" % (g.name))
                    savethisgroup = g

            if savethisgroup is None:
                LogEvent(INFO, self.session.jabberID, "Adding new group")
                newGroupID = self.generateGroupID()
                newGroup = oscar.SSIGroup(groupName, newGroupID, 0)
                self.bos.startModifySSI()
                self.bos.addItemSSI(newGroup)
                self.bos.endModifySSI()
                savethisgroup = newGroup
                self.bos.ssigroups.append(newGroup)

            group = self.findGroupByName(groupName)
            newUserID = self.generateBuddyID(group.groupID)
            newUser = oscar.SSIBuddy(userHandle, group.groupID, newUserID)
            savethisgroup.addUser(newUserID, newUser)

            LogEvent(INFO, self.session.jabberID, "Adding item to SSI")
            self.bos.startModifySSI()
            self.bos.addItemSSI(newUser)
            self.bos.modifyItemSSI(savethisgroup)
            self.bos.endModifySSI()

            self.legacyList.updateSSIContact(userHandle)
            self.updatePresence(userHandle, "subscribe")
        except AttributeError:
            self.alertUser(lang.get("sessionnotactive", config.jid))

    def removeContact(self, userHandle):
        LogEvent(INFO, self.session.jabberID)
        try:
            def cb(arg=None):
                self.updatePresence(userHandle, "unsubscribed")

            savetheseusers = []

            if userHandle in self.bos.authorizationRequests:
                self.bos.sendAuthorizationResponse(userHandle, False, "")
                self.bos.authorizationRequests.remove(userHandle)

            for g in self.bos.ssigroups:
                for u in g.users:
                    icqHandle = self.icq2uhandle(u.name)
                    LogEvent(
                        INFO, self.session.jabberID, "Comparing %s and %s" % (icqHandle, userHandle))
                    if icqHandle == userHandle:
                        LogEvent(
                            INFO, self.session.jabberID, "Located user %s" % (u.name))
                        savetheseusers.append(u)

            if len(savetheseusers) == 0:
                LogEvent(INFO, self.session.jabberID, "Did not find user")
                return

            self.bos.startModifySSI()
            for u in savetheseusers:
                LogEvent(INFO, self.session.jabberID, "Removing %s (u:%d g:%d) from group %s" % (
                    u.name, u.buddyID, u.groupID, u.group.name))
                de = self.bos.delItemSSI(u)
                de.addCallback(self.SSIItemDeleted, u)
            de.addCallback(cb)
            self.bos.endModifySSI()
        except AttributeError:
            self.alertUser(lang.get("sessionnotactive", config.jid))

    def authContact(self, userHandle):
        LogEvent(INFO, self.session.jabberID)
        try:
            if userHandle in self.bos.authorizationRequests:
                self.bos.sendAuthorizationResponse(userHandle, True, "OK")
                self.bos.authorizationRequests.remove(userHandle)
        except AttributeError:
            self.alertUser(lang.get("sessionnotactive", config.jid))

    def deauthContact(self, userHandle):
        LogEvent(INFO, self.session.jabberID)
        # I don't recall why these are the same
        self.authContact(userHandle)

    def SSIItemDeleted(self, x, user):
        c = 0
        for g in self.bos.ssigroups:
            c += 1
            for u in g.users:
                if u.buddyID == user.buddyID and u.groupID == user.groupID:
                    g.users.remove(u)
                    del g.usersToID[u]

    def errorCallback(self, result):
        try:
            LogEvent(INFO, self.session.jabberID)
            errmsg = result.getErrorMessage()
            errmsgs = errmsg.split("'")
            message = "Authentication Error!"
            if errmsgs[1]:
                message = message + "\n" + errmsgs[1]
            if errmsgs[3]:
                message = message + "\n" + errmsgs[3]
            self.alertUser(message)
            self.session.removeMe()
        except:
            pass

    def findGroupByID(self, groupID):
        for x in self.bos.ssigroups:
            if x.groupID == groupID:
                return x

    def findGroupByName(self, groupName):
        for x in self.bos.ssigroups:
            if x.name == groupName:
                return x

    def generateGroupID(self):
        pGroupID = len(self.bos.ssigroups)
        while True:
            pGroupID += 1
            found = False
            for x in self.bos.ssigroups:
                if pGroupID == x.groupID:
                    found = True
                    break
            if not found:
                break
        return pGroupID

    def generateBuddyID(self, groupID):
        group = self.findGroupByID(groupID)
        pBuddyID = len(group.users)
        while True:  # If all integers are taken we got a bigger problems
            pBuddyID += 1
            found = False
            for x in group.users:
                if pBuddyID == x.buddyID:
                    found = True
                    break
            if not found:
                break
        return pBuddyID

    def alertUser(self, message):
        if self.session:
            tmpjid = config.jid
            if self.session.registeredmunge:
                tmpjid = tmpjid + "/registered"
            self.session.sendErrorMessage(
                self.session.jabberID, tmpjid, 'cancel', '', 'undefined-condition', message)


class UserInfoCollector:

    def __init__(self, id, d, vcard, userinfo):
        self.packetCounter = 0
        self.vcard = vcard
        self.d = d
        self.id = id
        self.userinfo = userinfo
        self.nick = None
        self.first = None
        self.last = None
        self.email = None
        self.homeCity = None
        self.homeState = None
        self.homePhone = None
        self.homeFax = None
        self.homeAddress = None
        self.cellPhone = None
        self.homeZIP = None
        self.homeCountry = None
        self.workCity = None
        self.workState = None
        self.workPhone = None
        self.workFax = None
        self.workAddress = None
        self.workZIP = None
        self.workCountry = None
        self.workCompany = None
        self.workDepartment = None
        self.workPosition = None
        self.workRole = None
        self.homepage = None
        self.about = None
        self.birthday = None
        self.valid = True

    def gotUserInfo(self, id, type, userinfo):
        self.packetCounter += 1
        if type == 0xffff:
            self.valid = False
            self.packetCounter = 8  # we'll get no more packages
        if type == 0xc8:
            # basic user info
            self.nick = userinfo[0]
            self.first = userinfo[1]
            self.last = userinfo[2]
            self.email = userinfo[3]
            self.homeCity = userinfo[4]
            self.homeState = userinfo[5]
            self.homePhone = userinfo[6]
            self.homeFax = userinfo[7]
            self.homeAddress = userinfo[8]
            self.cellPhone = userinfo[9]
            self.homeZIP = userinfo[10]
            self.homeCountry = userinfo[11]
        elif type == 0xdc:
            self.homepage = userinfo[0]
            self.birthday = userinfo[1]
        elif type == 0xd2:
            self.workCity = userinfo[0]
            self.workState = userinfo[1]
            self.workPhone = userinfo[2]
            self.workFax = userinfo[3]
            self.workAddress = userinfo[4]
            self.workZIP = userinfo[5]
            self.workCountry = userinfo[6]
            self.workCompany = userinfo[7]
            self.workDepartment = userinfo[8]
            self.workPosition = userinfo[9]
        elif type == 0xe6:
            self.about = userinfo[0]

        if self.packetCounter >= 8:
            return True
        else:
            return False
