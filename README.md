# k1logram-test-o-parser

Для запуска проекта: 

установите библиотеки командой pip install -r requirements.txt

запустите сервер MySQL и redis

вставьте свои данные в файл settings.py DATABASES 

введите в терминал 

python manage.py runserver &

python telegram_bot.py &

celery -A parser.celery:app worker --loglevel=INFO &
