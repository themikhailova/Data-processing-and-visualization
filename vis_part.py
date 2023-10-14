import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.cm as cm


def time_ser():
    file = 'parsing_dates_century.xlsx'
    column_name = 'Век'
    df = pd.read_excel(file, names=[column_name])
    value_counts = df[column_name].value_counts().reset_index()
    value_counts.columns = ['Век', 'Частота']
    value_counts = value_counts.sort_values(by='Век')

    start_x = 0
    end_x = len(value_counts)
    x_values = range(start_x, end_x)
    x_labels = value_counts['Век']
    y_values = value_counts['Частота']

    plt.figure(figsize=(10, 6))
    plt.plot(x_values, value_counts['Частота'], marker='o', linestyle='-')
    plt.xlabel('Век')
    plt.ylabel('Частота')
    plt.title('Распределение веков постройки среди объектов')
    plt.xlim(0, len(x_labels) - 1)
    plt.xticks(x_values, x_labels, rotation=90)
    plt.grid(True, linestyle='--')

    plt.yticks(y_values)

    for x, y in zip(x_labels, y_values):
        plt.axvline(x=x, color='gray', linestyle='--', linewidth=0.5)
        plt.axhline(y=y, color='gray', linestyle='--', linewidth=0.5)
    plt.show()


def dot_map():
    data = pd.read_excel('all_transform.xlsx')

    x = data['Координата X (м, система координат СК-1964)']
    y = data['Координата Y (м, система координат СК-1964)']

    raions = data['Район']
    # каждый район с уникальным цветом
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

    plt.figure(figsize=(10, 8))
    for raion, color in colors.items():
        mask = (raions == raion)
        plt.scatter(x[mask], y[mask], label=raion, c=color, marker='o')

    plt.title('Точечная карта координат объектов с учетом районов')
    plt.xlabel('Координата X')
    plt.ylabel('Координата Y')
    plt.legend()
    plt.show()


def no_authors_freq():
    file = pd.read_excel('parsing_dates.xlsx')

    filtered_data = file[(file['Автор'] == 'автор не установлен') & (file['FirstNumber'] != 0)]
    first_number_counts = filtered_data['FirstNumber'].value_counts()

    data_frame = pd.DataFrame({'FirstNumber': first_number_counts.index, 'Частота': first_number_counts.values})
    data_frame = data_frame.sort_values(by='FirstNumber')

    colors = plt.cm.Blues([0.1, 0.3, 0.5, 0.7])
    plt.figure(figsize=(8, 8))
    plt.pie(data_frame['Частота'], labels=data_frame['FirstNumber'], autopct='%1.1f%%', colors=colors)
    plt.title('Количество объектов с неизвестным автором за век')

    plt.axis('equal')
    plt.show()


dot_map()
time_ser()
no_authors_freq()
