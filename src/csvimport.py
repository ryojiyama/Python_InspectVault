import os
import pandas as pd
from datetime import datetime
import shutil
import traceback

class CSVImporter:
    def __init__(self, base_directory=None):
        self.base_directory = base_directory or os.path.abspath(os.path.join(os.getcwd(), os.pardir))
        self.save_directory = os.path.join(self.base_directory, 'CSV')
        self.copy_directory = os.path.join(self.base_directory, 'CSV_LOG')
        self.drive_letters = ['S:', 'U:', 'T:']

        # 必要なディレクトリの作成
        os.makedirs(self.save_directory, exist_ok=True)
        os.makedirs(self.copy_directory, exist_ok=True)

    def get_available_directories(self):
            """利用可能なHIOKIディレクトリを取得"""
            try:
                # 全環境でUSBドライブを検索
                available_dirs = [f"{drive}\\HIOKI8847" for drive in self.drive_letters
                                if os.path.exists(f"{drive}\\HIOKI8847")]
                print(f"見つかったUSBディレクトリ: {available_dirs}")
                return available_dirs
            except Exception as e:
                print(f"ディレクトリ取得でエラー: {str(e)}")
                print(traceback.format_exc())
                raise

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
        try:
            files = [f for f in os.listdir(directory)
                    if os.path.isfile(os.path.join(directory, f)) and f.endswith('.CSV')]

            if not files:
                print(f"CSVファイルが見つかりませんでした。ディレクトリを確認してください: {directory}")
                return False

            print(f"処理対象ファイル: {files}")
            today = datetime.now().strftime('%Y-%m-%d')
            base_filename = f'{today}_InspectionLOG.CSV'
            final_filename = self.generate_filename(self.save_directory, base_filename)

            return self.process_files(directory, files, final_filename)

        except Exception as e:
            print(f"ディレクトリ処理でエラー: {str(e)}")
            print(traceback.format_exc())
            return False

    def process_files(self, directory, files, final_filename):
        """CSVファイルの処理と保存"""
        try:
            output_path = os.path.join(self.save_directory, final_filename)
            copy_path = os.path.join(self.copy_directory, final_filename)

            print(f"処理を開始: {directory}")

            # 最初のファイルからA列のデータを取得
            first_file = os.path.join(directory, files[0])
            print(f"ヘッダー読み込み: {files[0]}")
            header_frame = pd.read_csv(
                first_file,
                skiprows=7,
                encoding='shift_jis',
                usecols=[0]
            )

            # 各CSVファイルのB列データを読み込み
            data_frames = []
            for file in files:
                file_path = os.path.join(directory, file)
                print(f"データ読み込み: {file}")
                data = pd.read_csv(
                    file_path,
                    skiprows=8,
                    nrows=2050,
                    encoding='shift_jis',
                    usecols=[1]
                )
                data_frames.append(data)

            print("データ結合処理開始")
            combined_data = pd.concat(data_frames, axis=1)
            final_data = pd.concat([header_frame, combined_data], axis=1)
            final_data.columns = ['Time'] + [
                os.path.splitext(os.path.basename(f))[0] for f in files
            ]

            print(f"ファイル保存: {output_path}")
            final_data.to_csv(output_path, index=False)
            shutil.copy(output_path, copy_path)

            # 元ファイルの削除
            for file in files:
                file_path = os.path.join(directory, file)
                print(f"元ファイル削除: {file}")
                os.remove(file_path)

            print(f"CSVファイルの作成、およびUSB内のファイル削除が完了しました。ファイル名: {final_filename}")
            return True

        except Exception as e:
            print(f"ファイル処理でエラー: {str(e)}")
            print(traceback.format_exc())
            return False

    def cleanup_old_files(self, days=30):
        """古いファイルの削除"""
        try:
            current_time = datetime.now().timestamp()

            for directory in [self.save_directory, self.copy_directory]:
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        file_age = current_time - os.path.getmtime(file_path)
                        if file_age > (days * 24 * 60 * 60):  # days to seconds
                            os.remove(file_path)
                            print(f"古いファイルを削除: {file}")
        except Exception as e:
            print(f"クリーンアップでエラー: {str(e)}")
            print(traceback.format_exc())

def main():
    """メイン処理"""
    try:
        base_directory = os.environ.get('OneDriveGraph')
        if not base_directory:
            print("環境変数 'OneDriveGraph' が設定されていません")
            return False

        print(f"ベースディレクトリ: {base_directory}")
        importer = CSVImporter(base_directory)

        # 古いファイルのクリーンアップ（30日以上前のファイル）
        importer.cleanup_old_files(30)

        # 利用可能なディレクトリを取得
        directories = importer.get_available_directories()
        print(f"検索対象ディレクトリ: {directories}")

        if not directories:
            print("利用可能なディレクトリが見つかりません")
            return False

        success = False
        for directory in directories:
            print(f"ディレクトリ処理開始: {directory}")
            if importer.process_directory(directory):
                success = True

        return success

    except Exception as e:
        print(f"メイン処理でエラー: {str(e)}")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    main()
