import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import re

century_column_name = 'Век'
freq_column_name = 'Частота'


def dataframe_century_objects(original_cultural_sites):
    """
    Функция преобразования датафрейма со всеми данными в датафрейм с двумя столбцами:
    уникальными значениями веков и частотой их повторения среди объектов.
    :param original_cultural_sites: датафрейм со всеми данными.
    :return: датафрейм с веками и их частотой.
    """
    century_counts = pd.DataFrame()

    def convert_to_century(date):
        """
        Функция приведения всех дат к веку.
        :param date: изначальное значение даты.
        :return: дата в формате века, если даты нет, то возвращается 0.
        """
        match = re.search(r'\b\d{2}(\d{2})?\b', str(date))
        if date and match:
            year = match.group(0)
            if len(year) == 2:
                return int(year)
            elif len(year) == 4:
                century = int(year) // 100 + 1
                return int(century)
        return 0

    century_counts[century_column_name] = original_cultural_sites['Построен'].apply(convert_to_century)
    century_counts = century_counts[century_counts[century_column_name].notna()]

    century_counts = century_counts[century_column_name].value_counts().reset_index()
    century_counts.columns = [century_column_name, freq_column_name]
    return century_counts.sort_values(by=century_column_name)


def frequency_century_graph(century_freq):
    """
    Построение графика распределения частоты постройки в разные века.
    :param century_freq: датафрейм с данными о веках постройки объектов
                         и количеством объектов, построенных в этот век.
    :return: график.
    """

    # Настройка графика
    x_values = list(range(0, len(century_freq)))
    y_values = century_freq[freq_column_name]
    x_labels = century_freq[century_column_name]

    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, marker='o', linestyle='-')
    plt.xlabel(century_column_name)
    plt.ylabel(freq_column_name)
    plt.title('Распределение веков постройки среди объектов')
    plt.xlim(0, len(x_labels) - 1)
    plt.xticks(x_values, x_labels, rotation=90)
    plt.grid(True, linestyle='--')
    plt.yticks(y_values)

    for x, y in zip(x_labels, y_values):
        plt.axvline(x=x, color='gray', linestyle='--', linewidth=0.5)
        plt.axhline(y=y, color='gray', linestyle='--', linewidth=0.5)

    plt.show()


def point_map_of_districts(cultural_sites):
    """
    Функция постройки точечной карты распределения координат объектов по районам СПб.
    :param cultural_sites: оригинальный датафрейм с координатами.
    :return: карта.
    """
    
    x = cultural_sites['Координата X (м, система координат СК-1964)']
    y = cultural_sites['Координата Y (м, система координат СК-1964)']
    districts = cultural_sites['Район']

    # Распределение цветов по району
    colors = {
        'Адмиралтейский': 'blue',
        'Василеостровский': 'red',
        'Выборгский': 'green',
        'Калининский': 'orange',
        'Кировский': 'purple',
        'Колпинский': 'cyan',
        'Красногвардейский': 'magenta',
        'Петроградский': 'yellow',
        'Красносельский': 'pink',
        'Кронштадтский': 'brown',
        'Курортный': 'gray',
        'Московский': 'teal',
        'Невский': 'olive',
        'Петродворцовый': 'navy',
        'Приморский': 'maroon',
        'Пушкинский': 'lime',
        'Фрунзенский': 'silver',
        'Центральный': 'aqua',
    }

    # Настройка графика
    plt.figure(figsize=(10, 8))
    for district, color in colors.items():
        mask = (districts == district)
        plt.scatter(x[mask], y[mask], label=district, c=color, marker='o')

    plt.title('Точечная карта координат объектов с учетом районов')
    plt.xlabel('Координата X')
    plt.ylabel('Координата Y')
    plt.legend()
    plt.show()


def no_authors_freq():
    """
    Функция построения кольцевого графика по встречаемости объектов с утерянным авторством в каждом веке.
    :return: график.
    """
    # Чтение датафрейма с двумя столбцами: век объекта и его автор.
    file = pd.read_excel('data/century_author.xlsx')

    # Не учитываем данные, у которых неизвестен век или установлен автор.
    filtered_data = file[(file['Автор'] == 'автор не установлен') & (file['Век'] != 0)]
    century_counts = filtered_data['Век'].value_counts()

    visual_author_data = pd.DataFrame({'Век': century_counts.index, 'Частота': century_counts.values})
    visual_author_data = visual_author_data.sort_values(by='Век')

    # Настройка графика
    cmap = plt.cm.get_cmap('Blues')
    colors = cmap([0.1, 0.3, 0.5, 0.7])
    plt.figure(figsize=(8, 8))
    plt.pie(visual_author_data['Частота'], labels=visual_author_data['Век'], autopct='%1.1f%%', colors=colors)
    plt.title('Количество объектов с неизвестным автором за век')

    plt.axis('equal')
    plt.show()


def visual_data(cultural_sites):
    """
    Функция вызова всех ф-ций, связанных с построением графика.
    :param cultural_sites: датафрейм, данные которого будут визуализироваться.
    :return: графики
    """
    point_map_of_districts(cultural_sites)
    frequency_century_graph(dataframe_century_objects(cultural_sites))
    no_authors_freq()
