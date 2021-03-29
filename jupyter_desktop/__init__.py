import os
import shlex
from shutil import which
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))

def setup_desktop():
    sockets_dir = tempfile.mkdtemp()
    sockets_path = os.path.join(sockets_dir, 'vnc-socket')

    vnc_args = [
        'vncserver',
        '-rfbunixpath', sockets_path,
    ]
    socket_args = [
        '--unix-target', sockets_path
    ]

    vnc_command = ' '.join(shlex.quote(p) for p in (vnc_args + [
        '-verbose',
        '-xstartup', os.path.join(HERE, 'xstartup'),
        '-geometry', '1680x1050',
        '-SecurityTypes', 'None',
        '-fg',
        ':1',
    ]))
    return {
        'command': [
            'websockify', '-v',
            '--web', '/usr/share/novnc/',
            '--heartbeat', '30',
            '45605',
        ] + socket_args + [
            '--',
            '/bin/sh', '-c',
            f'cd {os.getcwd()} && {vnc_command}'
        ],
        'port': 45605,
        'timeout': 30,
        'mappath': {'/': '/vnc_lite.html'},
        'new_browser_window': True
    }
