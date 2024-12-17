import pandas as pd

def read_csv_file(filepath, encoding='cp932'):
    try:
        df = pd.read_csv(filepath, encoding=encoding)
        return df
    except Exception as e:
        print(f"ファイルの読み込みに失敗しました: {e}")
        return None

def transpose_and_process_data(df):
    # データフレームを転置
    df_transposed = df.T

    # 転置した後のデータフレームの列名をリセット（元々の行名が列名になる）
    df_transposed.reset_index(inplace=True)
    df_transposed.rename(columns={'index': 'Original Column Names', 0: 'Data'}, inplace=True)

    # 'Time' を含む行を抽出
    time_rows = df_transposed[df_transposed['Original Column Names'].str.contains('Time')]

    if not time_rows.empty:
        print("Timeを含む行のデータ:")
        print(time_rows)
    else:
        print("エラー: 'Time'という文字列を含む行が見つかりませんでした。")

def main():
    # 具体的なファイルパスを設定
    filepath = r"C:\Users\QC07\OneDrive - トーヨーセフティホールディングス株式会社\QC_試験グラフ作成\CSV\2024-04-19_TestLOG.CSV"
    df = read_csv_file(filepath)
    if df is not None:
        transpose_and_process_data(df)

if __name__ == '__main__':
    main()
