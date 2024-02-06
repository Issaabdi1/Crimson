# Team _enter team name here_ Small Group project

## Team members

The members of the team are:

- _ISSA ABDI_
- _SAMUEL CHILAKAMARI_
- _SIMON HA_
- _VINCENT HA_
- _Ryan McAree_
- _HILAL SAHIN_
- _HONGYI TU_
- _KAM HING HANSON ZHUANG_

## Project structure

The project is called `task_manager`. It currently consists of a single app `tasks`.

## Deployed version of the application

The deployed version of the application can be found at [_enter url here_](*enter_url_here*).

## Installation instructions

To install the software and use it in your local development environment, you must first set up and activate a local development environment. From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Create and open .env file:

```
$ touch .env
$ open .env
```

Add the following environment variables to .env file and save:

```
USE_S3=TRUE
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:

```
$ python3 manage.py test
```

Run code coverage:

```
$ Python -m coverage run manage.py test
$ coverage html
```

_The above instructions should work in your version of the application. If there are deviations, declare those here in bold. Otherwise, remove this line._

## Sources

The packages used by this application are specified in `requirements.txt`

_Declare are other sources here, and remove this line_
