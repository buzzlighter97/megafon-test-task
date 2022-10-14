# megafon-test-task

ENG

Functionality:

* parses given city forecast info for the next 7 days from yandex.ru/pogoda/{city name}/details;

* calculates average daytime temperature;

* checks if there's steep change in air pressure (more than 5 mm Hg);

Result: open .xlsx file with forecast information stored in excel_files/ directory.

Start: 
console start following pattern
```python main.py {city name in english notation}```

OR

average run with console city name input



RU

Функционал:

* парсит прогноз погоды на неделю в переданном городе из yandex.ru/pogoda/{название города}/details;

* вычисляет среднесуточную температуру;

* проверяет, будет ли заметное изменение атмосферного давления (больше 5 мм. рт. ст.);

Результат: открытый .xslx файл с прогнозом погоды, сохранённый в папке excel_files/

Старт:
запуск в консоли по шаблону
```python main.py {название города на английском}```

ИЛИ

стандартный запуск с передачей названия города в консоль
