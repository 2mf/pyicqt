# Licensed for distribution under the GPL version 2, check COPYING for details

from twisted.words.xish.domish import Element
from twisted.words.protocols.jabber.jid import internJID
from pyicqt import utils
from pyicqt.tlib import oscar
from pyicqt.debug import LogEvent, INFO, WARN, ERROR
from pyicqt import config
from pyicqt import lang
from pyicqt import globals
from pyicqt.adhoc import rights_guest, rights_user, rights_admin

# TODO: rewrite with better code)


class SetXStatus:

    def __init__(self, pytrans):
        self.pytrans = pytrans
        self.pytrans.adhoc.addCommand(
            'setxstatus', self.incomingIq, 'command_SetXStatus', rights_user)

    def incomingIq(self, el):

        xstatus_name = None
        xstatus_title = None
        xstatus_desc = None
        sessionid = None
        do_action = None
        return_back = False
        stage = 0

        to = el.getAttribute('from')
        toj = internJID(to)
        jid = toj.userhost()
        ID = el.getAttribute('id')
        ulang = utils.getLang(el)

        for command in el.elements():
            sessionid = command.getAttribute('sessionid')

            if jid in self.pytrans.sessions:
                if not config.xstatusessupport:
                    self.sendXStatusCompleted(
                        el, lang.get('xstatus_support_disabled'), sessionid)
                if int(self.pytrans.sessions[jid].legacycon.bos.settingsOptionValue('xstatus_sending_mode')) == 0:
                    self.sendXStatusCompleted(
                        el, lang.get('xstatus_sending_disabled'), sessionid)

            if command.getAttribute('action') == 'execute':
                pass
            elif command.getAttribute('action') == 'complete':
                do_action = 'done'
            elif command.getAttribute('action') == 'cancel':
                do_action = 'cancel'
            elif command.getAttribute('action') == 'prev':  # back
                return_back = True

            for child in command.elements():
                if child.name == 'x':
                    for field in child.elements():
                        if field.name == 'field':  # extract data
                            if field.getAttribute('var') == 'stage':
                                for value in field.elements():
                                    if value.name == 'value':
                                        stage = value.__str__()
                                        if return_back and int(stage) >= 0:
                                            stage = int(stage) - 1
                            if field.getAttribute('var') == 'xstatus_name':
                                for value in field.elements():
                                    if value.name == 'value':
                                        xstatus_name = value.__str__()
                            elif field.getAttribute('var') == 'xstatus_title':
                                for value in field.elements():
                                    if value.name == 'value':
                                        xstatus_title = value.__str__()
                            elif field.getAttribute('var') == 'xstatus_desc':
                                multiline = ''
                                for value in field.elements():
                                    if value.name == 'value':
                                        if multiline != '':
                                            multiline = multiline + \
                                                '\n' + value.__str__()
                                        else:
                                            multiline = value.__str__()
                                xstatus_desc = multiline

        if jid not in self.pytrans.sessions:  # if user not logined
            self.pytrans.adhoc.sendError('setxstatus', el, errormsg=lang.get(
                'command_NoSession', ulang), sessionid=sessionid)
        # if user not connected to ICQ network
        elif not hasattr(self.pytrans.sessions[toj.userhost()].legacycon, 'bos'):
            self.pytrans.adhoc.sendError('setxstatus', el, errormsg=lang.get(
                'command_NoSession', ulang), sessionid=sessionid)
        elif stage == '1':
            if xstatus_name != 'None':
                self.sendXStatusTextSelectionForm(
                    el, xstatus_name, sessionid)  # send second form
            else:
                # set only x-status name (icon)
                self.setXStatus(toj, xstatus_name)
                self.sendXStatusCompleted(
                    el, lang.get('xstatus_reset'), sessionid)  # send ack to user
        elif stage == '2' or do_action == 'done':
            # set x-status name and text
            self.setXStatus(toj, xstatus_name, xstatus_title, xstatus_desc)
            self.sendXStatusCompleted(
                el, lang.get('xstatus_set'), sessionid)  # send ack to user
        elif do_action == 'cancel':
            self.pytrans.adhoc.sendCancellation(
                "setxstatus", el, sessionid)  # correct cancel handling
        else:
            self.sendXStatusNameSelectionForm(el, sessionid)  # send first form

    def sendXStatusNameSelectionForm(self, el, sessionid=None):
        to = el.getAttribute('from')
        to_jid = internJID(to)
        jid = to_jid.userhost()
        ID = el.getAttribute('id')
        ulang = utils.getLang(el)

        iq = Element((None, 'iq'))
        iq.attributes['to'] = to
        iq.attributes['from'] = config.jid
        if ID:
            iq.attributes['id'] = ID
        iq.attributes['type'] = 'result'

        command = iq.addElement('command')
        if sessionid:
            command.attributes['sessionid'] = sessionid
        else:
            command.attributes['sessionid'] = self.pytrans.makeMessageID()
        command.attributes['node'] = 'setxstatus'
        command.attributes['xmlns'] = globals.COMMANDS
        command.attributes['status'] = 'executing'

        actions = command.addElement('actions')
        actions.attributes['execute'] = 'next'
        actions.addElement('next')

        x = command.addElement('x')
        x.attributes['xmlns'] = 'jabber:x:data'
        x.attributes['type'] = 'form'

        title = x.addElement('title')
        title.addContent(lang.get('xstatus_set_xstatus_name'))

        instructions = x.addElement('instructions')
        instructions.addContent(lang.get('xstatus_set_instructions'))

        field = x.addElement('field')
        field.attributes['var'] = 'xstatus_name'
        field.attributes['type'] = 'list-single'
        field.attributes['label'] = lang.get('xstatus_name')
        desc = field.addElement('desc')
        desc.addContent(lang.get('xstatus_set_instructions_Desc'))

        option = field.addElement('option')
        option.attributes['label'] = lang.get('xstatus_no_xstatus')
        value = option.addElement('value')
        value.addContent('None')

        counter = 0
        limit = False
        if int(self.pytrans.sessions[jid].legacycon.bos.settingsOptionValue('xstatus_sending_mode')) == 2:
            limit = True
            counter = 24
        for xstatus_title in oscar.X_STATUS_NAME:
            if limit:
                if counter > 0:
                    option = field.addElement('option')
                    option.attributes['label'] = lang.get(xstatus_title)
                    value = option.addElement('value')
                    value.addContent(xstatus_title)
                    counter -= 1
            else:
                option = field.addElement('option')
                option.attributes['label'] = lang.get(xstatus_title)
                value = option.addElement('value')
                value.addContent(xstatus_title)

        value = field.addElement('value')
        current_xstatus_name = self.pytrans.sessions[
            jid].legacycon.bos.getSelfXstatusName()
        if current_xstatus_name != '':
            value.addContent(current_xstatus_name)
        else:
            value.addContent('None')

        stage = x.addElement('field')
        stage.attributes['type'] = 'hidden'
        stage.attributes['var'] = 'stage'
        value = stage.addElement('value')
        value.addContent('1')

        self.pytrans.send(iq)

    def sendXStatusTextSelectionForm(self, el, xstatus_name, sessionid=None):

        to = el.getAttribute('from')
        ID = el.getAttribute('id')
        ulang = utils.getLang(el)

        iq = Element((None, 'iq'))
        iq.attributes['to'] = to
        iq.attributes['from'] = config.jid
        if ID:
            iq.attributes['id'] = ID
        iq.attributes['type'] = 'result'

        command = iq.addElement('command')
        if sessionid:
            command.attributes['sessionid'] = sessionid
        else:
            command.attributes['sessionid'] = self.pytrans.makeMessageID()
        command.attributes['node'] = 'setxstatus'
        command.attributes['xmlns'] = globals.COMMANDS
        command.attributes['status'] = 'executing'

        actions = command.addElement('actions')
        actions.attributes['execute'] = 'complete'
        actions.addElement('prev')
        actions.addElement('complete')

        x = command.addElement('x')
        x.attributes['xmlns'] = 'jabber:x:data'
        x.attributes['type'] = 'form'

        title = x.addElement('title')
        title.addContent(lang.get('xstatus_set_details'))

        toj = internJID(to)
        jid = toj.userhost()
        xstatus_number = self.pytrans.sessions[
            jid].legacycon.bos.getXstatusNumberByName(xstatus_name)
        title, desc = self.pytrans.xdb.getXstatusText(jid, xstatus_number)
        if title == '':
            title = lang.get(xstatus_name)
        else:
            if config.xdbDriver == 'xmlfiles':  # fix problem with & character
                title = utils.fixCharactersInDeXML(title)

        xstatus_title = x.addElement('field')
        xstatus_title.attributes['type'] = 'text-single'
        xstatus_title.attributes['var'] = 'xstatus_title'
        xstatus_title.attributes['label'] = lang.get('xstatus_title')
        value = xstatus_title.addElement('value')
        value.addContent(title)

        xstatus_desc = x.addElement('field')
        xstatus_desc.attributes['type'] = 'text-multi'
        xstatus_desc.attributes['var'] = 'xstatus_desc'
        xstatus_desc.attributes['label'] = lang.get('xstatus_description')
        value = xstatus_desc.addElement('value')
        value.addContent(desc)

        xstatus_icon = x.addElement('field')
        xstatus_icon.attributes['type'] = 'hidden'
        xstatus_icon.attributes['var'] = 'xstatus_name'
        value = xstatus_icon.addElement('value')
        value.addContent(xstatus_name)

        stage = x.addElement('field')
        stage.attributes['type'] = 'hidden'
        stage.attributes['var'] = 'stage'
        value = stage.addElement('value')
        value.addContent('2')

        self.pytrans.send(iq)

    def sendXStatusCompleted(self, el, message, sessionid=None):
        to = el.getAttribute('from')
        ID = el.getAttribute('id')
        ulang = utils.getLang(el)

        iq = Element((None, 'iq'))
        iq.attributes['to'] = to
        iq.attributes['from'] = config.jid
        if ID:
            iq.attributes['id'] = ID
        iq.attributes['type'] = 'result'

        command = iq.addElement('command')
        if sessionid:
            command.attributes['sessionid'] = sessionid
        else:
            command.attributes['sessionid'] = self.pytrans.makeMessageID()
        command.attributes['node'] = 'setxstatus'
        command.attributes['xmlns'] = globals.COMMANDS
        command.attributes['status'] = 'completed'

        note = command.addElement('note')
        note.attributes['type'] = 'info'
        note.addContent(message)

        x = command.addElement('x')
        x.attributes['xmlns'] = 'jabber:x:data'
        x.attributes['type'] = 'form'

        title = x.addElement('title')
        title.addContent(lang.get('command_SetXStatus'))

        instructions = x.addElement('instructions')
        instructions.addContent(message)

        self.pytrans.send(iq)

    def setXStatus(self, to_jid, xstatus_name, xstatus_title=None, xstatus_desc=None):
        jid = to_jid.userhost()
        LogEvent(INFO, jid)
        bos = self.pytrans.sessions[jid].legacycon.bos
        if xstatus_name == 'None':
            # no x-status
            # keep values for mood/activity
            mask = ('mood', 'activity', 'subactivity', 'text', 'usetune')
            bos.oscarcon.delSelfCustomStatus(savemask=mask)
        else:
            bos.selfCustomStatus['x-status name'] = xstatus_name
            if xstatus_title:
                bos.selfCustomStatus['x-status title'] = xstatus_title
            else:
                bos.selfCustomStatus['x-status title'] = ''
            if xstatus_desc:
                bos.selfCustomStatus['x-status desc'] = xstatus_desc
            else:
                bos.selfCustomStatus['x-status desc'] = ''
            bos.selfCustomStatus['avail.message'] = bos.selfCustomStatus[
                'x-status title'] + ' ' + bos.selfCustomStatus['x-status desc']
        bos.updateSelfXstatus()

        xstatus_number = bos.getXstatusNumberByName(xstatus_name)
        if jid in self.pytrans.sessions:
            if xstatus_title:
                xstatus_title = utils.fixCharactersInXML(xstatus_title)
            else:
                xstatus_title = ''
            self.pytrans.xdb.setXstatusText(
                jid, xstatus_number, xstatus_title, xstatus_desc)
            if bos.settingsOptionEnabled('xstatus_saving_enabled'):
                self.pytrans.xdb.setCSetting(
                    jid, 'latest_xstatus_number', str(xstatus_number))
