import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

worksheet = client.open("対戦ログ").worksheet('test')
worksheet2 = client.open("対戦ログ").worksheet('log')

#セルのA1~10に0~9を入力する
for i in range(10):
    worksheet.update_cell(i+1, 1, i)

#logシートのA列の行数を取得
timestamps = list(filter(None,worksheet2.col_values(1)))
print(len(timestamps))