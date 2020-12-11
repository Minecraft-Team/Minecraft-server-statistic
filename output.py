# name_list - массив, содержащий строки, вида:
#       [nickname, time_total, sum_total] - никнейм, количество проведённого времени и итоговая сумма

import requests
from xml.etree.ElementTree import fromstring, ElementTree


def beautiful_output(name_list, days_count):
    output_line = "Statistic for the last " + str(days_count) + " days:\n\n"
    max_nick_length = len("Nickname")
    max_time_length = len("Time Total")
    max_sum_usd_length = len("Sum Total USD")

    currency = get_currency()

    for person in name_list:
        max_nick_length = max(max_nick_length, len(person) + 1)
        max_time_length = max(max_time_length, len(str(name_list[person][0])))
        max_sum_usd_length = max(max_sum_usd_length, len(str(name_list[person][1])))

    output_line += "     Nickname" + " " * (max_nick_length - len("Nickname")) + " | " + \
                   "Time Total" + " " * (max_time_length - len("Time Total")) + " | " + \
                   "Sum Total USD" + " " * (max_sum_usd_length - len("Sum Total USD")) + " | " + \
                   "Sum Total USSR\n"

    for person in name_list:
        cur_nick_length = len(person)
        cur_time_length = len(str(name_list[person][0]))
        cur_sum_usd_length = len(str(name_list[person][1]))

        diff_nick = max_nick_length - cur_nick_length
        diff_time = max_time_length - cur_time_length
        diff_sum_usd = max_sum_usd_length - cur_sum_usd_length

        sum_ussr = name_list[person][1] * currency
        output_line += "   - " + str(person) + " " * diff_nick + " | " + \
                       str(name_list[person][0]) + " " * diff_time + " | " + \
                       str(name_list[person][1]) + " $" + " " * (diff_sum_usd - 2) + " | " + \
                       str(sum_ussr) + ' \u20BD' + "\n"

    return output_line


def get_currency():
    URL = "http://www.cbr.ru/scripts/XML_daily.asp"

    r = requests.get(url=URL)

    tree = ElementTree(fromstring(r.content))

    currency_usd = 0

    for leaf in tree.getroot():
        if leaf.attrib['ID'] == 'R01235':
            for i in leaf:
                if i.tag == "Value":
                    currency_usd = float(i.text.replace(',', '.'))

    return currency_usd
