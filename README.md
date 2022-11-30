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
- create a .env_deploy file:
```
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASS=
DATABASE_HOST=
DATABASE_PORT=
SECRET_KEY=
DJANGO_SETTINGS_MODULE=
```
- run : `docker compose --env-file .env_deploy up`
