# ELO
# python 3.4.3
import math
import csv
import json
import os
import shutil
from sys import argv
from datetime import datetime
from django.utils.encoding import smart_str, smart_unicode
from operator import itemgetter
from elo_classes import *

# Background information - https://en.wikipedia.org/wiki/Elo_rating_system
# Based on this equation - http://elo-norsak.rhcloud.com/index.php

_MAXSIZE = 186
_MINBUFFEREDELO = 1900
_MAXBUFFEREDELO = 3200
_YMAX = 4.4
_BASE = 1
_BUFFEREDELOSLOPE = -.14 / 1300
_EXPODENTIALRATE = 800
_WIN = 1.0
_LOSS = 0.0


def calculateElo(players):
    N = len(players)
    # compare every head to head matchup in given meet
    for i in players:
        # changing K multiplier depending on the size of race
        # K multiplier is maximum amount points that can be gained from a win
        if N > _MAXSIZE:
            K = 1.2
        else:
            k_slope = 3 * N / 175
            K = _YMAX - k_slope
        # chaning K multiplier depending on elo of runner
        multi = 1
        if i.elo > _MINBUFFEREDELO and i.elo < _MAXBUFFEREDELO:
            multi = _BASE + (_BUFFEREDELOSLOPE) * (i.elo - _MINBUFFEREDELO)
        K = multi * K
        for j in players:
            if i is not j:
                # S is the player's score - 1 for win - 0 for loss
                if i.place < j.place:
                    S = _WIN
                else:
                    S = _LOSS
                change = j.elo - i.elo
                # EA is the expected probability of player winning
                EA = 1 / (1.0 + math.pow(10.0, (change) / _EXPODENTIALRATE))
                i.elo += K * (S - EA)
        # making it so zero is floor of elo rating
        if i.elo < 0:
            i.elo = 0
