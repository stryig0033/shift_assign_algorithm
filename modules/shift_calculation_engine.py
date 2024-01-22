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

def shift_calculation_engine(employees, availability, min_staff_required):
    
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