import pandas as pd


def parse_author_info(info):
    result = info
    if "арх." in info:
        result = result.replace("арх.", "архитектор")
    if "инж." in info:
        result = result.replace("инж.", "инженер")
    if "ск." in info:
        result = result.replace("ск.", "скульптор")
    if "худ." in info:
        result = result.replace("худ.", "художник")
    if "воен." in info:
        result = result.replace("воен.", "военный ")
    if "гражд." in info:
        result = result.replace("гражд.", "гражданский ")
    return result


file_path = 'date_transform.xlsx'
sheet_name = 'Sheet1'
df = pd.read_excel(file_path, sheet_name=sheet_name)

for index, value in enumerate(df['Автор_x']):
    if df.at[index, 'Автор_x'] is not None:
        df.at[index, 'Автор_x'] = parse_author_info(str(df.at[index, 'Автор_x']))

df.to_excel('all_transform.xlsx', index=False)
