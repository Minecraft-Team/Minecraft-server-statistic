import os
import sys
import argparse
import logging
from datetime import datetime

from app.constants import Constants
from app.core import Statistics
from app.formatting import beautiful_output
from app.vk_bot import VkBotServerStatistics


def create_parser():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument
    date_validator = lambda date: datetime.strptime(date, Constants.DATE_FORMAT)

    _('--begin', type=date_validator, default=None, help='Begin statistic date')
    _('--end', type=date_validator, default=None, help='End statistic date')
    _('--last', action='store_true', help='Calculate statistic for not calculated period')

    return parser


def check_args(args):
    if args.last == False:
        if None in (args.begin, args.end):
            raise ValueError("'begin' or 'end' argument is empty")
        if not args.begin <= args.end:
            raise ValueError("'begin' date must be <= 'end'")


def check_files():
    if not os.path.isdir(Constants.LOGS_DIR):
        raise ValueError("Incorrect path to logs directory")

    if not os.path.isfile(Constants.DATA):
        open(Constants.DATA, "w").close()

    logging.warning('All paths are correct')


def main():
    try:
        parser = create_parser()
        args = parser.parse_args()
        check_args(args)
        check_files()

        statistic = Statistics()
        dates = statistic.upload_new_files()

        if args.last:
            begin_date, end_date = min(dates), max(dates)
        else:
            begin_date, end_date = args.begin, args.end

        stats = statistic.calculate_by_period(begin_date, end_date)
        print(beautiful_output(stats, f'{begin_date} {end_date}'))
        # VkBotServerStatistics().send_statistics(beautiful_output(stats, f'{begin_date} {end_date}'))

    except Exception:
        logging.exception("Something was broken")

    return 0


if __name__ == '__main__':
    sys.exit(main())
