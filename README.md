# Установка
git clone https://github.com/your-username/item-trading.git
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