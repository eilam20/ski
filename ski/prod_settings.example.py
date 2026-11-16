# Copy this file to ski/prod_settings.py on PythonAnywhere (it is gitignored).
# Fill in your MySQL database details from the PythonAnywhere "Databases" tab.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eilam20$ski_db',          # Format: <username>$<dbname>
        'USER': 'eilam20',                 # Your PythonAnywhere username
        'PASSWORD': 'YOUR_MYSQL_PASSWORD', # Your MySQL password
        'HOST': 'eilam20.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'CONN_MAX_AGE': 60,                # Reuse DB connections across requests
        'OPTIONS': {
            'charset': 'utf8mb4',          # Required for Hebrew & emojis
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

