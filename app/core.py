import json
import os
import gzip
import logging

from datetime import datetime
from collections import defaultdict

from app.constants import Constants


class Statistics:
    def __init__(self):
        self.__data, self.__loaded_files = self.__upload_data()

    def __upload_data(self):
        with open(Constants.DATA) as f:
            try:
                return json.load(f)
            except json.decoder.JSONDecodeError:
                logging.warning(f'{Constants.DATA} file is empty. Json can\'t read data.')
                return defaultdict(list), set()

    def __save_data(self):
        with open(Constants.DATA, "w") as f:
            json.dump((self.__data, self.__loaded_files), f, indent=4, sort_keys=True, default=str)

    def __upload_file(self, file):
        with gzip.open(file, 'rt', encoding='utf-8') as f:
            lines = f.readlines()

        date = datetime.strptime(file[5:15], Constants.DATE_FORMAT)

        for line in lines:
            if 'joined' in line or 'left' in line:
                time = datetime.strptime(line[1:9], Constants.DAY_FORMAT)
                nickname, state, *_ = line[33:].split()

                if nickname in Constants.NORMAL_PLAYERS:
                    self.__data[nickname].append((datetime.combine(date.date(), time.time()), state))

        return date.strftime(Constants.DATE_FORMAT)

    def upload_new_files(self):
        new_dates = set()

        for file in os.listdir(Constants.LOGS_DIR):
            if (
                    os.path.isfile(os.path.join(Constants.LOGS_DIR, file)) and
                    file.endswith('log.gz') and
                    file not in self.__loaded_files
            ):
                filepath = os.path.join(Constants.LOGS_DIR, file)
                date = self.__upload_file(filepath)
                new_dates.add(date)
                self.__loaded_files.add(filepath)

        self.__save_data()
        return new_dates

    def calculate_by_period(self, begin_date, end_date):
        for nickname, logs in self.__data.items():
            pass

        return {}
