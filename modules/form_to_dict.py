'''
google formの回答データを辞書型に変換するモジュール

引数としてgoogle formから出力したcsvファイルを取る

各従業員の、各時間帯における出勤可否を辞書形式のバイナリデータで出力
'''

import pandas as pd

def form_of_employees_availability_to_dict(form):
    
    #出勤可能タイムテーブルのコード
    data = pd.read_csv(form, encoding='shift-jis')#任意のフォーム回答データ
    df = pd.DataFrame(data)
    
    # 時間帯のリストを作成
    times = pd.date_range("07:00", "23:30", freq="30min").time

    # データフレームにインデックス名とカラム名を追加
    new_df = pd.DataFrame(index=df["name"], columns=times)

    def is_time_in_range(start, end, check_time):
        if start <= end:
            return start <= check_time <= end
        else:
            return start <= check_time or check_time <= end

    # 出勤の可否をバイナリで表現
    for index, row in df.iterrows():
        employee_name = row["name"]
        if row["order"] == "終日OK":
            new_df.loc[employee_name, :] = 1
        else:
            start_time, end_time = row["order"].split("~")
            start_time = pd.to_datetime(start_time).time()
            end_time = pd.to_datetime(end_time).time()
            for time in times:
                new_df.loc[employee_name, time] = 1 if is_time_in_range(start_time, end_time, time) else 0
    
    # 従業員のリスト
    employees = new_df.index.to_list()

    # データを辞書型に変換
    dict = {}
    for i in range(len(new_df)):
        emp_name = new_df.index[i]
        emp_value = new_df.iloc[i].to_list()
        dict[emp_name] = emp_value
    
    return employees, dict