from libs.recog_img import ImageRecognition
from libs.operate_obs import OBS
from libs.spreadsheet import SpreadSheet
import numpy as np
import cv2
import configparser
import glob
import os
import pandas as pd
import datetime
import logging
import logging.config

recog = ImageRecognition()

config = configparser.ConfigParser()
config.read("./pokemon_sv_vs_support/python/asset/setting.ini", encoding="utf-8")

logging.config.fileConfig("./pokemon_sv_vs_support/python/asset/logging.ini")
logger_stream = logging.getLogger("stream")
PHASE_1 = "matching"
PHASE_2 = "selecting"
PHASE_3 = "vs"
PHASE_4 = "result"
SELECTING_ENEMY_TEAM = "selecting_enemy_team"
POKEMON_PLACE = "pokemon"
ACTION = "action"
ENEMY_LEVEL = "enemy_level"
MY_LEVEL = "my_level"
X = "left"
DX = "width"
Y = "top"
DY = "height"

# 画像認識の範囲を外部ファイルで設定できるようにするため、iniファイルを利用。
TRIM_PLACE = {
    1: {
        "x": int(config[PHASE_1][X]),
        "dx": int(config[PHASE_1][DX]),
        "y": int(config[PHASE_1][Y]),
        "dy": int(config[PHASE_1][DY]),
    },
    2: {
        "x": int(config[PHASE_2][X]),
        "dx": int(config[PHASE_2][DX]),
        "y": int(config[PHASE_2][Y]),
        "dy": int(config[PHASE_2][DY]),
    },
    3: {
        "x": int(config[PHASE_3][X]),
        "dx": int(config[PHASE_3][DX]),
        "y": int(config[PHASE_3][Y]),
        "dy": int(config[PHASE_3][DY]),
    },
    4: {
        "x": int(config[PHASE_4][X]),
        "dx": int(config[PHASE_4][DX]),
        "y": int(config[PHASE_4][Y]),
        "dy": int(config[PHASE_4][DY]),
    },
    "selecting_enemy_team": {
        "x": int(config[SELECTING_ENEMY_TEAM][X]),
        "dx": int(config[SELECTING_ENEMY_TEAM][DX]),
        "y": int(config[SELECTING_ENEMY_TEAM][Y]),
        "dy": int(config[SELECTING_ENEMY_TEAM][DY]),
    },
    "pokemon": {
        "x": int(config[POKEMON_PLACE][X]),
        "dx": int(config[POKEMON_PLACE][DX]),
        "y": int(config[POKEMON_PLACE][Y]),
        "dy": int(config[POKEMON_PLACE][DY]),
    },
    "actions": {
        "x": int(config[ACTION][X]),
        "dx": int(config[ACTION][DX]),
        "y": int(config[ACTION][Y]),
        "dy": int(config[ACTION][DY]),
    },
    "enemy_level": {
        "x": int(config[ENEMY_LEVEL][X]),
        "dx": int(config[ENEMY_LEVEL][DX]),
        "y": int(config[ENEMY_LEVEL][Y]),
        "dy": int(config[ENEMY_LEVEL][DY]),
    },
    "my_level": {
        "x": int(config[MY_LEVEL][X]),
        "dx": int(config[MY_LEVEL][DX]),
        "y": int(config[MY_LEVEL][Y]),
        "dy": int(config[MY_LEVEL][DY]),
    },
}

THRESHOLD_MATCHING = float(config["threshold"]["matching"])
THRESHOLD_FOUND_ENEMY = float(config["threshold"]["found_enemy"])
THRESHOLD_SELECTING = float(config["threshold"]["selecting"])
THRESHOLD_POKEMON = float(config["threshold"]["pokemon"])
THRESHOLD_BATTLING = float(config["threshold"]["battling"])
THRESHOLD_WIN = float(config["threshold"]["win"])
THRESHOLD_LOSE = float(config["threshold"]["lose"])
THRESHOLD_ACTION = float(config["threshold"]["action"])
THRESHOLD_LEVEL = float(config["threshold"]["level"])

PORT = int(config["obs"]["port"])
PASSWORD = config["obs"]["pass"]
SOURCE = config["obs"]["source"]
TIME_SOURCE = config["obs"]["time_source"]

TIMER_ENABLED = config.getboolean("feature_enabled", "timer")
ACTION_LOG_ENABLED = config.getboolean("feature_enabled", "action_log")

