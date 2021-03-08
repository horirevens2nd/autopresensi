#!/usr/bin/env pipenv-shebang
from presensi import login_app

if __name__ == '__main__':
    login_app(action='check_in')
