import os
import pandas as pd

# スクリプトが実行されているディレクトリの取得
scripts_directory = os.getcwd()

# scriptsディレクトリの親ディレクトリに移動して、基本パスを取得
base_directory = os.path.abspath(os.path.join(scripts_directory, os.pardir))

# 入力ファイルパスの設定
input_filepath = os.path.join(base_directory, 'CSV', '2024-04-19_TestLOG.CSV')

# ヘッダー行のみを読み込む
header_df = pd.read_csv(input_filepath, nrows=0, encoding='cp932')  # nrows=0でデータ行を読み込まずに列名のみ取得

# ヘッダー行からTime列を除いた列名を取得
header = header_df.columns[1:]  # Time列を除外

# 1行のデータとしてヘッダーを含むDataFrameを作成
header_data = [header.tolist()]  # リストのリストにすることでDataFrameのデータとして扱える
header_df_to_save = pd.DataFrame(header_data, columns=header)  # 列名としても同じヘッダーを使う

# ヘッダー情報をCSVファイルとして出力
output_filepath = os.path.join(base_directory, 'CSV', 'Header.csv')
header_df_to_save.to_csv(output_filepath, index=False, encoding='cp932')

print("ヘッダー情報が保存されました:", output_filepath)
