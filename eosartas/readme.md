postgres$ psql		CREATE DATABASE testdb
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic

Make venv see system-installed python packages:
python -m venv --system-site-packages myenv 
Prevent automatic installation of dependencies:
pip install --no-deps
