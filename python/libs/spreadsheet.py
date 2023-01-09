import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SpreadSheet:

    def __init__(self, book_name) -> None:
        self.SCOPE =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', self.SCOPE)
        self.client = gspread.authorize(self.creds)
        self.workbook = self.client.open(book_name)

    def set_worksheet(self, sheet_name):
        self.worksheet = self.workbook.worksheet(sheet_name)

    def get_col_values(self, column_number:int)->list:
        values = list(filter(None, self.worksheet.col_values(column_number)))
        return values

    def set_range(self,  row, column, last_row, last_column)->list[gspread.Cell]:
        cell_list = self.worksheet.range(row, column, last_row, last_column)
        return cell_list

    def set_values_on_range(self, cell_list:list[gspread.Cell], values)->list[gspread.Cell]:
        for i, cell in enumerate(cell_list):
            cell.value = values[i]
        return cell_list

    def write_values(self, cell_list:list[gspread.Cell], is_converted:bool = True)->None:
        if is_converted:
            self.worksheet.update_cells(cell_list, 'user_entered')
        else:
            self.worksheet.update_cells(cell_list)