import json
import os
import gzip
import logging

from datetime import datetime
from collections import defaultdict

from app.constants import Constants


class Statistic:
    def __init__(self):
        self.__data, self.__loaded_files = self.__upload_data()

    def __upload_data(self):
        with open(Constants.DATA, "rb") as f:
            try:
                return json.load(f)
            except EOFError:
                logging.warning(f'{Constants.DATA} file is empty. Pickle can\'t read data.')
                return defaultdict(list), set()

    def __save_data(self):
        with open(Constants.DATA, "wb") as f:
            json.dump((self.__data, self.__loaded_files), f)

    def __upload_file(self, file):
        with gzip.open(file, 'rt', encoding='utf-8') as f:
            lines = f.readlines()

        date = datetime.strptime(file[5:15], '%Y-%m-%d')

        for line in lines:
            if 'joined' in line or 'left' in line:
                time = datetime.strptime(line[1:9], '%H:%M:%S')
                nickname, state, *_ = line[33:].split()

                if nickname in Constants.NORMAL_PLAYERS:
                    self.__data[nickname].append((datetime.combine(date.date(), time.time()), state))

    def upload_new_files(self):
        for file in os.listdir(Constants.LOGS_DIR):
            if (
                    os.path.isfile(os.path.join(Constants.LOGS_DIR, file)) and
                    file.endswith('log.gz') and
                    file not in self.__loaded_files
            ):
                filepath = os.path.join(Constants.LOGS_DIR, file)
                self.__upload_file(filepath)
                self.__loaded_files.add(filepath)

        self.__save_data()
        return [1, 0]

    def calculate_by_period(self, begin_date, end_date):
        for nickname, logs in self.__data:
            pass