IMG_MATCHING = cv2.imread("./pokemon_sv_vs_support/python/asset/temp_png/matching.png")
IMG_FOUND_ENEMY = cv2.imread(
    "./pokemon_sv_vs_support/python/asset/temp_png/found_enemy.png"
)
IMG_SELECTING = cv2.imread(
    "./pokemon_sv_vs_support/python/asset/temp_png/selecting.png"
)
IMG_BATTLING = cv2.imread("./pokemon_sv_vs_support/python/asset/temp_png/battling.png")
IMG_WIN = cv2.imread("./pokemon_sv_vs_support/python/asset/temp_png/win.png")
IMG_LOSE = cv2.imread("./pokemon_sv_vs_support/python/asset/temp_png/lose.png")

POKE_PING_FILES = glob.glob("./pokemon_sv_vs_support/python/asset/poke_png/*.png")
ID = pd.read_csv("./pokemon_sv_vs_support/python/asset/poke_id.csv")

IMG_ACTION_1 = recog.convert2gray(
    cv2.imread("./pokemon_sv_vs_support/python/asset/action_png/aiteno.png")
)
IMG_ACTION_2 = recog.convert2gray(
    cv2.imread("./pokemon_sv_vs_support/python/asset/action_png/exclamation_mark.png")
)
IMG_ACTION_3 = recog.convert2gray(
    cv2.imread("./pokemon_sv_vs_support/python/asset/action_png/kuridashita.png")
)
IMG_ACTION_4 = recog.convert2gray(
    cv2.imread("./pokemon_sv_vs_support/python/asset/action_png/modore.png")
)
IMG_ACTION_5 = recog.convert2gray(
    cv2.imread("./pokemon_sv_vs_support/python/asset/action_png/no.png")
)
IMG_ACTION_6 = recog.convert2gray(
    cv2.imread("./pokemon_sv_vs_support/python/asset/action_png/taoreta.png")
)
IMG_ACTION_7 = recog.convert2gray(
    cv2.imread("./pokemon_sv_vs_support/python/asset/action_png/tsukatta.png")
)
IMG_ACTION_8 = recog.convert2gray(
    cv2.imread("./pokemon_sv_vs_support/python/asset/action_png/yuke.png")
)
IMG_ACTIONS = [
    IMG_ACTION_1,
    IMG_ACTION_2,
    IMG_ACTION_3,
    IMG_ACTION_4,
    IMG_ACTION_5,
    IMG_ACTION_6,
    IMG_ACTION_7,
    IMG_ACTION_8,
]
IMG_LEVEL = cv2.imread(
    "./pokemon_sv_vs_support/python/asset/action_png/level_status.png"
)

# スプレッドシートの構造を変化させた場合は、ここを編集する。
VS_TIMESTAMP_COLUMN = 1
VS_ID_COLUMN = 2
ENEMY_TEAM_LAST_COLUMN = 8
MY_TEAM_COLUMN = 12
WIN_LOOSE_COLUMN = 16


