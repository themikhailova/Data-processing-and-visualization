import re


def full_date_form(date, pattern, pattern_reverse, form_result):
    """
    Функция замены сокращений в., пол. и чет.
    :param date: изначальная форма даты из датафрейма
    :param pattern: паттерн, по которому происходит сравнение даты
    :param pattern_reverse: паттерн с измененным порядком его частей
    :param form_result: форма результирующей строки, которая ожидается после выполнения функция
    :return: исправленная дата
    """
    correct_date = ""

    def replace(match, part_index, year_index):
        """
        Замена сокращенной формы записи даты на полную
        :param match: совпадающая часть у pattern и date
        :param part_index: индекс той части, где обозначается четверть/половина века
        :param year_index: индекс той части, где обозначается номер века
        :return: дата с полной записью четверти/половины века
        """
        if match.lastindex >= 2:
            return form_result.format(match.group(part_index), match.group(year_index))

    # Проверка на то, есть ли в записи совпадение заданными паттернами
    if re.match(pattern, date):
        correct_date = re.sub(pattern, lambda match: replace(match, 1, 2), date)

    if re.match(pattern_reverse, date):
        correct_date = re.sub(pattern_reverse, lambda match: replace(match, 2, 1), date)

    return correct_date


def replace_abbreviations(date):
    """
    Функция замены сокращений на полную форму слов.
    :param date: дата, в которой необходимо устранить сокращения
    :return: корректный формат даты без сокращений
    """
    abbreviations = dict(zip(["кон.", "сер.", "в.", "нач."], ["конец", "середина", "век", "начало"]))

    for abb, full in abbreviations.items():
        if abb in date:
            date = date.replace(abb, full)
    return date


def date_standardization(original_date):
    """
    Стандартизация даты под заданный формат
    :param original_date: сырая дата из датафрейма
    :return: стандартизированная дата
    """

    result_date = original_date

    if ";" in original_date:
        result_date = result_date.replace(";", ",")

    if "пол." in original_date:
        result_date = full_date_form(result_date, pattern=r"(\d+)-я пол\. (\d+) в\.",
                                     pattern_reverse=r"(\d+) в\. (\d+)-я пол\.",
                                     form_result="{}-я половина {} века")
    if "четв." in original_date:
        result_date = full_date_form(result_date, pattern=r"(\d+)-я четв\. (\d+) в\.",
                                     pattern_reverse=r"(\d+) в\. (\d+)-я четв\.",
                                     form_result="{}-я четверть {} века")

    # Замена сокращений на полные формы
    result_date = replace_abbreviations(result_date)

    return result_date
