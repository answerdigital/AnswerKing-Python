# AnswerKing-Python
Answer King Python App
***
### Requirements:
- #### Python 3.10+
- #### Poetry
  - Uses `pyproject.toml` to build a virtual environment and installs all necessary packages
  - Follow installation documentation to configure Poetry for Windows https://python-poetry.org/docs/
- #### node.js
  - Required by `pyright` package to detect and verify correct types have been used in the codebase
- #### Docker
  - Used to set up a disposable local MySQL database quickly.
    - Install Docker following the docs [here](https://docs.docker.com/get-docker/).
- ### Ubuntu
    - dependencies:  python3.10 git curl libmysqlclient-dev build-essential python3.10-dev

***
### Installation:
- Open root folder and run command `poetry install`
- This will install a virtual environment to a path that looks like this `C:\Users\Username\AppData\Local\pypoetry\Cache\virtualenvs`. Alternatively, run command `poetry env info` or `poetry show -v`in the folder containing `pyproject.toml` and this will display where the virtual environment was installed

### Setup
- Add the required environment variables. The easiest ways to do this is with a .env file which can be provided by another member of the team.
- Install the required MySQL container using `docker compose up -d`
- Migrate the database using `poetry run python manage.py migrate`

### Run:
- Run program using `poetry run python manage.py runserver`
***
### Test:
- Test program using `poetry run python manage.py test`

***
### Development:
Commands for maintaining consistency and PEP8 standards across codebase, as well as checking code coverage.
- #### pyright:
  - `poetry run pyright`
- #### black:
  - Run in root folder `poetry run black .`
    - To follow PEP8 guidelines for line length `poetry run black --line-length=79 .`
- #### pycodestyle:
  - Run in root folder `poetry run pycodestyle .`
    - To ignore `E501 line too long` error as this will be handled by `black`. Run `poetry run pycodestyle --ignore=E501 .`
- #### coverage:
  - Test using coverage `poetry run coverage run manage.py test`
    - View coverage report in the terminal `poetry run coverage report`
    - Generate interactive coverage file to view in a browser `poetry run coverage html`, then open `htmlcov/index.html`

***
### Docker:
To view the python backend application we can spin up the app on docker. To do this ensure docker is installed then:
- create a .env.production file containing (filling out the database password with your chosen password):
```
DATABASE_NAME=answerking_app
DATABASE_HOST=host.docker.internal
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASS=
SECRET_KEY="django-insecure-x977=v5a2q-e%_5$b9ge@jzk%s_nhk2l8_use&h@*m$w33dopr"
DJANGO_SETTINGS_MODULE=answerking.settings.base
DATABASE_ENGINE="django.db.backends.mysql"
```
- run in git bash :
  - `docker compose build`
  - `docker compose --env-file .env.production up` (This runs your built image with the .env.production variables)

- send HTTP requests to 127.0.0.1:8000

***
### Swagger:
To view the AnswerKing Python API documentation in Swagger as per OpenAPI specification, visit the following URL while
 your local server is running: http://127.0.0.1:8000/api/schema/swagger-ui/

