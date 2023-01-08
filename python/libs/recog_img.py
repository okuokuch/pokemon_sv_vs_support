import cv2
import numpy as np
import configparser

class ImageRecognition:
    def __init__(self) -> None:
        pass

    def trim(self, img:np.ndarray, x:int, dx:int, y:int, dy:int)->np.ndarray:
        """画像をトリムする。"""
        return img[y:y+dy, x:x+dx]

    def resize(self, img:np.ndarray, raito:float)->np.ndarray:
        """画像の縮尺を変更する

        parameter:
            img:縮尺を変更する画像
            raito:変更したい縮尺
        ---------------------------
        return:
            x方向とy方向にraito倍した画像
        """
        return cv2.resize(img, None, fx=raito, fy=raito)

    def find_max_similarity(self, img:np.ndarray, temp_img:np.ndarray)->float:
        """テンプレートマッチングし、類似度を出力する

        parameter
            img:走査される(動かない)画像
            temp_img:テンプレート画像。走査する(動く)画像
        ---------------------------
        return:
            類似度。0~1の間の数字で、1に近いほど類似する部分があることを示す
        ---------------------------
        Attention:
            img画像サイズより、temp_img画像サイズが大きいとエラーが発生します
        """
        match = cv2.matchTemplate(img,temp_img,cv2.TM_CCOEFF_NORMED)
        minVal,maxVal,minLoc,maxLoc = cv2.minMaxLoc(match)
        
        return maxVal

    def show(self, img:np.ndarray, window_name:str = 'test')->None:
        cv2.imshow(window_name, img)
        cv2.waitKey()
        cv2.destroyAllWindows()