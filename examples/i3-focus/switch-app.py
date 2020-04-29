#!/usr/bin/env python3

import re
import sys
from argparse import ArgumentParser
from functools import reduce
import i3ipc
from tools import App, Lists, Menu, Sockets

parser = ArgumentParser(prog='switch-current-app-window.py',
                        description='''
        switch-current-app-window.py is dmenu-based script for creating dynamic app switcher.
        ''',
                        epilog='''
        Additional arguments found after "--" will be passed to dmenu.
        ''')
parser.add_argument('--socket-file', default='/tmp/i3-focus-history-server.socket', help='Socket file path')
(args, menu_args) = parser.parse_known_args()

sockets = Sockets(args.socket_file)
containers_info = sockets.get_containers_history()

apps = list(map(App, containers_info))
apps_uniq = reduce(Lists.accum_uniq_apps, apps, [])

if len(apps_uniq) < 2:
    sys.exit()

prev_app = apps_uniq[1]

i3 = i3ipc.Connection()
i3.command("[con_id=\"%s\"] focus" % prev_app.get_con_id())
