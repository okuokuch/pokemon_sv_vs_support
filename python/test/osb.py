import obsws_python as obs
import os

#OBSとのWebsocketサーバへの接続
cl = obs.ReqClient(host='localhost', port=4455, password='obwgzSCmFWzpaJaq')

#保存したいパスを取得
path = os.getcwd() + '\\pokemon_sv_vs_support'
print('{}\\test.png'.format(path))

#test.pngを保存。保存サイズはデフォルト。
cl.save_source_screenshot('vscode', 'png', '{}\\test.png'.format(path),None, None, -1)