import os
import logging
from datetime import datetime
from pathlib import Path

class GraphGenerationController:
    def __init__(self):
        self.setup_logging()
        self.setup_paths()

    def setup_logging(self):
        # ログファイルの設定
        log_dir = Path(os.environ['OneDriveGraph']) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"graph_generation_{datetime.now():%Y%m%d_%H%M%S}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('GraphGeneration')

    def setup_paths(self):
        # 環境変数からパスを取得
        self.base_path = os.environ.get('OneDriveGraph')
        if not self.base_path:
            raise EnvironmentError("環境変数 'OneDriveGraph' が設定されていません。")

        # 必要なディレクトリの存在確認と作成
        self.logger.info(f"Base path: {self.base_path}")
        required_dirs = ['CSV', 'CSV_LOG', 'templates', 'logs']
        for dir_name in required_dirs:
            dir_path = Path(self.base_path) / dir_name
            if not dir_path.exists():
                self.logger.warning(f"ディレクトリが存在しません: {dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"ディレクトリを作成しました: {dir_path}")
            else:
                self.logger.info(f"ディレクトリが存在します: {dir_path}")

    def run_process(self):
        try:
            self.logger.info("グラフ生成プロセスを開始します")

            # 1. CSVインポート
            self.logger.info("CSVインポートを開始")
            from src.csvimport import main as csv_import_main
            success = csv_import_main()
            if not success:
                self.logger.warning("csvインポートでエラーが発生しました")
                return

            # 2. CSVピボット
            self.logger.info("CSVピボット処理を開始")
            from src.csvpivot import main as csv_pivot_main
            csv_pivot_main()

            # 3. XLSXコンバート
            self.logger.info("XLSXコンバート処理を開始")
            from src.csvtoxlsxconverter import main as csv_to_xlsx_main
            csv_to_xlsx_main()

            self.logger.info("全てのプロセスが正常に完了しました")

        except Exception as e:
            self.logger.error(f"予期せぬエラーが発生しました: {str(e)}", exc_info=True)
            raise

def main():
    controller = GraphGenerationController()
    controller.run_process()

if __name__ == "__main__":
    main()
