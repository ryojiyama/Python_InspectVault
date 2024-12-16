

import os
import pandas as pd
from datetime import datetime
import shutil

# 利用可能なドライブを指定
drive_letters = ['S:', 'U:', 'T:']
directories = [f"{drive}\\HIOKI8847" for drive in drive_letters if os.path.exists(f"{drive}\\HIOKI8847")]

# 日付を取得してファイル名を生成
today = datetime.now().strftime('%Y-%m-%d')
base_filename = f'{today}_InspectionLOG.CSV'

# スクリプトが実行されているディレクトリの取得
scripts_directory = os.getcwd()

# scriptsディレクトリの親ディレクトリに移動して、基本パスを取得
base_directory = os.path.abspath(os.path.join(scripts_directory, os.pardir))

# 保存先ディレクトリとコピー先ディレクトリのパスを設定
# save_directory = base_directory
save_directory = os.path.join(base_directory, 'CSV')
copy_directory = os.path.join(base_directory, 'CSV_LOG')

# 連番を付けるための関数
def generate_filename(base_path, base_filename):
    counter = 1
    filename = base_filename
    while os.path.exists(os.path.join(base_path, filename)):
        filename = f"{counter}-{base_filename}"
        counter += 1
    return filename

for directory in directories:
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.endswith('.CSV')]
    if files:
        final_filename = generate_filename(save_directory, base_filename)
        output_path = os.path.join(save_directory, final_filename)
        copy_path = os.path.join(copy_directory, final_filename)

        # 最初のファイルからA列のデータ全てを取得
        header_frame = pd.read_csv(os.path.join(directory, files[0]), skiprows=7, encoding='shift_jis', usecols=[0])

        # 各CSVファイルのB列データを読み込み、リストに格納
        data_frames = []
        for file in files:
            data = pd.read_csv(os.path.join(directory, file), skiprows=8, nrows=2050, encoding='shift_jis', usecols=[1])
            data_frames.append(data)

        # データフレームを横方向に連結
        combined_data = pd.concat(data_frames, axis=1)

        # ヘッダーフレームと結合したデータを連結
        final_data = pd.concat([header_frame, combined_data], axis=1)

        # ヘッダーの修正
        final_data.columns = ['Time'] + [os.path.splitext(os.path.basename(f))[0] for f in files]

        # 結果をCSVファイルに保存
        final_data.to_csv(output_path, index=False)

        # ファイルを指定のディレクトリにコピー
        shutil.copy(output_path, copy_path)

        # USBドライブ内のCSVファイルを削除
        for file in files:
            os.remove(os.path.join(directory, file))

        print(f"CSVファイルの作成、およびUSB内のファイル削除が完了しました。ファイル名: {final_filename}")
    else:
        print(f"CSVファイルが見つかりませんでした。ディレクトリを確認してください: {directory}")
