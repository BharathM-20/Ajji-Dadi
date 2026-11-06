"""Provision local invited accounts; passwords are entered privately, never CLI arguments."""

import argparse
import getpass
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.accounts import DEFAULT_DB, AccountStore  # noqa: E402


class PrivateArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # argparse normally echoes invalid arguments, which could include a pasted password.
        super().error('Invalid options. Use --help; passwords belong only in hidden prompts.')


def main(argv=None):
    parser = PrivateArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, default=DEFAULT_DB)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--add', metavar='USERNAME')
    group.add_argument('--seed-demo', type=int, metavar='COUNT')
    args = parser.parse_args(argv)
    try:
        store = AccountStore(args.database)
        if args.add:
            password = getpass.getpass('New password (12–128 characters): ')
            if not 12 <= len(password) <= 128:
                raise ValueError('Password must contain12–128 characters; no account created.')
            if password != getpass.getpass('Confirm password: '):
                raise ValueError('Passwords did not match; no account created.')
            store.create_user(args.add, password)
            print('Invited account created. Use your chosen username and password to sign in.')
        else:
            store.seed_demo(args.seed_demo)
            print(f'Disabled synthetic demo accounts prepared. Total rows: {store.count()}.')
        return 0
    except ValueError as exc:
        # These validation messages are fixed strings and never contain supplied passwords.
        print(f'ERROR: account setup failed. WHY: {exc} '
              'FIX: correct the stated issue and rerun; existing accounts are preserved.')
        return 1
    except EOFError:
        print('ERROR: password entry interrupted. WHY: no terminal input was available. '
              'FIX: rerun in your terminal and enter the password at both hidden prompts.')
        return 1
    except (OSError, sqlite3.Error):
        print('ERROR: account database unavailable. WHY: file access or database operation failed. '
              'FIX: check write access to data/accounts.sqlite3 and rerun; do not delete it.')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
