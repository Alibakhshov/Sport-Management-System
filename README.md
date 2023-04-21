# UCA-Sport-Management-System

## Introduction
This is a project for the course of Software Engineering at UCA. The project is a sport management system for a gym. The system is able to manage the users, the trainers, the classes, the payments and the subscriptions. The system is also able to generate reports and statistics.

## Installation
To install the project you need to have installed the following programs:
- [python](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [django](https://docs.djangoproject.com/en/3.1/topics/install/)


Once you have installed the programs, you need to clone the repository and create a virtual environment. To do that, you need to run the following commands:
```bash
git clone
cd UCA-Sport-Management-System
virtualenv venv
```

Then, you need to activate the virtual environment and install the dependencies:
```bash

source venv/bin/activate

pip install -r requirements.txt
```

Finally, you need to run the migrations and start the server:
```bash

python manage.py migrate

python manage.py runserver
```

## Usage

To use the system, you need to create a superuser:
```bash

python manage.py createsuperuser
```

Then, you need to go to the admin page and create the objects that you need. To do that, you need to go to the following url:
```

http://localhost:8000/admin
```

To use the system, you need to go to the following url:
```

http://localhost:8000
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
```


            
    