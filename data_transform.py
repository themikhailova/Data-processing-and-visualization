import re
import pandas as pd


def convert_half(text):
    # паттерн для поиска "n-я пол. m в." или "m в. n-я пол."
    pattern = r"(\d+)-я пол\. (\d+) в\."
    pattern2 = r"(\d+) в\. (\d+)-я пол\."

    # замена частей строк
    def replace(match):
        if match.lastindex >= 2:
            year = match.group(2)
            return f"{match.group(1)}-я половина {year} века"

    def replace2(match):
        if match.lastindex >= 2:
            year = match.group(1)
            return f"{match.group(2)}-я половина {year} века"

    match1 = re.match(pattern, text)
    if match1:
        result = re.sub(pattern, replace, text)
        # дополнительная замена в строке, если нужно
        if "кон." in result:
            result = replace_kon(result)
        if "нач." in result:
            result = replace_nach(result)
        return result
    match2 = re.match(pattern2, text)
    if match2:
        result = re.sub(pattern2, replace2, text)
        # дополнительная замена в строке, если нужно
        if "кон." in result:
            result = replace_kon(result)
        if "нач." in result:
            result = replace_nach(result)
        return result

def convert_quarter(text):
    # паттерн для поиска "n-я четв. m в." или "m в. n-я четв."
    pattern = r"(\d+)-я четв\. (\d+) в\."
    pattern2 = r"(\d+) в\. (\d+)-я четв\."

    # замена частей строк
    def replace(match):
        if match.lastindex >= 2:
            year = match.group(2)
            return f"{match.group(1)}-я четверть {year} века"

    def replace2(match):
        if match.lastindex >= 2:
            year = match.group(1)
            return f"{match.group(2)}-я четверть {year} века"

    match1 = re.match(pattern, text)
    if match1:
        result = re.sub(pattern, replace, text)
        # дополнительная замена в строке, если нужно
        if "кон." in result:
            result = replace_kon(result)
        if "нач." in result:
            result = replace_nach(result)
        return result
    match2 = re.match(pattern2, text)
    if match2:
        result = re.sub(pattern2, replace2, text)
        # дополнительная замена в строке, если нужно
        if "кон." in result:
            result = replace_kon(result)
        if "нач." in result:
            result = replace_nach(result)
        return result

def transform_to_list(text):
    # паттерн для поиска годов и годовых диапазонов
    pattern = r"(\d{4}|\d{1,4}-\d{4})"

    # нахождение совпадений
    matches = re.findall(pattern, str(text))
    result = []
    if matches:
        for match in matches:
            if "-" in match:
                start_year, end_year = map(int, match.split("-"))
                result.append(f"{start_year}-{end_year}")
            else:
                result.append(int(match))
    return result

def replace_kon(text):
    result = text.replace("кон.", "конец")
    if "нач." in result:
        result = result.replace("нач.", "начало")
    if "сер." in result:
        result = result.replace("сер.", "середина")
    if "в." in result:
        result = result.replace("в.", "век")
    return result

def replace_nach(text):
    result = text.replace("нач.", "начало")
    if "кон." in result:
        result = result.replace("кон.", "конец")
    if "сер." in result:
        result = result.replace("сер.", "середина")
    if "в." in result:
        result = result.replace("в.", "век")
    return result

def parse_year_info(info):
    result = info
    if ";" in info:
        result = result.replace(";", ",")
    if "пол." in info:
        result = convert_half(result)
    elif "четв." in info:
        result = convert_quarter(result)
    elif "кон." in info:
        result = replace_kon(result)
    elif "нач." in info:
        result = replace_nach(result)
    else:
        result = transform_to_list(result)
        result = [str(item) for item in result]
        return ", ".join(result)
    return result


file_path = 'data.xlsx'
sheet_name = 'Sheet1'
df = pd.read_excel(file_path, sheet_name=sheet_name)

for index, value in enumerate(df['Построен']):
    if df.at[index, 'Построен'] is not None:
        df.at[index, 'Построен'] = parse_year_info(str(df.at[index, 'Построен']))

df.to_excel('date_transform.xlsx', index=False)


