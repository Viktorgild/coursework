# Учебный проект по Python.

# Описание проекта:
Данный проект нужен для работы обработки и дальнейших работ с банковскими данными.

Приложение анализирует транзакции, которые находятся в Excel-файле.
Приложение будет генерировать JSON-данные для веб-страниц, формировать Excel-отчеты,
а также предоставлять другие сервисы.

## В приложении присутствуют следующие функции:

1. get_transactions: функция для получения текущего курса акций, информацию об наименовании акций получает из json файла 
либо из пользовательского ввода.
2. get_exchange_rates: функция для получения текущего курса валют, информацию о нужных валютах получает из json файла.
3. greetings: функция, которая выводит приветствие исходя из текущего времени суток.
4. calculate_card_details: функция для расчёта последних 4 цифр номера карты, общей суммы расходов и кешбэка 
для каждой карты.
5. top_transactions: функция выдает топ-5 транзакций по сумме платежа.
6. analyze_cashback: функция позволяет проанализировать, какие категории были наиболее выгодными для выбора
в качестве категорий повышенного кешбэка.
7. generate_report: функция возвращает траты по заданной категории за последние три месяца (от переданной даты).

## Для проверки кода использовались линкеры и тесты:
* pytest
* flake8
* isort
* mypy

## Установка:
1. Клонируйте репозиторий:
```
https://github.com/Viktorgild/Projekt
```
2. Установите зависимости:
```
pip install -r requirements.txt
```

## Разработчик:

https://github.com/Viktorgild