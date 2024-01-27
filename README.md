# Auto shift generating system
This is an algorithm of calculating the best part-time shift pattern with linear programing by Python plup.  
I build this system for Oriental Hotel Kobe to enhance their work productivity by lettig them free from doing their annoying daily task.  

# シフト自動作成システム
PythonのライブラリであるPlupを用いた線形計画法によって、従業員の出勤可否から自動的にシフトを作成するシステムを作成しました。
一般的なシフト作成では「早番」「遅番」といったように勤務時間が確定しており、それに対する数理的アプローチは多くあるものの、ホテル・イベント会場・居酒屋などの、宴会や婚礼のスケジュールよって始業時間と終業時間が大きく変化する場合に対しては、有効なシフト作成の手段やシステムの前例がありませんでした。  
本システムではその点を克服し、実用に耐えうる程度まで精度を向上させています。完全に最適で完璧なシフトを作成するのは難しいものの、これまで1日当たり2時間程度かかっていたシフト作成がこのシステムにより30分以内に終了するようになっています。
