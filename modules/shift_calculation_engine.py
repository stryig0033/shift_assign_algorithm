'''
シフト構成を計算するための線形計画法モデル。

引数として以下を取る。
employees: 従業員のリスト(list)
availability: 従業員の勤務可能時間を格納した辞書(dict)
min_staff_required: 各時間帯に必要な最低人数を格納したリスト(list)

出力として以下を返す。
employee_shifts: 各従業員の始業時間と退勤時間の計算結果を格納した辞書(dict)
'''

import pulp

def shift_calculation_engine(employees, availability, min_staff_required):#8スロット=4時間
    
     # 線形計画法モデルのセットアップ
    model = pulp.LpProblem("StaffingProblem", pulp.LpMinimize)

    # 変数の作成（7時から23時30分までの各30分間隔）
    time_slots = range(7 * 2, 23 * 2 + 2)  # 7:00は14, 23:30は48
    shifts = pulp.LpVariable.dicts("Shift", ((e, t) for e in employees for t in time_slots), cat='Binary')

    # 目的関数を設定
    model += pulp.lpSum(shifts[(e, t)] for e in employees for t in time_slots)


    # 制約条件を追加
    for t in time_slots:
        model += pulp.lpSum(shifts[(e, t)] for e in employees if availability[e][t-14]) >= min_staff_required[t-14]
        
    # 従業員の勤務可能時間に対する制約
    for e in employees:
        for t in time_slots:
            if not availability[e][t - 14]:
                model += shifts[(e, t)] == 0         
                
    # モデルを解く
    model.solve()
    
    # 各従業員の始業時間と退勤時間を格納する辞書
    # 関数を実行するごとに更新される
    employee_shifts = {}

    for e in employees:
        shift_times = [t / 2 for t in time_slots if pulp.value(shifts[(e, t)]) == 1]
        if shift_times:
            start_time = min(shift_times)
            end_time = max(shift_times) + 0.5  # 退勤時間は30分後
            employee_shifts[e] = (start_time, end_time)
            
    return employee_shifts



from copy import deepcopy

# 時間を30分ごとのスロットに変換する関数
def time_to_slot(time):
    return int(time * 2) - 14

# シフトにアサインされた時間を出勤不可に更新する関数
def update_availability(shifts, availability):
    for name, times in shifts.items():
        if name in availability:
            start_slot = time_to_slot(times[0])
            end_slot = time_to_slot(times[1])
            for i in range(start_slot, end_slot):
                availability[name][i] = 0
                
    return availability


# 最適な順序でシフト計算を行う
def calculate_shifts_in_best_order(best_order, floors_dict, availability_dict, employees_name):
    final_shifts = {}
    availability_dict_updated = deepcopy(availability_dict)

    for floor in best_order:
        employee_data = floors_dict[floor]
        # シフトアサインの計算
        shifts = shift_calculation_engine(employees_name, availability_dict_updated, employee_data)

        # 勤務時間が2時間以下の従業員を削除
        shifts = {e: (start, end) for e, (start, end) in shifts.items() if end - start > 2}

        # 出勤可否を更新
        availability_dict_updated = update_availability(shifts, availability_dict_updated)

        # 最終的なシフトを辞書に追加
        final_shifts.update(shifts)

    return final_shifts