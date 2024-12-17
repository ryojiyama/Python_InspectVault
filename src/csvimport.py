import os
import pandas as pd
from datetime import datetime
import shutil

class CSVImporter:
    def __init__(self, base_directory=None):
        # base_directoryが指定されていない場合、環境変数から取得
        self.base_directory = base_directory or os.environ.get('OneDriveGraph') or os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        # ディレクトリの存在確認と作成
        self.save_directory = os.path.join(self.base_directory, 'CSV')
        self.copy_directory = os.path.join(self.base_directory, 'CSV_LOG')
        # 必要なディレクトリを作成
        os.makedirs(self.save_directory,exist_ok=True)
        os.makedirs(self.copy_directory,exist_ok=True)
        self.drive_letters = ['S:', 'U:', 'T:']

    def get_available_directories(self):
        """利用可能なHIOKIディレクトリを取得"""
        return [f"{drive}\\HIOKI8847" for drive in self.drive_letters
                if os.path.exists(f"{drive}\\HIOKI8847")]

    def generate_filename(self, base_path, base_filename):
        """ユニークなファイル名を生成"""
        counter = 1
        filename = base_filename
        while os.path.exists(os.path.join(base_path, filename)):
            filename = f"{counter}-{base_filename}"
            counter += 1
        return filename

    def process_directory(self, directory):
        """指定されたディレクトリのCSVファイルを処理"""
        files = [f for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f)) and f.endswith('.CSV')]

        if not files:
            print(f"CSVファイルが見つかりませんでした。ディレクトリを確認してください: {directory}")
            return False

        today = datetime.now().strftime('%Y-%m-%d')
        base_filename = f'{today}_InspectionLOG.CSV'
        final_filename = self.generate_filename(self.save_directory, base_filename)

        return self.process_files(directory, files, final_filename)

    def process_files(self, directory, files, final_filename):
        """CSVファイルの処理と保存"""
        try:
            output_path = os.path.join(self.save_directory, final_filename)
            copy_path = os.path.join(self.copy_directory, final_filename)

            # 最初のファイルからA列のデータを取得
            header_frame = pd.read_csv(
                os.path.join(directory, files[0]),
                skiprows=7,
                encoding='shift_jis',
                usecols=[0]
            )

            # 各CSVファイルのB列データを読み込み
            data_frames = []
            for file in files:
                data = pd.read_csv(
                    os.path.join(directory, file),
                    skiprows=8,
                    nrows=2050,
                    encoding='shift_jis',
                    usecols=[1]
                )
                data_frames.append(data)

            # データの結合と処理
            combined_data = pd.concat(data_frames, axis=1)
            final_data = pd.concat([header_frame, combined_data], axis=1)
            final_data.columns = ['Time'] + [
                os.path.splitext(os.path.basename(f))[0] for f in files
            ]

            # ファイルの保存とクリーンアップ
            final_data.to_csv(output_path, index=False)
            shutil.copy(output_path, copy_path)

            # 元ファイルの削除
            for file in files:
                os.remove(os.path.join(directory, file))

            print(f"CSVファイルの作成、およびUSB内のファイル削除が完了しました。ファイル名: {final_filename}")
            return True

        except Exception as e:
            print(f"エラーが発生しました: {str(e)}")
            return False

def main():
    # 環境変数から基本パスを取得
    base_directory = os.environ.get('OneDriveGraph')
    if not base_directory:
        print("環境変数 'OneDriveGraph'が設定されていません")
        return False

    importer = CSVImporter()
    directories = importer.get_available_directories()
    success = False

    for directory in directories:
        if importer.process_directory(directory):
            success = True

    return success

if __name__ == "__main__":
    main()
