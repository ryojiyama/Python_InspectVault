import pandas as pd
import os

# スクリプトが実行されているディレクトリの取得
scripts_directory = os.getcwd()

# scriptsディレクトリの親ディレクトリに移動して、基本パスを取得
base_directory = os.path.abspath(os.path.join(scripts_directory, os.pardir))

# 入力ファイルパスの設定
input_filepath = os.path.join(base_directory, 'CSV', '2024-04-19_TestLOG.CSV')

# 出力ファイルパスの設定
output_filepath = os.path.join(base_directory, 'OutputTest.csv')

# CSVファイルの読み込み
df = pd.read_csv(input_filepath, encoding='cp932')

# データフレームを転置
df_transposed = df.T

# 行インデックスをリセットして新しい列として追加
df_transposed.reset_index(inplace=True)
df_transposed.rename(columns={'index': 'New Column'}, inplace=True)

# 1列目の値を基にソートする関数の定義
def custom_sort(value):
    sort_priority = ['HEL_TOP', 'HEL_ZENGO']
    parts = value.split('_')
    if len(parts) > 1 and any(prefix in parts[0] for prefix in sort_priority):
        sort_key = parts[0]  # 文字列部分を取得
        sort_index = sort_priority.index(sort_key) if sort_key in sort_priority else len(sort_priority)
        return (sort_index, int(parts[1]))  # 文字列の優先順位と数字部分
    else:
        return (len(sort_priority), 0)

# Timeを含む行を除外してソートするために一時的に保存
time_row = df_transposed[df_transposed['New Column'].str.contains('Time')]

# ソート対象となるデータの選択
df_filtered = df_transposed[~df_transposed['New Column'].str.contains('Time')]
df_filtered = df_filtered[df_filtered['New Column'].str.match(r'^\d{4}[A-Z_]+')]

# ソート実行
df_sorted = df_filtered.sort_values(by='New Column', key=lambda x: x.apply(custom_sort))

# Time行を元の位置に戻す
df_final = pd.concat([time_row, df_sorted])

# 52列目から最終列までの値を27列目から並べ直す
cols_to_move = df_final.columns[52:]  # 52列目以降の列名を取得
new_cols_order = list(df_final.columns[:27]) + list(cols_to_move) + list(df_final.columns[27:52])
df_final = df_final.reindex(columns=new_cols_order)

# 1行目の731列目から、データフレームの最終行の最終列までの値をクリア
if len(df_final.columns) > 1977:
    df_final.iloc[0:, 1977:] = None  # 指定範囲の値をクリア
else:
    print("警告: データフレームに1977列目が存在しません。")

# 1列目の値を2列目にコピーし、1列目の値は削除
df_final.iloc[:, 1] = df_final.iloc[:, 0].astype(str)  # 1列目の値を文字列として2列目にコピー
df_final.iloc[:, 0] = None  # 1列目の値を削除

# 3列目3行目から27列目最終行までの値を削除
df_final.iloc[1:, 2:27] = None  # 指定範囲の値を削除

# 転記先のCSVファイルに保存
df_final.to_csv(output_filepath, encoding='cp932', index=False)