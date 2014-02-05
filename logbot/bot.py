from .common import publish, Message

from sleekxmpp import ClientXMPP

from datetime import datetime
from signal import signal, SIGINT


class LogBot(ClientXMPP):
    def __init__(self, jid, password, room, nick, tz=None):
        super(LogBot, self).__init__(jid, password)
        self.room = room
        self.nick = nick
        self.tz = tz

        register = self.add_event_handler

        register("session_start", self.session_start)
        register("groupchat_message", self.publish)

        def evt(name):
            return 'muc::{}::got_{}'.format(self.room, name)

        register(evt('online'), lambda evt: self.on_status(evt, 'entered'))
        register(evt('offline'), lambda evt: self.on_status(evt, 'left'))

    def session_start(self, event):
        self.register_plugin('xep_0045')
        self.send_presence()
        self.get_roster()

        self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

    def on_status(self, event, action):
        msg = {
            'mucnick': event['muc']['nick'],
            'from': event['from'],
            'body': '{} the room'.format(action),
        }
        self.publish(msg)

    def xmpp_user(self, xmpp_msg):
        return xmpp_msg['mucnick'] or xmpp_msg['from'].bare

    def publish(self, xmpp_msg):
        msg = Message(
            user=self.xmpp_user(xmpp_msg),
            content=xmpp_msg['body'],
            time=datetime.now(tz=self.tz),
        )
        publish(msg)


def run(host, port, user, passwd, rooms, use_tls=True, nick='logbot', tz=None):
    xmpp = LogBot(user, passwd, rooms, nick, tz)

    signal(SIGINT, lambda signum, frame: xmpp.disconnect())

    xmpp.connect((host, port), use_tls=use_tls)
    xmpp.process(block=True)