def update_phase(img: np.ndarray, phase: int, spreadsheet: SpreadSheet) -> int:
    """画像認識を用いてフェーズを判定、処理を実行しフェーズを更新する。"""

    # main.pyの中で、引き継ぎたい変数。
    global vs_id
    global row_number
    global action_number
    global white_character_old
    global update_time
    global has_captured_select_scene
    global end_time
    if phase == 0 or phase == 1:
        img = recog.trim(
            img,
            TRIM_PLACE[1]["x"],
            TRIM_PLACE[1]["dx"],
            TRIM_PLACE[1]["y"],
            TRIM_PLACE[1]["dy"],
        )
        if recog.is_matched(img, IMG_MATCHING, THRESHOLD_MATCHING):
            logger_stream.debug("対戦相手検索中です。")
            return 2
        return phase
    elif phase == 2:
        img_text = recog.trim(
            img,
            TRIM_PLACE[1]["x"],
            TRIM_PLACE[1]["dx"],
            TRIM_PLACE[1]["y"],
            TRIM_PLACE[1]["dy"],
        )
        if recog.is_matched(img_text, IMG_FOUND_ENEMY, THRESHOLD_FOUND_ENEMY):
            # 【今後修正】順位認識を行う。
            logger_stream.debug("対戦相手が見つかりました。")
            vs_id = len(spreadsheet.get_col_values(1))
            action_number = 0
            if ACTION_LOG_ENABLED is True:
                cv2.imwrite(
                    "{}/pokemon_sv_vs_support/actions_png/{}_{}.png".format(
                        os.getcwd(), vs_id, action_number
                    ),
                    img,
                )
                logger_stream.debug("対戦相手情報を保存します。")
                action_number += 1
            row_number = vs_id + 1
            is_character, white_character_old = detect_character(
                img
            )  # white_character_oldエラー対策で設定。
            return 3
        return phase
    elif phase == 3:
        img_team = recog.trim(
            img,
            TRIM_PLACE["selecting_enemy_team"]["x"],
            TRIM_PLACE["selecting_enemy_team"]["dx"],
            TRIM_PLACE["selecting_enemy_team"]["y"],
            TRIM_PLACE["selecting_enemy_team"]["dy"],
        )
        img = recog.trim(
            img,
            TRIM_PLACE[2]["x"],
            TRIM_PLACE[2]["dx"],
            TRIM_PLACE[2]["y"],
            TRIM_PLACE[2]["dy"],
        )
        if recog.is_matched(img, IMG_SELECTING, THRESHOLD_SELECTING):
            # ポケモン認識処理を行う
            pokemons = recog_enemy_pokemons(img_team)
            logger_stream.debug("相手ポケモンを認識しました。{}".format(pokemons))
            values = [vs_id]
            values.extend(pokemons)
            cell_list = spreadsheet.set_range(
                row_number, VS_ID_COLUMN, row_number, ENEMY_TEAM_LAST_COLUMN
            )
            cell_list = spreadsheet.set_values_on_range(cell_list, values)
            spreadsheet.write_values(cell_list)
            logger_stream.debug("対戦ID、ポケモン名をスプレッドシートに書き込みました。")
            config.read(
                "./pokemon_sv_vs_support/python/asset/setting.ini", encoding="utf-8"
            )
            cell_list = spreadsheet.set_range(
                row_number, MY_TEAM_COLUMN, row_number, MY_TEAM_COLUMN
            )
            cell_list = spreadsheet.set_values_on_range(
                cell_list, [config["my_team"]["id"]]
            )
            spreadsheet.write_values(cell_list)
            logger_stream.debug("自分チームIDをスプレッドシートに書き込みました。")
            update_time = datetime.datetime.now()
            return 4
        return phase
    elif phase == 4:
        if ACTION_LOG_ENABLED is True:
            is_character, white_character = detect_character(img)
            dt: datetime.timedelta = datetime.datetime.now() - update_time
            if is_character:
                try:
                    if (
                        recog.is_matched(white_character, white_character_old, 0.8)
                        and dt.total_seconds() <= 5
                    ):
                        return phase
                except NameError:
                    # 初回はエラーが発生するのでそのエスケープ
                    pass
                update_time = datetime.datetime.now()
                cv2.imwrite(
                    "{}/pokemon_sv_vs_support/actions_png/{}_{}.png".format(
                        os.getcwd(), vs_id, action_number
                    ),
                    img,
                )
                white_character_old = white_character.copy()
                action_number += 1
        img = recog.trim(
            img,
            TRIM_PLACE[3]["x"],
            TRIM_PLACE[3]["dx"],
            TRIM_PLACE[3]["y"],
            TRIM_PLACE[3]["dy"],
        )
        if recog.is_matched(img, IMG_BATTLING, THRESHOLD_BATTLING):
            # 時間測定開始する。
            logger_stream.debug("対戦を開始しました。")
            now = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            end_time = datetime.datetime.now() + datetime.timedelta(minutes=20)
            cell_list = spreadsheet.set_range(
                row_number, VS_TIMESTAMP_COLUMN, row_number, VS_TIMESTAMP_COLUMN
            )
            cell_list = spreadsheet.set_values_on_range(cell_list, [now])
            spreadsheet.write_values(cell_list)
            logger_stream.debug("対戦開始日時をスプレッドシートに書き込みました。")
            has_captured_select_scene = True
            return 5
        return phase
    elif phase == 5:
        if ACTION_LOG_ENABLED is True:
            is_character, white_character = detect_character(img)
            dt: datetime.timedelta = datetime.datetime.now() - update_time
            if is_character:
                if (
                    recog.is_matched(white_character, white_character_old, 0.8)
                    and dt.total_seconds() <= 5
                ):
                    return phase
                update_time = datetime.datetime.now()
                cv2.imwrite(
                    "{}/pokemon_sv_vs_support/actions_png/{}_{}.png".format(
                        os.getcwd(), vs_id, action_number
                    ),
                    img,
                )
                white_character_old = white_character.copy()
                action_number += 1
                has_captured_select_scene = False
            else:
                if not (has_captured_select_scene):
                    img_enemy_level = recog.trim(
                        img,
                        TRIM_PLACE["enemy_level"]["x"],
                        TRIM_PLACE["enemy_level"]["dx"],
                        TRIM_PLACE["enemy_level"]["y"],
                        TRIM_PLACE["enemy_level"]["dy"],
                    )
                    img_my_level = recog.trim(
                        img,
                        TRIM_PLACE["my_level"]["x"],
                        TRIM_PLACE["my_level"]["dx"],
                        TRIM_PLACE["my_level"]["y"],
                        TRIM_PLACE["my_level"]["dy"],
                    )
                    if recog.is_matched(
                        img_enemy_level, IMG_LEVEL, THRESHOLD_LEVEL
                    ) and recog.is_matched(img_my_level, IMG_LEVEL, THRESHOLD_LEVEL):
                        cv2.imwrite(
                            "{}/pokemon_sv_vs_support/actions_png/{}_{}.png".format(
                                os.getcwd(), vs_id, action_number
                            ),
                            img,
                        )
                        action_number += 1
                        has_captured_select_scene = True
                img_win_lose = recog.trim(
                    img,
                    TRIM_PLACE[4]["x"],
                    TRIM_PLACE[4]["dx"],
                    TRIM_PLACE[4]["y"],
                    TRIM_PLACE[4]["dy"],
                )
                if recog.is_matched(img_win_lose, IMG_WIN, THRESHOLD_WIN):
                    # 背景の変化が大きいため、閾値を低めに設定。
                    logger_stream.debug("勝利しました。")
                    cell_list = spreadsheet.set_range(
                        row_number, WIN_LOOSE_COLUMN, row_number, WIN_LOOSE_COLUMN
                    )
                    cell_list = spreadsheet.set_values_on_range(cell_list, ["〇"])
                    spreadsheet.write_values(cell_list)
                    logger_stream.debug("勝敗をスプレッドシートに書き込みました。")
                    return 1
                elif recog.is_matched(img_win_lose, IMG_LOSE, THRESHOLD_LOSE):
                    # 背景の変化が大きいため、閾値を低めに設定。
                    logger_stream.debug("敗北しました。")
                    cell_list = spreadsheet.set_range(
                        row_number, WIN_LOOSE_COLUMN, row_number, WIN_LOOSE_COLUMN
                    )
                    cell_list = spreadsheet.set_values_on_range(cell_list, ["×"])
                    spreadsheet.write_values(cell_list)
                    logger_stream.debug("勝敗をスプレッドシートに書き込みました。")
                    return 1
                img = recog.trim(
                    img,
                    TRIM_PLACE[1]["x"],
                    TRIM_PLACE[1]["dx"],
                    TRIM_PLACE[1]["y"],
                    TRIM_PLACE[1]["dy"],
                )
                if recog.is_matched(img, IMG_MATCHING, THRESHOLD_MATCHING):
                    logger_stream.debug("勝敗の認識に失敗しました。対戦相手の検索中です。")
                    return 2
        else:
            img_win_lose = recog.trim(
                img,
                TRIM_PLACE[4]["x"],
                TRIM_PLACE[4]["dx"],
                TRIM_PLACE[4]["y"],
                TRIM_PLACE[4]["dy"],
            )
            if recog.is_matched(img_win_lose, IMG_WIN, THRESHOLD_WIN):
                # 背景の変化が大きいため、閾値を低めに設定。
                logger_stream.debug("勝利しました。")
                cell_list = spreadsheet.set_range(
                    row_number, WIN_LOOSE_COLUMN, row_number, WIN_LOOSE_COLUMN
                )
                cell_list = spreadsheet.set_values_on_range(cell_list, ["〇"])
                spreadsheet.write_values(cell_list)
                logger_stream.debug("勝敗をスプレッドシートに書き込みました。")
                return 1
            elif recog.is_matched(img_win_lose, IMG_LOSE, THRESHOLD_LOSE):
                # 背景の変化が大きいため、閾値を低めに設定。
                logger_stream.debug("敗北しました。")
                cell_list = spreadsheet.set_range(
                    row_number, WIN_LOOSE_COLUMN, row_number, WIN_LOOSE_COLUMN
                )
                cell_list = spreadsheet.set_values_on_range(cell_list, ["×"])
                spreadsheet.write_values(cell_list)
                logger_stream.debug("勝敗をスプレッドシートに書き込みました。")
                return 1
            img = recog.trim(
                img,
                TRIM_PLACE[1]["x"],
                TRIM_PLACE[1]["dx"],
                TRIM_PLACE[1]["y"],
                TRIM_PLACE[1]["dy"],
            )
            if recog.is_matched(img, IMG_MATCHING, THRESHOLD_MATCHING):
                logger_stream.debug("勝敗の認識に失敗しました。対戦相手の検索中です。")
                return 2
        return phase


