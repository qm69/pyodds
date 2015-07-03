#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import UserDict
from datetime import datetime
# from logger import log_db


class Match(UserDict):
    """docstring for Match @ v0.4.142 {
        'league': 'lega-a',
        'xeid': 'tGwcHwNl',
        'season': '2014-2015',
        'link': '/basketball/italy/lega-a/venezia-sassari-tGwcHwNl/',
        'sport': 'basketball',
        'score': {
            'quat': ['19:21, 19:23, 22:10, 23:29, 7:17'],
            'ot': True,
            'full': '90:100',
            'main': '83:83'},
        'country': 'italy',
        'seas_type': 'season',
        'date': {
            'scraptime': '2015-07-01 22:36',
            'timestamp': 1402448400,
            'datetime': '04-01-15 04:00',
            'time': '04:00',
            'date': '11 Jun 2014'},
        'home': {
            'team': 'Venezia',
            'ftot': {
                'delta': [1, -13.5, 24.5, 5.5],
                'profit': [54, 90, 92, 89],
                'resalt': [False, -10, 190, 90]},
            'frst': {
                'delta': [1, -13.5, 24.5, 5.5],
                'profit': [54, 90, 92, 89],
                'resalt': [False, -10, 190, 90]}},
        'away': {
            'team': 'Sassari',
            'ftot': {
                'delta': [-1, 13.5, 24.5, 18.5],
                'profit': [100, -100, 92, 89],
                'resalt': [True, 10, 190, 100]},
            'frst': {
                'delta': [-1, 13.5, 24.5, 18.5],
                'profit': [100, -100, 92, 89],
                'resalt': [True, 10, 190, 100]}}
    }"""

    def __init__(self, dd):
        """ dd as dict_data {
            'teams': ['Venezia', 'Sassari'],
            'link': '/basketball/italy/lega-a/venezia-sassari-tGwcHwNl/',
            'xeid': 'tGwcHwNl',
            'xhash': 'yjc0b',
            'meta': {
                'season': '2014-2015',
                'league': 'lega-a',
                'country': 'italy',
                'sport': 'basketball',
                'seas_type': 'season'},
            'score': {
                'quat': ['19:21, 19:23, 22:10, 23:29, 7:17'],
                'full': '90:100',
                'main': '83:83',
                'ot': True},
            'date': {
                'date': '11 Jun 2014',
                'time': '04:00',
                'datetime': '04-01-15 04:00',
                'timestamp': 1402448400},
            'odds': {
                'hand': {
                    'ftot': {
                        'close': [1.9, 1.88],
                        'mean': [1.9, 1.88],
                        'open': [1.89, 1.89],
                        'value': [-3.5, 3.5]},
                    'frst': {
                        'close': [1.87, 1.88],
                        'mean': [1.87, 1.89],
                        'open': [1.86, 1.9],
                        'value': [-1.5, 1.5]}},
                'line': {
                    'ftot': {
                        'close': [1.58, 2.29],
                        'mean': [1.56, 2.33],
                        'open': [1.55, 2.36]},
                    'frst': {
                        'close': [1.64, 2.14],
                        'mean': [1.62, 2.17],
                        'open': [1.61, 2.19]}},
                'totl': {
                    'ftot': {
                        'close': [1.84, 1.92],
                        'mean': [1.85, 1.92],
                        'open': [1.85, 1.91],
                        'value': [165.5, 165.5]},
                    'frst': {
                        'close': [1.87, 1.87],
                        'mean': [1.88, 1.86],
                        'open': [1.88, 1.85],
                        'value': [82.5, 82.5]}}}
        """

        self.data = {'home': {'ftot': {}, 'frst': {}},
                     'away': {'ftot': {}, 'frst': {}}}

        self.update(dd['meta'])
        self['link'] = dd['link']
        self['xeid'] = dd['xeid']
        self['date'] = dd['date']
        self['score'] = dd['score']
        self['odds'] = dd['odds']  # может в каждую команду отдельно???

        self['date']['scraptime'] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self['home']['team'], self['away']['team'] = dd['teams']
        self['home']['tid'], self['away']['tid'] = dd['tids']

        # counting Full Time & Over Time
        once_scrd = self.count_result(dd['score']['full'])
        (self['home']['ftot']['resalt'],
         self['away']['ftot']['resalt']) = once_scrd

        scor = [int(s) for s in dd['score']['full'].split(':')]
        line = self.count_line(scor, dd['odds']['line']['ftot'])
        hand = self.count_handy(scor, dd['odds']['hand']['ftot'])
        totl = self.count_total(scor, dd['odds']['totl']['ftot'])
        itot = self.count_i_tot(scor, dd['odds']['itot']['ftot'])

        # делает срезы из массивов 1й дельта, а 2й прибыль
        self['home']['ftot']['delta'], self['away']['ftot']['delta'] = [
            [line[0][n], hand[0][n], totl[0][n], itot[0][n]] for n in range(0, 2)]

        self['home']['ftot']['profit'], self['away']['ftot']['profit'] = [
            [line[1][n], hand[1][n], totl[1][n], itot[1][n]] for n in range(0, 2)]

        """ counting First Half if Odds exist
        if dd['odds']['line']['frst']:
            line = self.count_line()
            hand = self.count_handy()
            totl = self.count_total()
            itot = self.count_i_tot()

            once_scrd = self.count_result(dd['score']['full'])
            (self['home']['frst']['resalt'],
             self['away']['frst']['resalt']) = once_scrd

            self['home']['frst']['delta'], self['away']['frst']['delta'] = [
                [line[0][n], hand[0][n], totl[0][n], itot[0][n]] for n in range(0, 2)]

            self['home']['frst']['profit'], self['away']['frst']['profit'] = [
                [line[1][n], hand[1][n], totl[1][n], itot[1][n]] for n in range(0, 2)]
        """

    def count_result(self, score):
        """
        Возвращает результат в очках для каждой команды

        Arguments: score @ str: '90:100'

        Return: [ [True, 14, 210, 112], [False, -14, 210, 98]]
        """
        score = [int(s) for s in score.split(':')]  # [90, 100]
        reslt = [True, False] if score[0] > score[1] else [False, True]
        handy = [score[0] - score[1], score[1] - score[0]]
        total = sum(score)

        return [[reslt[n], handy[n], total, score[n]] for n in range(0, 2)]
        """
        return [[reslt[0], handy[0], total, score[0]],
                [reslt[1], handy[1], total, score[1]]]
        except Exception:
            log_db.exception('From count_totl')
        """

    def count_line(self, score, odds):
        """ Подсчет результата матча & профит:
                    выиграл проигр
            равный      1    -1
            фаворит     2    -2
            аутсайдер   3    -3

            Arguments:
                score: [90, 100]
                odds: [1.54, 2.25]
            Return: [[1, 54], [-1, -100]]
        """
        home_win = True if score[0] > score[1] else False
        delta, profit = [], []

        # подсчет результатов
        if abs(sum(score)) <= 0.1:
            delta = [3, -3] if home_win else [-3, 3]
        else:
            if odds['mean'][0] < odds['mean'][1]:
                delta = [1, -2] if home_win else [-1, 2]
            else:
                delta = [2, -1] if home_win else [-2, 1]

        # подсчет прибыли
        if home_win:
            profit = [int((odds['mean'][0] - 1) * 100), -100]
        else:
            profit = [-100, int((odds['mean'][1] - 1) * 100)]

        return [delta, profit]

    def count_handy(self, score, handy):
        """
        Считает дельту по форе & профит:
        Return:
            (7.5, -7.5)
        """
        delta = [self['home']['ftot']['resalt'][1] + handy['value'][0],
                 self['away']['ftot']['resalt'][1] + handy['value'][1]]

        # подсчет прибыли
        if delta[0] > delta[1]:
            profit = [int((handy['mean'][0] - 1) * 100), -100]
        else:
            profit = [-100, int((handy['mean'][1] - 1) * 100)]

        return [delta, profit]

    def count_total(self, score, total):
        """ Считатет дельту тотала & профит """
        delta = self['home']['ftot']['resalt'][2] - total['value'][0]

        # подсчет прибыли
        if delta > 0:
            profit = int((total['mean'][0] - 1) * 100)
        else:
            profit = -100

        return [[delta, delta], [profit, profit]]

    def count_i_tot(self, score, itot):
        """ Считатет инд. тотал & профит """
        delta = [self['home']['ftot']['resalt'][3] - itot['value'][0],
                 self['away']['ftot']['resalt'][3] - itot['value'][1]]

        profit = [int((itot['mean'][0] - 1) * 100) if delta[0] > 0 else -100,
                  int((itot['mean'][1] - 1) * 100) if delta[1] > 0 else -100]

        return [delta, profit]

