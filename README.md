## CSVファイルをグラフ生成用ファイルに転記する。

## 概要

このシステムは、HIOKI測定器からのCSVデータを読み取り、グラフ生成用ファイルに転記するプログラムです。

## ディレクトリ構造

```
ROOT_DIR/
├─scripts/
│  └─start_graph_generator.bat
├─src/
│  ├─csvimport.py
│  ├─csvpivot.py
│  └─csvtoxlsxconverter.py
├─tests/
│  ├─Excel/
│  └─test_data/
│      ├─CSV/
│      ├─CSV_LOG/
│      ├─EXCEL/
│      ├─logs/
│      ├─OUTPUT/
│      ├─PROCESSED/
│      └─templates/
└─☆Excel/
```

## 主要コンポーネント

### 1. CSVインポート (csvimport.py)

- HIOKIデバイスからUSBドライブ（S:, U:, T:）のCSVファイルを読み取り
- データを結合して単一のCSVファイルを作成
- 処理済みデータをCSVフォルダとCSV_LOGフォルダに保存
- 元のUSBドライブ上のファイルを削除

### 2. CSVピボット処理 (csvpivot.py)

- CSVフォルダ内の「InspectionLOG」ファイルを処理
- データの転置と特定順序でのソート（HEL_TOP、HEL_ZENGO等）
- 処理結果をOUTPUTフォルダに保存
- 処理済みファイルをPROCESSEDフォルダに移動

### 3. Excel変換 (csvtoxlsxconverter.py)

- OUTPUTフォルダ内の「Output_」で始まるCSVファイルを処理
- データタイプに基づく適切なExcelテンプレートの選択
- データを対応するExcelシートに転記
- 結果を☆Excelフォルダに保存

## 使用方法

1. プログラムの起動
   
   - `scripts`フォルダ内の`start_sheet_generator.bat`を実行

2. データ処理の流れ
   
   - HIOKIデバイスからのCSVファイルを自動検出
   - データの変換と整形を自動実行
   - 最終的なExcelファイルを生成

## 出力ファイル

- 生成されたExcelファイルは`☆Excel`フォルダに保存
- ファイル名は処理されたデータタイプに基づいて自動生成
  例：`Bicycle_Helmet_グラフ作成用ファイル_0.xlsm`

## ログと一時ファイル

- 処理ログは`logs`フォルダに保存
- 中間生成ファイルは以下のフォルダで管理
  - CSV_LOG: バックアップ
  - PROCESSED: 処理済みファイル

## 注意事項

- プログラム実行前に所定のUSBメモリが正しく接続されていることを確認
- テンプレートファイルは`templates`フォルダに配置必須
- 30日以上経過した古いファイルは自動的に削除される設定

## テスト環境

- `tests/test_data`フォルダでテスト実行が可能
- 本番環境との切り替えは起動バッチファイルで制御
- まだ試していない。2024-12-24
