# yandex-dzen-words-parser

Парсер статей с Яндекс Дзен, который ищет статьи с желаемыми словами в заголовках и в аннотациях.
По итогу формирует облако слов и сохраняет этот рисунок в папку **wordclouds**. [Пример](./wordclouds/wordcloud_1696128090.210268.png)

Для парсинга сайта использован **Selenium**, для анализа слов **nltk** и для создания облака слов **wordcloud**.

## Запуск

Для начала, необходимо создать виртуальную среду, активировать её и установить необходимые пакеты: 
```
python3 -m venv venv
venv\scripts\activate.ps1  # Windows и Powershell
# venv\scripts\activate.bat  # Windows и CMD
# source venv/bin/activate   # Linux
pip install -r requirements.txt
```

Также, в **venv** нужно создать папку **nltk_data**: `mkdir venv/nltk_data`

После этого, нужно запустить скрипт [nltk_init.py](./src/nltk_init.py) из любой директории:
```
python3 src/nltk_init.py
```
Скрипт загрузит необходимые для работы стоп-слова и знаки пунктуации

После всех этих действий, скрипт можно запустить командой: `python3 app.py`