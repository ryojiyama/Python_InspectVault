import pandas as pd
import os
import re

def read_and_preprocess(filepath, encoding='cp932'):
    df = pd.read_csv(filepath, encoding=encoding)
    print(df.head())
    df_transposed = df.T
    df_transposed.reset_index(inplace=True)
    df_transposed.rename(columns={'index': 'New Column'}, inplace=True)
    return df_transposed

def sort_data(df_transposed):
    sort_priority = ['HEL_TOP', 'HEL_ZENGO', 'HEL_SIDE', 'BICYCLE', 'BASEBALL', 'FALLARR']
    def custom_sort(value):
        if isinstance(value, float):
            return (len(sort_priority), 0)
        match = re.match(r"(\d+)(HEL_TOP|HEL_ZENGO|HEL_SIDE|BICYCLE|BASEBALL|FALLARR)", value)
        if match:
            number_part = int(match.group(1))
            identifier_part = match.group(2)
            sort_index = sort_priority.index(identifier_part)
            return (sort_index, number_part)
        return (len(sort_priority), 0)

    df_sorted = df_transposed.sort_values(by="New Column", key=lambda x: x.apply(custom_sort))
    return df_sorted

def adjust_columns(df_sorted):
    # 52列目から最終列までの値を27列目から並べ直す
    columns_to_move = df_sorted.iloc[:, 51:]  # 52列目からの列を取得
    remaining_columns_before = df_sorted.iloc[:, :26]  # 27列目の前までの列を取得
    remaining_columns_after = df_sorted.iloc[:, 26:51]  # 27列目から51列目までの列を取得

    # 新しい列の順序でデータフレームを再構築
    df_sorted = pd.concat([remaining_columns_before, columns_to_move, remaining_columns_after], axis=1)

    # 1列目の前に新しい列(New First Column)を追加し、2列目を削除
    df_sorted.insert(0, 'New First Column', pd.Series([None]*df_sorted.shape[0]))
    df_sorted.drop(df_sorted.columns[2], axis=1, inplace=True)  # 列の追加により2列目がずれる

    # 3列目から26列目までのデータを消去
    df_sorted.iloc[:, 2:26] = None  # 3列目から26列目のデータをNoneで置き換える

    return df_sorted

def save_dataframe_with_sequence(df, base_directory, base_filename):
    base_filepath = os.path.join(base_directory, base_filename)
    filename, ext = os.path.splitext(base_filepath)
    i = 1
    new_filepath = f"{filename}_{i}{ext}"
    while os.path.exists(new_filepath):
        i += 1
        new_filepath = f"{filename}_{i}{ext}"
    df.to_csv(new_filepath, encoding='cp932', index=False)
    print(f"Saved: {new_filepath}")

def process_files(directory, keyword):
    csv_dir = os.path.join(directory, 'CSV')
    if not os.path.exists(csv_dir):
        print(f"CSV directory does not exist: {csv_dir}")
        return
    files = [file for file in os.listdir(csv_dir) if keyword in file and file.endswith('.CSV')]
    if not files:
        print("No files found.")
        return
    print(f"Processing {len(files)} files...")
    for file in files:
        filepath = os.path.join(csv_dir, file)
        df_transposed = read_and_preprocess(filepath)
        df_sorted = sort_data(df_transposed)
        df_final = adjust_columns(df_sorted)
        output_filename = 'Output_' + file
        save_dataframe_with_sequence(df_final, directory, output_filename)

# スクリプトが実行されているディレクトリの取得
scripts_directory = os.getcwd()
base_directory = os.path.abspath(os.path.join(scripts_directory, os.pardir))

# 指定されたディレクトリとキーワードでファイルを処理
process_files(base_directory, 'InspectionLOG')
print(base_directory)
