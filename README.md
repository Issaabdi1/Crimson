# Team Crimson Major Group project

## Team members
The members of the team are:
- *ISSA ABDI*
- *SAMUEL CHILAKAMARI*
- *SIMON HA*
- *VINCENT HA*
- *Ryan McAree*
- *HILAL SAHIN*
- *HONGYI TU*
- *KAM HING HANSON ZHUANG*

## Project structure
The project is called `task_manager`.  It currently consists of a single app `tasks`.

## Deployed version of the application
The deployed version of the application can be found at [*https://teamcrimson.pythonanywhere.com/*](https://teamcrimson.pythonanywhere.com/).

## Instructions To access the python anywhere account
*delete section when submitting*

Login to PythonAnywhere
```
Username: TeamCrimson
Password: UfbnDsjntpo
```

## Amazon S3 Bucket

People can inspect the bucket via [here](https://aws.amazon.com)
```
- Account ID: 975050003861
- IAM user name: hanson
- Password: ^VkC12-w
```

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

Create and open .env file:

```
$ touch .env
$ open .env
```

Add the following environment variables to .env file and save:

```
USE_S3=TRUE
AWS_ACCESS_KEY_ID=AKIA6GBMCKWKVMOCFXG4
AWS_SECRET_ACCESS_KEY=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
AWS_STORAGE_BUCKET_NAME=mypdfbucket01
```

Set up and activate a local development environment:
```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Seed the development database with:

```
$ python3 manage.py seed
```

Before running the tests, download chrome webdriver from  [here](https://googlechromelabs.github.io/chrome-for-testing/),and save it to a directory of your choice on your system, for example, /Users/username/Desktop/drivers. 


Next, add the directory where you saved the Chrome WebDriver to the system's PATH by Opening the /etc/paths file using a text editor with administrative privileges. Add the full path to the directory where you saved the Chrome WebDriver (e.g., /Users/username/Desktop/drivers) as a new line in the /etc/paths file.
```
sudo nano /etc/paths
```

Create a superuser and run all tests with:
```
$ python3 manage.py create_debug_superuser
$ python3 manage.py test
```

## Sources
The packages used by this application are specified in `requirements.txt`

Chromedriver is used by this application for testing purpose, and can be downloaded via [here](https://googlechromelabs.github.io/chrome-for-testing/)
