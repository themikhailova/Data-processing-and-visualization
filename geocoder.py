import pandas as pd
import requests

file_path = 'converted_coordinates.xlsx'  # путь к файлу
sheet_name = 'Sheet1'
df = pd.read_excel(file_path, sheet_name=sheet_name)
adress_column = df['Адрес']
column_data = adress_column.tolist()

all_data = []
for column in column_data:
    adress = column
    url = f'https://geocode.gate.petersburg.ru/parse/free?street={adress}'
    # заголовок для получения ответа в формате JSON
    headers = {'accept': 'application/json'}
    # GET-запрос
    response = requests.get(url, headers=headers)

    if response.status_code == 200:  # проверка успешности запроса
        data = response.json()
        if 'Building_ID' in data:
            building_id = data['Building_ID']
            name = data['Name']
            appending = [name, building_id]
            all_data.append(appending)
        else:
            print("Ключ 'Building_ID' не найден в JSON-ответе.")
            appending = [adress, 'Не найдено']
            all_data.append(appending)
    else:
        print(f"Ошибка запроса: {response.status_code}")

result_df = pd.DataFrame(all_data, columns=["Name", "Building_ID"])
output_file = "output.xlsx"
result_df.to_excel(output_file, index=False)

