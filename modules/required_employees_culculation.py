'''
宴会情報から必要な従業員数を計算するモジュール
引数として宴会情報のリストを受け取り、必要な従業員数のデータフレームを返す
'''

import pandas as pd

def required_employees(data):
    
    # 辞書型データをリストに変換
    data_list = []
    for floor, info in data.items():
        data_list.append([floor, info['room'], info['guests_num'], info['time_start'], info['time_end']])

    # データフレームの作成
    df = pd.DataFrame(data_list, columns=["floor", "room", "num", "start", "end"])

    # 初期化
    def initialize_employee_count_dict():
        floors = set(df['floor'])
        return {floor: [0] * 34 for floor in floors}
    
    # 時間をスロットに変換
    def time_to_slot(time_str):
        hours, minutes = map(int, time_str.split(':'))
        slot = hours * 2 + minutes // 30 - 14
        return max(0, min(33, slot))
    
    # 必要従業員数の計算
    def calculate_required_employees(num_guests):
        return 1 + num_guests // 10

    employee_count_per_floor = initialize_employee_count_dict()

    # データの処理
    for index, row in df.iterrows():
        start_time = time_to_slot(row["start"])
        end_time = time_to_slot(row["end"])
        num_guests = row["num"]
        floor = row["floor"]

        required_employees = calculate_required_employees(num_guests)

        for slot in range(start_time - 4, end_time + 2):
            if 0 <= slot < len(employee_count_per_floor[floor]):
                employee_count_per_floor[floor][slot] += required_employees

    # データフレームへの変換
    time_slots = [f"{hour // 2 + 7:02d}:{30 * (hour % 2):02d}" for hour in range(34)]
    required_df = pd.DataFrame(employee_count_per_floor, index=time_slots).T
    
    return required_df