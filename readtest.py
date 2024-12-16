import os

directory = r'C:\Users\QC07\TSホールディングス株式会社\OfficeScriptの整理 - ドキュメント\QC_グラフ作成'
files = os.listdir(directory)
print("ディレクトリ内のファイルリスト:")
for file in files:
    print(file)



def write_data_to_sheet(sheet, data_frame, start_row, start_col):
    """データフレームの内容をExcelシートに転記する"""
    for index, row in data_frame.iterrows():
        for col_index, value in enumerate(row, start=1):  # Excelの列は1から始まる
            sheet.cell(row=start_row + index, column=start_col + col_index - 1).value = value
