'''
シフトの可視化を行うモジュール。
出力としてガントチャートを作成する.
'''

import numpy as np
import matplotlib.pyplot as plt
import japanize_matplotlib

def shift_visualization(employee_shifts, title):
    
    # ガントチャートの作成
    fig, ax = plt.subplots(figsize=(10, 8))

    # 辞書に基づいて各従業員のシフトをプロット
    for i, (e, times) in enumerate(employee_shifts.items()):
        start_time, end_time = times
        ax.broken_barh([(start_time, end_time - start_time)], (i - 0.4, 0.8), facecolors='tab:blue')

    ax.set_yticks(range(len(employee_shifts)))
    ax.set_yticklabels(employee_shifts.keys())

    ax.set_xticks(np.arange(7, 24, 0.5))
    ax.set_xticklabels([f'{int(h)}:{int(30*(h%1))}' for h in np.arange(7, 24, 0.5)])

    ax.tick_params(axis='x', labelsize=8)
    ax.set_xlabel('Time')
    ax.set_ylabel('Employee')
    ax.set_title(f'{title}')
    ax.grid(True)

    plt.show()