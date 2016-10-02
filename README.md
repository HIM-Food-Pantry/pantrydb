
## Installation

### Quick start Dev

Install Dependencies and Project

1. `python3 -m venv ~/.virtualenvs/him_database`
2. `source ~/.virtualenvs/him_database/bin/activate`
3. `git clone git clone https://github.com/ncrmro/him_database`
4. `pip3 install requirements/development.txt`

Run Migrations and Start Web Server

1. `cd src`
2. `python3 manage.py migrate`
3. `python3 manage.py runserver`

Run Tests and Lint

1. `python3 manage.py test --settings=him_database.settings.testing`
2. `prospector`

### Production

See [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) for more.
