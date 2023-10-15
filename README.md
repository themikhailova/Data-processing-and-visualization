# Data-processing-and-visualization
Тестовое задание для аналитика данных

Найти само задание можно в файле 'Аналитика данных.docx'

Файлы:

[main.py](https://github.com/themikhailova/Data-processing-and-visualization/blob/main/main.py) - основная часть кода, содержащая выполнение всех этапов задания и вызывающая прочие файлы.

[data_transform.py](https://github.com/themikhailova/Data-processing-and-visualization/blob/main/data_transform.py) - функции стандартизации столбца "Построен". 

[vis_part.py](https://github.com/themikhailova/Data-processing-and-visualization/blob/main/vis_part.py) - построение трех графиков, требуемых по заданию.

В папке [data](https://github.com/themikhailova/Data-processing-and-visualization/blob/main/vis_part.py) содержатся все файлы с данными, необходимыми в процессе работы с кодом:
Файлы [all.xlsx](https://github.com/themikhailova/Data-processing-and-visualization/blob/main/data/all.xlsx) и [composite.xlsx](https://github.com/themikhailova/Data-processing-and-visualization/blob/main/data/composite.xlsx) являются входными и содержат список полных объектов и составных соответственно.

Файл [century_author.xlsx](https://github.com/themikhailova/Data-processing-and-visualization/blob/main/data/century_author.xlsx) содержит все даты в формате веков и авторов объектов. Используется для визуализации круговой диаграммы.

Файл [output.xlsx](https://github.com/themikhailova/Data-processing-and-visualization/blob/main/data/output.xlsx) содержит результат работы кода.

Визуализация:

Точечная карта координат объектов с учетом районов

Карта показывает расположение объектов, разделяя их на районы. Значительная часть представленных объектов расположена в Петроградском, Колпинском, Василеостровском и Адмиралтейском районах. В Курортном, Красносельском, Кронштадтском и Колпинском районе плотность расположения объектов меньше.

![image](https://github.com/themikhailova/Data-processing-and-visualization/assets/91223359/c4f1d725-fcc1-404e-bbe6-c68d4238959c)

 
Временной ряд для распределения веков постройки среди объектов

Пик застройки приходится на 19 век – 3663 объекта. Значение в точке 0 означает количество объектов с неизвестной датой постройки. Можно предположить, что после 17 века сохранилось больше документации, подтверждающей дату постройки различных объектов, а также технологии постройки улучшаются и используются более прочные материалы, что позволило большему числу объектов сохраниться. 

![image](https://github.com/themikhailova/Data-processing-and-visualization/assets/91223359/12b78de5-a611-4fe5-8d75-c2dd67c9bb7f)

 
Круговая диаграмма для сравнения количества неизвестных авторов объектов по векам

Рассматривая 4 века и сравнивая предыдущую и данную диаграммы, можно сделать вывод, что времена, имеющее большее количество новых построек также лидируют по числу утраченных данных по авторам объектов. 

 ![image](https://github.com/themikhailova/Data-processing-and-visualization/assets/91223359/f29a4c0e-2ecf-47b7-a405-0fcb90c4d3c6)

