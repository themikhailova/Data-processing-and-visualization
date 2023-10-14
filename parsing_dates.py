import pandas as pd
import re


def two_or_four(text):
    text = str(text)

    if not text:
        return 0  # 0 для пустых значений

    # выражение для поиска
    match = re.search(r'\b\d{2}(\d{2})?\b', text)
    if match:
        year = match.group(0)
        if len(year) == 2:
            return int(year)
        elif len(year) == 4:
            century = int(year) // 100 + 1
            return int(century)
    else:
        return 0


def process_excel_file(input_file, output_file):
    df = pd.read_excel(input_file)

    df['FirstNumber'] = df['Построен'].apply(two_or_four)
    df = df[df['FirstNumber'].notna()]
    df[['FirstNumber']].to_excel(output_file, index=False)


input_file = 'all_transform.xlsx'
output_file = 'parsing_dates.xlsx'
process_excel_file(input_file, output_file)
