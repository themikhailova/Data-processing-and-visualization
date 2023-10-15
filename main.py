import pandas as pd
import requests

from config import file_all, file_compos, transformer
from data_transform import date_standardization
from vis_part import visual_data

"""
СПб ГУП «ИАЦ»: Тестовое задание для аналитика данных.
Задачи:
1) Совмещение датасетов
2) Перевод координат из системы МСК-64 в WSG84 
3) Парсинг геокода адресов
4) Стандартизация данных
5) Визуализация данных.
"""


def merge_files(all_data, compose_data):
    """
    Обновление данных в файле всех объектов данными из файла составных объектов
    :param all_data: датафрейм со всеми объектами
    :param compose_data: датафрейм с составными объектами
    :return: совмещенный файл
    """
    # Соединение по столбцу "Код ОКН" и "Код объекта"
    update_data = all_data.merge(compose_data, left_on='Код ОКН', right_on='Код объекта', how='outer')
    update_data['Код ОКН'] = update_data['Код ОКН'].fillna(update_data['Код объекта'])

    # Замена значений столбцов 'Наименование объекта' и 'Адрес',
    # оставляя только значения из compose_data, если они не пусты
    update_data['Наименование объекта'] = update_data['Наименование ОКН'] \
        .combine_first(update_data['Наименование объекта'])
    update_data['Адрес'] = update_data['Адрес_КЗР'].combine_first(update_data['Адрес'])

    # Удаление лишних столбцов
    update_data.drop(['Код объекта', 'Наименование ОКН', 'Адрес_КЗР',
                      'Дата постройки', 'Кат_охраны', 'Основание',
                      'Кадастровый номер_y', 'Автор_y'], axis=1, inplace=True)

    # Сортировка столбцов
    new_order = ['id'] + [col for col in update_data.columns if col not in ['id']]

    return update_data[new_order]


def convert_coordinates(row):
    """
    Функция перевода координат из системы МСК-64 в WSG84
    :param row: строка датафрейма, координаты которой будут преобразованы.
    :return: столбцы с переведенными координатами
    """
    lon, lat = transformer.transform(row['Координата X (м, система координат СК-1964)'],
                                     row['Координата Y (м, система координат СК-1964)'])
    return pd.Series({'Latitude': lat, 'Longitude': lon})


def get_geocode(all_addresses):
    """
    Функция парсинга геокода с сайта
    :param all_addresses: столбец адресов из датафрейма
    :return: массив Building_ID для каждого адреса
    """
    geocodes = []
    headers = {'accept': 'application/json'}

    for address in all_addresses:
        url = f'https://geocode.gate.petersburg.ru/parse/free?street={address}'
        response = requests.get(url, headers=headers)
        # Проверка успешности запроса
        if response.status_code == 200:
            data = response.json()
            if 'Building_ID' in data:
                geocodes.append(data['Building_ID'])
            else:
                # Если Building_ID отсутствует для адреса на сайте,
                # то это будет отображено в датафрейме
                geocodes.append('Не найдено')
        else:
            print(f"Ошибка запроса: {response.status_code}")

    return geocodes


def authors_standardization(author):
    """
    Функция замены сокращений в столбце Автор на полные наименования профессий.
    :param author: значение ячейки в столбце Автор
    :return: обновленное значение ячейки без сокращений
    """
    abbreviations = dict(zip(["арх.", "инж.", "ск.", "худ.", "воен.", "гражд."],
                             ["архитектор", "инженер", "скульптор", "художник", "военный ", "гражданский "]))
    for abb, full in abbreviations.items():
        if abb in author:
            author = author.replace(abb, full)

    return author


if __name__ == '__main__':
    # Загрузка данных и объединение таблиц
    chs_all = pd.read_excel(file_all)
    chs_all['id'] = range(1, len(chs_all) + 1)
    cultural_sites = merge_files(chs_all, pd.read_excel(file_compos))

    # Перевод координат в систему WSG84
    cultural_sites[['Latitude', 'Longitude']] = cultural_sites.apply(convert_coordinates, axis=1)

    # Добавление в таблицу колонки геокода с сайта
    addresses = cultural_sites['Адрес'].tolist()
    cultural_sites['Building_ID'] = get_geocode(addresses)

    # Стандартизация колонок с авторами и временем постройки
    for index, _ in enumerate(cultural_sites['Автор_x']):
        if cultural_sites.at[index, 'Автор_x'] is not None:
            cultural_sites.at[index, 'Автор_x'] = authors_standardization(str(cultural_sites
                                                                              .at[index, 'Автор_x']))
        if cultural_sites.at[index, 'Построен'] is not None:
            cultural_sites.at[index, 'Построен'] = date_standardization(str(cultural_sites
                                                                            .at[index, 'Построен']))

    # Сохранение полученной таблицы в файл
    cultural_sites.to_excel("data/output.xlsx", index=False)

    # Визуализация полученных данных
    visual_data(cultural_sites)
