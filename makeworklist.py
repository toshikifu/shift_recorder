import pandas as pd
import datetime
import calendar
import dateutil

def make_work_list(i=0):
    #月の確認
    month = datetime.datetime.today()
    month = month - dateutil.relativedelta.relativedelta(months=i)
    month = month.strftime("%Y-%m")
    #対象ファイルを指定
    try:
        fromdesktop = pd.read_csv("datas/"+month+"_forDesktop.csv")
    except:
        fromdesktop = pd.DataFrame(columns=["ID","Activity","Time stamp","Feed back"])
    try:
        fromnote = pd.read_csv("datas/"+month+"_forNote.csv")
    except:
        fromnote = pd.DataFrame(columns=["ID","Activity","Time stamp","Feed back"])

    #出力用DataFrame
    dd = pd.DataFrame(columns=["day","start","end","feedback"])

    for df in [fromdesktop,fromnote]:
        #ファイルの整形
        df["Time stamp"] = pd.to_datetime(df["Time stamp"].str[:16])

        #ユニークなcase_idを抽出
        case_ids = df["ID"].unique()

        #集計
        for case_id in case_ids:
            if "取り消し" in list(df[df["ID"]==case_id]["Activity"]):
                continue
            dd = dd.append({
                    "day":str(df[df["ID"]==case_id][df["Activity"]=="開始"]["Time stamp"].iloc[-1])[:10],
                    "start":str(df[df["ID"]==case_id][df["Activity"]=="開始"]["Time stamp"].iloc[-1])[-8:],
                    "end":str(df[df["ID"]==case_id][df["Activity"]=="終了"]["Time stamp"].iloc[-1])[-8:],
                    "feedback":str(df[df["ID"]==case_id][df["Activity"]=="終了"]["Feed back"].iloc[-1])}
                    ,ignore_index=True)

    #差分計算
    dd["time(min)"] = (pd.to_datetime(dd["end"]) - pd.to_datetime(dd["start"])).dt.total_seconds()

    #分表示に
    dd["time(min)"] = dd["time(min)"]/60

    #曜日計算
    dd["date"] = pd.to_datetime(dd["day"]).dt.day_name()

    #表示順変更
    dd = dd.reindex(columns=["day","date","start","end","time(min)","feedback"])

    #==============================================================================

    now = datetime.datetime.now()
    month_days = [i+1 for i in range(calendar.monthrange(now.year, now.month)[1])]
    days = []
    for day in month_days:
        days.append(month+"-"+str(day))

    d_zero = pd.DataFrame(days,columns=["day"])
    d_zero["time(min)"]=0
    ddd = dd[["day","time(min)"]]

    work_list = pd.concat([ddd,d_zero])
    work_list["day"] = pd.to_datetime(work_list["day"])
    work_list = work_list.groupby("day")["time(min)"].sum()

    with pd.ExcelWriter("/Users/toshiki/Downloads/"+month+"_出勤簿.xlsx") as writer:
        dd.to_excel(writer, sheet_name='勤務履歴')
        work_list.to_excel(writer, sheet_name='出勤簿')