def find_most_similar_pokemon(img: np.ndarray) -> tuple[str, float]:
    """入力画像と最も似たポケモンを見つけ、ポケモン名等を出力する
    parameter:
        img:cv2で読み込んだ画像
    return:
        poke_name:ポケモン名
        max_similarity:類似度
    """
    max_similarity = 0
    img_name = ""

    for file_path in POKE_PING_FILES:  # 全ポケモン画像に対してテンプレートマッチングを実行
        temp_origin = cv2.imread(file_path)
        try:  # 【今後修正】画像サイズエラーが出る場合があったので強引に処理。
            similarity = recog.find_max_similarity(img, temp_origin)
        except:
            break
        if similarity > max_similarity:
            max_similarity = similarity
            img_name, ext = os.path.splitext(os.path.basename(file_path))
    poke_name = ID[ID["img_name"] == img_name]["name"].values[0]

    return poke_name, max_similarity


def recog_enemy_pokemons(
    img_selecting: np.ndarray,
) -> list[str, str, str, str, str, str]:
    """相手選出部分のポケモン画像を認識する。

    param:
        img_selecting:選出部分の枠の画像
    return:
        ポケモン名を含んだリスト
    """
    pokemons = []
    # 1~6体目を順番に認識しpokemonsに出力する。
    place = TRIM_PLACE["pokemon"]
    for i in range(6):
        img_poke = recog.trim(
            img_selecting,
            place["x"],
            place["dx"],
            place["y"] + (place["dy"] + 1) * i,
            place["dy"],
        )
        pokemon_name, similarity = find_most_similar_pokemon(img_poke)
        if similarity >= THRESHOLD_POKEMON:
            pokemons.append(pokemon_name)
        else:
            logger_stream.info("{}体目のポケモンが認識でいませんでした。画像を差し替えてください。".format(i + 1))
            cv2.imwrite(
                "./pokemon_sv_vs_support/python/asset/{}.png".format(pokemon_name),
                img_poke,
            )
            pokemons.append("")
    return pokemons


