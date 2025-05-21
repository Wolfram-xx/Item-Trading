# Установка
git clone https://github.com/Wolfram-xx/Ttem-Trading.git
cd item-trading

# Создаём виртуальное окружение
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows

# Устанавливаем зависимости
pip install -r requirements.txt

# Настройка БД
python manage.py makemigrations
python manage.py migrate

# Запуск
python manage.py runserver
