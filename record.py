from datetime import datetime
import pandas as pd
import numpy as np
import os
#ファイルがなかったら新規作成＆読み込み

def record(activity,text=""):
    time_now = datetime.now()
    date = time_now.strftime("%Y-%m")
    try:
        #日付の月のファイルを開く
        df = pd.read_csv("datas/"+date+"_forDesktop.csv")
    except:
        # なかったら作成する
        df = pd.DataFrame(columns=["ID","Activity","Time stamp","Feed back"])
        os.makedirs("datas",exist_ok=True)
    if activity =="開始":
        id = int(len(df)+1)
    else:
        id = np.nan
    df = df.append({"ID":id,
                "Activity":activity,
                "Time stamp":datetime.now(),
                "Feed back":text},
                ignore_index=True)
    df["ID"] = df["ID"].interpolate("ffill")
    df.to_csv("datas/"+date+"_forDesktop.csv",index=False)

    