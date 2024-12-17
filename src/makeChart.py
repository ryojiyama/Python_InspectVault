import pandas as pd
import matplotlib.pyplot as plt

# CSVファイルの読み込み
# file_path = '"C:\Users\QC07\OneDrive - トーヨーセフティホールディングス株式会社\QC_試験グラフ作成\CSV\2024-04-18_TestLOG.CSV"'
file_path = "C:/Users/QC07/OneDrive - トーヨーセフティホールディングス株式会社/QC_試験グラフ作成/CSV/2024-04-18_TestLOG.CSV"
data = pd.read_csv(file_path)

# A列を時間（秒数）として設定
time = data.iloc[:, 0]  # A列を取得

# グラフの作成と保存
for i in range(1, data.shape[1]):  # B列から最後の列まで繰り返し
    plt.figure(figsize=(10, 5))  # グラフのサイズ設定
    plt.plot(time, data.iloc[:, i], label=data.columns[i])  # 時間と各列のデータでグラフを描画
    plt.title(f'Graph of {data.columns[i]} over Time')  # グラフのタイトル
    plt.xlabel('Time (seconds)')  # X軸のラベル
    plt.ylabel('Value')  # Y軸のラベル
    plt.legend()  # 凡例の表示
    plt.grid(True)  # グリッドの表示
    plt.savefig(f'{data.columns[i]}_graph.png')  # グラフを画像として保存
    plt.close()  # グラフをクローズ

print("グラフの画像が生成されました。")
