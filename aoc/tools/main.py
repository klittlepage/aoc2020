import argparse
import pathlib
import os

import requests

from dotenv import load_dotenv
load_dotenv()


def fetch(args):
    resp = requests.get(f"https://adventofcode.com/{args.year}/day/{args.day}/"
                        "input", cookies={'session': args.session_cookie})

    if 200 <= resp.status_code < 300:
        output_dir = pathlib.Path(os.path.join(args.root_dir,
                                               f"d{args.day:02d}"))
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir.joinpath('input.txt')
        with open(output_path, 'w', encoding='utf8') as output_file:
            output_file.write(resp.text)
    else:
        print(f"got a bad status: {resp.status_code}")


def main():
    def valid_year(arg):
        year = int(arg)

        if 2015 <= year <= 2020:
            return year

        raise ValueError

    def valid_day(arg):
        day = int(arg)
        if 1 <= day <= 25:
            return day

        raise ValueError

    def valid_output_directory(arg):
        pathlib.Path(arg).mkdir(parents=True, exist_ok=True)
        return arg

    parser = argparse.ArgumentParser(prog='aoc_tools')
    subparsers = parser.add_subparsers(help='aoc tool command')
    fetch_cmd = subparsers.add_parser('fetch', help='a help')
    fetch_cmd.add_argument('--session-cookie', type=str,
                           default=os.environ.get('AOC_SESSION_COOKIE'))
    fetch_cmd.add_argument('--root-dir', type=valid_output_directory,
                           default='data', help='the root output directory')
    fetch_cmd.add_argument('year', type=valid_year)
    fetch_cmd.add_argument('day', type=valid_day)
    fetch_cmd.set_defaults(func=fetch)

    args = parser.parse_args()
    args.func(args)
