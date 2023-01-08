from libs.recog_img import ImageRecognition
from libs.operate_obs import OBS
import numpy as np
import cv2
import configparser

is_turned_on = True
phase = 0
"""phaseの定義
0:不明
1:マッチング中
2:マッチング完了
3:選出中
4:選出完了
5:対戦開始
6:勝敗画面
"""
recog = ImageRecognition()

config = configparser.ConfigParser()
config.read('./pokemon_sv_vs_support/python/asset/setting.ini', encoding='utf-8')
PHASE_1 = 'matching'
PHASE_2 = 'selecting'
PHASE_3 = 'vs'
PHASE_4 = 'result'
X = 'left'
DX = 'width'
Y = 'top'
DY = 'height'

TRIM_PLACE = {
    1:{
        'x':int(config[PHASE_1][X]),
        'dx':int(config[PHASE_1][DX]),
        'y':int(config[PHASE_1][Y]),
        'dy':int(config[PHASE_1][DY]),
    },
    2:{
        'x':int(config[PHASE_2][X]),
        'dx':int(config[PHASE_2][DX]),
        'y':int(config[PHASE_2][Y]),
        'dy':int(config[PHASE_2][DY]),
    },
    3:{
        'x':int(config[PHASE_3][X]),
        'dx':int(config[PHASE_3][DX]),
        'y':int(config[PHASE_3][Y]),
        'dy':int(config[PHASE_3][DY]),
    },
    4:{
        'x':int(config[PHASE_4][X]),
        'dx':int(config[PHASE_4][DX]),
        'y':int(config[PHASE_4][Y]),
        'dy':int(config[PHASE_4][DY]),
    }
}

IMG_BATTLING = cv2.imread('./pokemon_sv_vs_support/python/asset/temp_png/battling.png')
IMG_MATCHING = cv2.imread('./pokemon_sv_vs_support/python/asset/temp_png/matching.png')
IMG_FOUND_ENEMY = cv2.imread('./pokemon_sv_vs_support/python/asset/temp_png/found_enemy.png')
IMG_SELECTING = cv2.imread('./pokemon_sv_vs_support/python/asset/temp_png/selecting.png')
IMG_WIN = cv2.imread('./pokemon_sv_vs_support/python/asset/temp_png/win.png')
IMG_LOSE = cv2.imread('./pokemon_sv_vs_support/python/asset/temp_png/lose.png')

def update_phase(img:np.ndarray, phase:int)->int:
    """フェーズごとの処理を行い、フェーズを更新する。"""
    if phase == 0 or phase == 1:
        img = recog.trim(img, TRIM_PLACE[1]['x'], TRIM_PLACE[1]['dx'], TRIM_PLACE[1]['y'], TRIM_PLACE[1]['dy'])
        if recog.is_matched(img, IMG_MATCHING):
            return 2
    elif phase == 2:
        img = recog.trim(img, TRIM_PLACE[1]['x'], TRIM_PLACE[1]['dx'], TRIM_PLACE[1]['y'], TRIM_PLACE[1]['dy'])
        if recog.is_matched(img, IMG_FOUND_ENEMY):
            #順位認識を行う。
            return 3
    elif phase == 3:
        img = recog.trim(img, TRIM_PLACE[2]['x'], TRIM_PLACE[2]['dx'], TRIM_PLACE[2]['y'], TRIM_PLACE[2]['dy'])
        if recog.is_matched(img, IMG_SELECTING):
            #ポケモン認識処理を行う
            return 4
    elif phase == 4:
        img = recog.trim(img, TRIM_PLACE[3]['x'], TRIM_PLACE[3]['dx'], TRIM_PLACE[3]['y'], TRIM_PLACE[3]['dy'])
        if recog.is_matched(img, IMG_BATTLING):
            #時間測定開始する。
            return 5
    elif phase == 5:
        img = recog.trim(img, TRIM_PLACE[4]['x'], TRIM_PLACE[4]['dx'], TRIM_PLACE[4]['y'], TRIM_PLACE[4]['dy'])
        if recog.is_matched(img, IMG_WIN, 0.8):
            #勝利時処理
            return 1
        elif recog.is_matched(img, IMG_LOSE, 0.8):
            #敗北時処理
            return 1

def recog_pokemon():
    pass