def detect_character(img):
    white_character_img = recog.binarize(
        recog.convert2gray(
            recog.trim(
                img,
                TRIM_PLACE["actions"]["x"],
                TRIM_PLACE["actions"]["dx"],
                TRIM_PLACE["actions"]["y"],
                TRIM_PLACE["actions"]["dy"],
            )
        ),
        230,
    )
    for action_temp in IMG_ACTIONS:
        if recog.is_matched(white_character_img, action_temp, THRESHOLD_ACTION):
            return True, white_character_img
    return False, white_character_img


def main():
    ws = OBS(PORT, PASSWORD)
    path = os.getcwd()
    img_path = "{}/pokemon_sv_vs_support/python/screen.png".format(path)
    logger_stream.info("{}に保存します。".format(img_path))
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

    spreadsheet = SpreadSheet(config["spreadsheet"]["book"])
    spreadsheet.set_worksheet(config["spreadsheet"]["log_sheet"])
    logger_stream.debug("出力するスプレッドシートを認識しました。")

    while is_turned_on:
        # OBSでスクショを取る。
        ws.take_screenshot(SOURCE, img_path, width=1280, height=720)

        img = cv2.imread(img_path)
        phase = update_phase(img, phase, spreadsheet)
        if phase == 5 and TIMER_ENABLED is True:
            tod_time = end_time - datetime.datetime.now()
            if tod_time.seconds > 1200:
                ws.set_string(TIME_SOURCE, "試合終了")
            ws.set_string(
                TIME_SOURCE,
                "{}:{:02}".format(tod_time.seconds // 60, tod_time.seconds % 60),
            )


if __name__ == "__main__":
    logger_stream.debug("起動しました。")
    try:
        main()
    except:
        logger_stream.exception("エラーが発生しました。")
