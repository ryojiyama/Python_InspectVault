import pandas as pd
import os
import glob
import re
from datetime import datetime

# ベースディレクトリの取得
def get_base_directory():
    return os.path.abspath(os.path.join(os.getcwd(), os.pardir))

# CSVファイルの読み込み
def read_csv_file(filepath, encoding='cp932'):
    try:
        return pd.read_csv(filepath, encoding=encoding)
    except FileNotFoundError:
        print(f"Error: The file {filepath} does not exist.")
        return None

# ファイルパスの生成
def generate_file_paths(base_directory, sub_folder, pattern):
    return glob.glob(os.path.join(base_directory, sub_folder, pattern))

# Timeを含む行を取得
def get_time_row(df):
    if df.iloc[:, 1].dtype != object:
        df.iloc[:, 1] = df.iloc[:, 1].astype(str)
    return df[df.iloc[:, 1].str.contains('Time')]

# データのソートなどの処理
def process_data(df):
    # 列が文字列型でなければ文字列型に変換
    if df['Time'].dtype != object:
        df['Time'] = df['Time'].astype(str)

    # Time行を抽出しておく
    time_row = df[df['Time'].str.contains('Time')]

    # ここでデータをソートしたり、フィルタリングするなどの操作を実行
    df_sorted = sort_and_filter_data(df)

    # Time行を元の位置に戻す
    df_final = pd.concat([time_row, df_sorted])

    # 52列目から最終列までの値を27列目から並べ直す
    cols_to_move = df_final.columns[52:]  # 52列目以降の列名を取得
    new_cols_order = list(df_final.columns[:27]) + list(cols_to_move) + list(df_final.columns[27:52])
    df_final = df_final.reindex(columns=new_cols_order)

    # 1行目の1977列目から、データフレームの最終行の最終列までの値をクリア
    if len(df_final.columns) > 1977:
        df_final.iloc[0:, 1977:] = None  # 指定範囲の値をクリア
    else:
        print("警告: データフレームに1977列目が存在しません。")

    # 1列目の値を2列目にコピーし、1列目の値は削除
    df_final.iloc[:, 1] = df_final.iloc[:, 0].astype(str)  # 1列目の値を文字列として2列目にコピー
    df_final.iloc[:, 0] = None  # 1列目の値を削除

    return df_final

def sort_and_filter_data(df):
    # ここにデータのソートやフィルタリングのロジックを実装
    return df  # 仮にそのまま返す

# ファイルの保存
def save_filtered_df(df, time_row, keyword, filename_pattern, date, base_directory):
    filtered_df = df[df.iloc[:, 1].str.contains(keyword)]
    if not filtered_df.empty:
        result_df = pd.concat([time_row, filtered_df], ignore_index=True)
        filepath = os.path.join(base_directory, filename_pattern.format(date=date))
        result_df.to_csv(filepath, encoding='cp932', index=False)

# メイン処理関数
def process_files():
    base_directory = get_base_directory()
    input_files = generate_file_paths(base_directory, 'CSV', '*Test*LOG*.CSV')

    for file_path in input_files:
        df = read_csv_file(file_path)
        if df is not None:
            time_row = get_time_row(df)
            df_processed = process_data(df)
            file_date = extract_date_from_filename(os.path.basename(file_path))
            if file_date:
                save_filtered_df(df, time_row, 'HEL', 'Helmet_Test_{date}_1.csv', file_date, base_directory)
                save_filtered_df(df, time_row, 'BASEBALL', 'Baseball_Test_{date}_1.csv', file_date, base_directory)
                save_filtered_df(df, time_row, 'BICYCLE', 'Bicycle_Test_{date}_1.csv', file_date, base_directory)
                save_filtered_df(df, time_row, 'FALLARR', 'FallArrest_Test_{date}_1.csv', file_date, base_directory)

# ファイル名から日付を抽出
def extract_date_from_filename(filename):
    match = re.search(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        return match.group(1).replace('-', '')
    return None

if __name__ == '__main__':
    process_files()
