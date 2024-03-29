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
 
***
### CI pipeline
When raising a PR it goes through the Continuous Integration pipeline which has been implemented. This consists of two pipelines; one for Integration testing and one for static code anaylsis testing.

#### Static Code Analysis CI
This pipeline consists of the following checks:

- #### Black
  - This checks that the formating package black has been run on the code to format it in a consistent way acording to PEP 8 guidelines. The line length has been set to 79 characters.

- #### Pycodestyle
  - This checks that PEP 8 guidelines have been adhered to. We ignore error code E501 which is raised if the length of the line is over 82 characters long. This is ok to ignore as the previous `Black` check ensures that the line length is less than 79 characters where possible.
  
- #### Pyright
  - This checks that static type checking has been implemented properly.
  
- #### Unit tests
  - This runs the written unit tests against the PR code.
  
- #### SonarCloud
  - SonarCloud is also run agains the PR code and checks for non-optimal code (code smells), Bugs in the code, vulnerabilities in the code, and potential security issues in the code (security Hotspots). It also check duplicated code and code coverage. SonarCloud has been configured so that if there are any Code smells, Bugs, Vulnerabilities or Security Hotspots in the code the PR will be blocked until these are resolved. It is also set up to block the PR if the percentage duplication is above 4% or the code coverage is less than 80%.
  
#### Integration CI
This pipeline runs the integration tests and tests the connection to the database is working correctly.

#### Dependabot
Dependabot has been implemented to notify and automatically update to new versions of any packages we have within our poetry dependancy file.

***
### Terraform:
The infrastructure created by running terraform in the `terraform/ecs_fargate` folder is illustrated below:

![Alt text](terraform/ecs_fargate/infrastructure.svg?raw=true "VPC Subnet Module Diagram")

To deploy the application to a server accessible by a public IP address:
- create a `variables_env.tf`  file in the `ecs_fargate` folder containing the following variables:
```
variable "django_secret_key" {
    type = string
    description = "Django secret key."
    default = "<DJANGO_SECRET_KEY>"
}

variable "aws_account_id" {
    type        = string
    default     = "<AWS_ACCOUNT_ID>"
}

variable "dns_hosted_zone_id" {
  type        = string
  description = "ID of the hosted zone."
  default     = "<DNS_HOSTED_ZONE_ID>"
}
```
Note: The `DNS_HOSTED_ZONE_ID` can be found in the AWS console. Search for Route 53, select 'Hosted zone' under 'DNS management' and look in the 'Hosted zone ID' column.

- run the following in the command line while in the `ecs_fargate` directory:
  - `terraform init`
  - `terraform apply`
- push to a release branch to build and push Docker image to the created ECR.
- from the AWS console search for Elastic Container Service, select `ak-python-ecs-cluster`.
- go to the Tasks tab and then select the running container. Here you can open or copy the IP address.
- when finished run `terraform destroy` to tear down the infrastructure.

The ECR should already be created but if it is not, and you get an error follow the procedure outlined below:
- create a `ecr.tf`  file in the `ecs_fargate` folder containing the following resource:
```
resource "aws_ecr_repository" "python_ecr_repository" {
  name = "${var.project_name}-repo"
}
```
- run the `terraform apply` command.
- to stop the ECR being deleted by terraform destroy, first delete the `ecr.tf`  file.
- then run this command to remove it from the state file ` terraform state rm "aws_ecr_repository.python_ecr_repository"
`. This will leave the ECR for future runs using the infrastructure.
