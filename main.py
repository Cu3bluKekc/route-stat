#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
from os.path import join as os_join
import signal
from datetime import datetime
import argparse
from selenium.webdriver import PhantomJS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import unicodecsv as csv

PATH = os.path.dirname(os.path.realpath(__file__))
DEFAULT_PHANTOMJS = os_join(
    PATH, 'node_modules', 'phantomjs', 'lib', 'phantom', 'bin', 'phantomjs'
)
FULLHD = (1920, 1080, )
DEFAULT_YA_CLASS = 'route-view_driving__route-title-text'
DESCRIPTION = """
    Ходит в яндекс карты по ссылке и сохраняет первый результат по маршрутам
"""


def is_class_exist(class_name):
    return EC.presence_of_element_located((By.CLASS_NAME, class_name))


class RouteStatistic(object):

    def __init__(self, url, phantomjs=None, resolution=None, ya_class=None,
                 screen_path=None, screen_pattern=None, csv_path=None):
        self.url = url

        self.phantomjs = phantomjs or DEFAULT_PHANTOMJS
        assert os.path.isfile(self.phantomjs), "phantomjs не найден"

        resolution = resolution or FULLHD
        assert isinstance(resolution, (list, tuple))
        assert len(resolution) == 2

        self.ya_class = ya_class or DEFAULT_YA_CLASS
        self.screen_path = screen_path or PATH

        self.screen_pattern = screen_pattern or '%s.png'
        assert '%s' in self.screen_pattern

        self.csv_path = csv_path or os_join(PATH, 'statistic.csv')

        self.driver = PhantomJS(self.phantomjs)
        self.driver.set_window_size(*resolution)

    def track(self):
        self.driver.get(self.url)
        WebDriverWait(self.driver, 5).until(is_class_exist(self.ya_class))
        time = self.driver.find_element_by_class_name(self.ya_class).text
        now = datetime.now()
        self._save_screenshot(now)
        self._update_file(now, *[t.strip() for t in time.split(',')])

    def _save_screenshot(self, now):
        if '%s' in self.screen_pattern:
            file_name = self.screen_pattern % (now, )
        else:
            file_name = self.screen_pattern
        file_name = os_join(self.screen_path, file_name)
        self.driver.save_screenshot(file_name)

    def _update_file(self, now, time, distance):
        with open(self.csv_path, 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=str('\t'))
            writer.writerow([now, time, distance, ])

    def __call__(self):
        return self.track()

    def __del__(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.service.process.send_signal(signal.SIGTERM)
            self.driver.quit()


def arguments():
    readme_md = os_join(PATH, 'README.md')
    if os.path.isfile(readme_md):
        with open(readme_md, 'r') as f:
            description = f.read().decode("utf-8")
    else:
        description = DESCRIPTION

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--url', help='Ссылка на маршрут', required=True)
    parser.add_argument('--phantomjs', default=DEFAULT_PHANTOMJS,
                        help='Путь к phantomjs')
    parser.add_argument('--resolution', '-r', type=int, default=FULLHD,
                        help='Разрешение скриншота')
    parser.add_argument('--ya_class', default=DEFAULT_YA_CLASS,
                        help="""Название класса DOM элемента из которого
                        возьмётся время и дистанция""")
    parser.add_argument('--screen_path', help="Путь к папке со скриншотами")
    parser.add_argument('--screen_pattern', help="Паттерн названия скриншотов")
    parser.add_argument('--csv_path', help="Путь к csv файлу со статистикой")

    args = parser.parse_args()
    return args.__dict__


if __name__ == '__main__':
    RouteStatistic(**arguments())()
