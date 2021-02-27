#!/usr/bin/env pipenv-shebang
from presensi import Presensi

if __name__ == '__main__':
    presensi = Presensi()
    presensi.login_app(action='check_in')
