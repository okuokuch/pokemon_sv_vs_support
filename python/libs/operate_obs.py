import obsws_python as obs
import obsws_python.error as obs_error

class OBS:
    """OBSの操作をするクラス。"""

    def __init__(self, port:int, password:str) -> None:
        """ポートとパスワードを用いてOBSに接続する。"""
        self.connect(port, password)

    def connect(self, port:int, password:str)->None:
        try:
            self.ws = obs.ReqClient(host='localhost', port=port, password=password)
        except ConnectionRefusedError as e:
            print(e)
            print('接続できませんでした。')
        except obs_error.OBSSDKError as e:
            print(e)
            print('portかパスワードを確認してください。')

    def take_screenshot(self, scene_name:str, file_path:str, img_format:str = 'png', width:int = None, height:int = None)->None:
        """指定したシーンのスクショを保存する。

        param:
            scene_name:シーン名
            file_path:保存ファイル名。フルパスで指定する必要あり。
            img_format:デフォルトはpng。
            width:保存する画像サイズの幅。未記入の場合、OBSで設定している幅となる。
            height:保存する画像サイズの高さ。未記入の場合、OBSで設定している高さとなる。
        """
        self.ws.save_source_screenshot(scene_name, img_format, file_path, width, height, -1)

if __name__ == '__main__':
    test = OBS(4455, 'obwgzSCmFWzpaJaq')