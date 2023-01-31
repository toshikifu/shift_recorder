from rumps import *
from record import *
import download,datetime

class RumpsTest(App):
    def __init__(self):
        super(RumpsTest, self).__init__("shift_recorder",icon="../images/black.png", title=None,quit_button="shift_recorderの終了")
        #デフォルトのメニュー作成
        self.menu=[
                MenuItem("開始",callback=self.start),
                MenuItem("休憩"),
                MenuItem("終了"),
                MenuItem("取り消し"),
                MenuItem("経過時間"),
                None,
                MenuItem("修正"),
                MenuItem("出力",callback=self.download),
                None,
                MenuItem("環境設定"),
                MenuItem("詳細")]

    def start(self,sender):
        #記録開始
        # print("開始しました")
        record("開始","")
        #タイマー軌道
        global my_timer,count
        count=0
        my_timer=Timer(self.pass_time,1)
        my_timer.start()
        #メニューの更新
        self.menu["開始"].set_callback(None)
        self.menu["休憩"].set_callback(self.rest)
        self.menu["終了"].set_callback(self.end)
        self.menu["取り消し"].set_callback(self.cancel)
        self.icon="../images/green.png"

    def end(self,sender):
        # print("終了しました")
        #タイマー停止
        my_timer.stop()
        #メニュー更新
        self.menu["終了"].set_callback(None)
        self.menu["開始"].set_callback(self.start)
        self.menu["休憩"].set_callback(None)
        self.menu["取り消し"].set_callback(None)
        self.menu["経過時間"].title="経過時間"
        self.icon="../images/pink.png"
        #入力フィールドの表示
        response = Window(message="Feed back?",dimensions=(300,200)).run()
        print(response.text)
        record("終了",response.text)
        self.icon="../images/black.png"
        # 再起動？

    def pass_time(self,sender):
        global count
        count = count+1
        pass_time = datetime.timedelta(seconds=int(count)+1)
        self.menu["経過時間"].title="経過時間:"+str(pass_time)

    def rest(self,sender):
        # print("休憩します")
        record("休憩","")
        my_timer.stop()
        self.menu["休憩"].set_callback(self.restart)
        self.menu["休憩"].title="再会"
        self.icon="../images/yellow.png"

    def restart(self,sender):
        # print("再会します")
        record("再会","")
        my_timer.start()
        self.menu["休憩"].set_callback(self.rest)
        self.menu["休憩"].title="休憩"
        self.icon="../images/green.png"

    def cancel(self,sender):
        # print("取り消します")
        if alert("取り消しますか？",ok="はい",cancel="いいえ"):
            record("取り消し","")
            my_timer.stop()
            self.menu["終了"].set_callback(None)
            self.menu["開始"].set_callback(self.start)
            self.menu["休憩"].set_callback(None)
            self.menu["取り消し"].set_callback(None)
            self.menu["経過時間"].title="経過時間"
            self.icon="../images/black.png"
        # 開始データ削除
    
    def download(self,sender):
        download.download()

if __name__ == "__main__":
    app = RumpsTest()
    app.run()