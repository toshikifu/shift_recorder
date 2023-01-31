#出力
import datetime,dateutil
import shutil
def download():
    date = datetime.datetime.now().strftime("%Y-%m")
    try:
        shutil.copy("datas/"+date+"_forDesktop.csv","/Users/toshiki/Downloads")
    except:
        print("ファイルがありませんでした")

def download_last_month():
    date = datetime.datetime.today()
    date = date - dateutil.relativedelta.relativedelta(months=1)
    date = date.strftime("%Y-%m")
    try:
        shutil.copy("datas/"+date+"_forDesktop.csv","/Users/toshiki/Downloads")
    except:
        print("ファイルがありませんでした")