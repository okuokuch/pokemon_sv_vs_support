from tkinter import *
from tkinter import ttk, scrolledtext 

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
        #Frameの定義
        self.upper_notebook = ttk.Notebook(self.master)
        self.lower_frame = ttk.Frame(self.master)
        self.tab1 = ttk.Frame(self.upper_notebook)
        self.tab2 = ttk.Frame(self.upper_notebook)
        self.log_area = scrolledtext.ScrolledText(self.lower_frame)

        #Labelの定義
        self.label_obs = ttk.Label(self.tab1, text='OBS設定')

        self.upper_notebook.add(self.tab1, text='基本設定')
        self.upper_notebook.add(self.tab2, text='自分ポケモン')

        self.upper_notebook.grid(column=0, row=0, sticky=W+N)
        self.lower_frame.grid(column=0, row=1, sticky=W)
        self.label_obs.grid(column=0, row=0)
        self.log_area.grid(column=0, row=0)

        #重み付け
        self.master.rowconfigure(0, weight=2)
        self.master.rowconfigure(1, weight=1)

if __name__ == '__main__':
    root = Tk()
    app = Application(master = root)
    app.mainloop()