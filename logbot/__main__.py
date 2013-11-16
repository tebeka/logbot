from logbot.common import create_cfg_dirs, run_thread, register_listener
from logbot import log, httpd, bot, search, __version__

from pytz import timezone, UnknownTimeZoneError

from getpass import getuser, getpass


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='Jabber Log Bot')
    parser.add_argument('--user', help='jabber user', default=None)
    parser.add_argument('--passwd', help='jabber password', default=None)
    parser.add_argument('--host', help='jabber host', default='localhost')
    parser.add_argument('--port', help='jabber port', default=5222, type=int)
    parser.add_argument('--no-tls', help='do not use tls', dest='use_tls',
                        action='store_false', default=True)
    parser.add_argument('room', help='room to log')  # FIXME: Rooms
    parser.add_argument('--version', action='version',
                        version='logbot {}'.format(__version__))
    parser.add_argument('--timezone', help='time zone', default=None)

    args = parser.parse_args(argv[1:])

    if args.timezone:
        try:
            tz = timezone(args.timezone)
        except UnknownTimeZoneError:
            raise SystemExit(
                'error: unknown timezone - {}'.format(args.timezone))
    else:
        tz = None

    create_cfg_dirs()

    user = args.user or getuser()
    passwd = args.passwd or getpass()

    register_listener(log.log)
    register_listener(search.index)

    run_thread(httpd.run)
    bot.run(args.host, args.port, user, passwd, args.room, args.use_tls, tz)


if __name__ == '__main__':
    main()
