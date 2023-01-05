from tkinter import *
from tkinter import ttk

class Application(ttk.Frame):
    """ポケモン対戦画面を画像認識してスプレッドシートに出力するアプリのGUI"""

    def __init__(self, master:Tk=None):
        super().__init__(master)
        self.master = master
        self.master.title('スプレッドシート転送アプリ')
        self.master.geometry('850x500')        
        self.font_family = 'calibri'
        self.font_size = 15
        self.font_size_title = 17
        self.grid_x, self.grid_y = 2,2
        self.style = ttk.Style()
        self.style.configure("Custom.TButton",font = (self.font_family, self.font_size))
        self.create_widget()

    def create_widget(self):
        pass

if __name__ == '__main__':
    root = Tk()
    app = Application(master = root)
    app.mainloop()