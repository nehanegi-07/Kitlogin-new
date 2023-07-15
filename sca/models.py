from ctypes import pythonapi
from django.db import models

# Create your models here.
export DEBUG=1
pythonapi manage.py makemigrations && python manage.py migrate
	set DEBUG=1 python manage.py migrate

set DEBUG=1 python manage.py migrate_clickhouse 

