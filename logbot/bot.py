from .common import publish, Message

from sleekxmpp import ClientXMPP

from datetime import datetime
from signal import signal, SIGINT


def muc_event(room, name):
    return 'muc::{}::got_{}'.format(room, name)


def xmpp_user(msg):
    return msg['mucnick'] or msg['from'].resource


class LogBot(ClientXMPP):
    def __init__(self, jid, password, rooms, nick, tz=None):
        super(LogBot, self).__init__(jid, password)
        self.rooms = rooms
        self.nick = nick
        self.tz = tz

        self.register_handlers(rooms)

    def register_handlers(self, rooms):
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("groupchat_message", self.publish)

    def join_room(self, room):
        self.plugin['xep_0045'].joinMUC(room, self.nick, wait=True)
        for name, action in [('online', 'entered'), ('offline', 'left')]:
            event = muc_event(room, name)
            self.add_event_handler(event, self.muc_handler(room, action))

    def muc_handler(self, room, action):
        return lambda evt: self.on_status(evt, room, action)

    def session_start(self, event):
        self.register_plugin('xep_0045')
        self.send_presence()
        self.get_roster()

        for room in self.rooms:
            self.join_room(room)

    def on_status(self, event, room, action):
        msg = {
            'from': event['from'],
            'body': '{} the room'.format(action),
        }
        self.publish(msg)


    def publish(self, xmpp_msg):
        msg = Message(
            user=xmpp_user(xmpp_msg),
            content=xmpp_msg['body'],
            time=datetime.now(tz=self.tz),
            room=xmpp_msg['from'].node,
        )
        publish(msg)


def run(host, port, user, passwd, rooms, use_tls=True, nick='logbot', tz=None):
    xmpp = LogBot(user, passwd, rooms, nick, tz)

    signal(SIGINT, lambda signum, frame: xmpp.disconnect())

    xmpp.connect((host, port), use_tls=use_tls)
    xmpp.process(block=True)
