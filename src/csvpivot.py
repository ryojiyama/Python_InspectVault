import pandas as pd
import numpy as np
import os
import re

class CSVPivot:
    def __init__(self, base_directory=None):
        self.base_directory = base_directory or os.environ.get('OneDriveGraph')
        self.csv_dir = os.path.join(self.base_directory, 'CSV')

    def read_and_preprocess(self, filepath, encoding='cp932'):
        """CSVファイルを読み込んで前処理を行う"""
        try:
            df = pd.read_csv(filepath, encoding=encoding)
            print(f"ファイル読み込み: {os.path.basename(filepath)}")
            print(f"データ形状: {df.shape}")
            df_transposed = df.T
            df_transposed.reset_index(inplace=True)
            df_transposed.rename(columns={'index': 'New Column'}, inplace=True)
            return df_transposed
        except Exception as e:
            print(f"ファイル読み込みエラー: {str(e)}")
            raise

    def sort_data(self, df_transposed):
        """データのソート処理"""
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

    def adjust_columns(self, df_sorted):
        """列の調整処理"""
        # 52列目から最終列までの値を27列目から並べ直す
        columns_to_move = df_sorted.iloc[:, 51:]
        remaining_columns_before = df_sorted.iloc[:, :24]
        remaining_columns_after = df_sorted.iloc[:, 24:51]
        df_sorted = pd.concat([remaining_columns_before, columns_to_move, remaining_columns_after], axis=1)

        # 1列目の前に新しい列(New First Column)を追加し、2列目を削除
        df_sorted.insert(0, 'New First Column', pd.Series([np.nan]*df_sorted.shape[0]))
        df_sorted.drop(df_sorted.columns[2], axis=1, inplace=True)

        # 3列目から26列目までのデータをnp.nanで置き換える
        df_sorted.iloc[:, 2:24] = np.nan

        return df_sorted

    def save_dataframe_with_sequence(self, df, base_filename):
        """連番付きでデータフレームを保存"""
        base_filepath = os.path.join(self.base_directory, base_filename)
        filename, ext = os.path.splitext(base_filepath)
        i = 1
        new_filepath = f"{filename}_{i}{ext}"
        while os.path.exists(new_filepath):
            i += 1
            new_filepath = f"{filename}_{i}{ext}"

        df.to_csv(new_filepath, encoding='cp932', index=False)
        print(f"保存完了: {new_filepath}")
        return new_filepath

    def process_files(self):
        """CSVファイルの処理を実行"""
        if not os.path.exists(self.csv_dir):
            print(f"CSVディレクトリが存在しません: {self.csv_dir}")
            return False

        files = [file for file in os.listdir(self.csv_dir)
                if 'InspectionLOG' in file and file.endswith('.CSV')]

        if not files:
            print("処理対象のファイルが見つかりません")
            return False

        print(f"処理対象ファイル数: {len(files)}")

        try:
            for file in files:
                filepath = os.path.join(self.csv_dir, file)
                df_transposed = self.read_and_preprocess(filepath)
                df_sorted = self.sort_data(df_transposed)
                df_final = self.adjust_columns(df_sorted)
                output_filename = 'Output_' + file
                self.save_dataframe_with_sequence(df_final, output_filename)
            return True
        except Exception as e:
            print(f"処理中にエラーが発生しました: {str(e)}")
            return False

def main():
    """メイン処理"""
    base_directory = os.environ.get('OneDriveGraph')
    if not base_directory:
        print("環境変数 'OneDriveGraph' が設定されていません")
        return False

    pivot = CSVPivot(base_directory)
    return pivot.process_files()

if __name__ == "__main__":
    main()