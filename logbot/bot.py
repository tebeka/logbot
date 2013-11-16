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

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("groupchat_message", self.publish)

    def session_start(self, event):
        self.register_plugin('xep_0045')
        self.send_presence()
        self.get_roster()

        self.plugin['xep_0045'].joinMUC(self.room, self.nick, wait=True)

    def xmpp_user(self, xmpp_msg):
        return xmpp_msg['mucnick'] or xmpp_msg['from'].split('@', 1)[0]

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