if __name__ == '__main__':
    base = {
        'teams': ['Toronto Blue Jays', 'Boston Red Sox'],
        'link': '/baseball/usa/mlb/toronto-blue-jays-boston-red-sox-4G79dfXC/',
        'xhash': 'yj17d',
        'xeid': '4G79dfXC',
        'meta': {
            'season': '2015',
            'seas_type': 'season',
            'sport': 'baseball',
            'country': 'usa',
            'league': 'mlb'},
        'date': {
            'timestamp': 1435770420,
            'date': '01 Jul 2015',
            'datetime': '01-07-15 20:07',
            'time': '20:07'},
        'score': {
            'full': '11:2',
            'ot': False,
            'quat': '5:0, 2:0, 1:0, 0:0, 0:0, 1:0, 0:1, 2:1, X:0',
            'main': ''},
        'odds': {
            'itot': {
                'ftot': {
                    'mean': [1.89, 1.89],
                    'value': [4.5, 3.5]}},
            'totl': {
                'ftot': {
                    'value': [8.5, 8.5], 'mean': [1.86, 1.94],
                    'open': [1.83, 1.98], 'close': [1.9, 1.9]},
                'frst': {
                    'value': [4.5, 4.5], 'mean': [1.88, 1.92],
                    'open': [1.87, 1.93], 'close': [1.88, 1.92]}
            },
            'line': {
                'ftot': {
                    'open': [1.67, 2.2],
                    'close': [1.68, 2.18],
                    'mean': [1.67, 2.19]},
                'frst': {
                    'open': [1.66, 2.27],
                    'close': [1.68, 2.23],
                    'mean': [1.67, 2.25]}
            },
            'hand': {
                'ftot': {
                    'value': [-1.5, 1.5], 'mean': [2.37, 1.6],
                    'open': [2.34, 1.61], 'close': [2.39, 1.59]},
                'frst': {
                    'value': [-0.5, 0.5], 'mean': [1.92, 1.85],
                    'open': [1.92, 1.89], 'close': [1.92, 1.82]}
            }
        }
    }
    m = Match(base)
    print(m)
