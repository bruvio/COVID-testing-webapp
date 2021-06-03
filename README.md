# Fake COVID testing webapp

This is a web service that fakes a COVID testing facility.
It assumes that the lab receives tests and creates input data for the web application in the form of json files.

The app provides a secured service to store data through an API and then provides two public endpoints for reporting and plotting of the data

Example data is provided in the Repo (in the Data folder)

## Deliverables

### Endpoints

The following endpoints are provided:

- GET /cartridge/{cartridgeID} Searches the data for the specific cartridge (test)
- GET /cartridges Returns all cartridgeIDs
- DELETE /cartridge/{cartridgeID} Delete a cartridgeID
- PUT /cartridge/{cartridgeID} put/update a cartridgeID
- POST /cartridge/{cartridgeID} posts/creates a cartridgeID
- POST /auth/ authenticates the user
- POST /register/ posts/creates a new user able to access private endpoints

### 1. Initial Setup

**Quick Setup** (prereq: `git, python3.8`,`docker` )

```bash
git clone <reponame>
```

### 2. Webapp

A CRUD application with a dockerized environment for development and future deployment to AWS services. Python for services and SqlAlchemy for database.

#### Project Structure:

Mono-repo style

```
├──app/
    ├── __init__.py
    ├── ─wsgi.py
    ├── tests
    │   ├── test.py
    └── src
        ├── __init__.py
        ├── app1.py
        ├── app2.py
        ├── db.py
        ├── security_class.py
        ├── server.py
        └── helpers.py
        └── models
            ├── __init__.py
            ├── cartridge.py
            ├── user.py
        └── resources
            ├── __init__.py
            ├── cartridge.py
            ├── user.py
        └── utils
            ├── __init__.py
            ├── data.py
├──Dockerfile
├──docker-compose.yml
├──.pylintrc
├──.gitignore
├──.pre-commit-config.yaml
├──isort.cfg
├──requirements-dev.txt
├──README.md


```

- `app/wsgi`: contains the entrypoint for the application.
- `app/tests/`: Tests for CRUD operations of the API.
- `app/utils/`: Helpers functions
- `app/resources/`: folder where the resources (the cartridge and the user) are defined
- `app/models/`: folder where the models (the cartridge and the user) are defined
- `Dockerfile`: dockerfile for building an image, local testing and future deployment to AWS

### 4. Starting the environment

`gunicord wsgi:server`
the service will start listening at
`http://127.0.0.1:8000`

Here you will see a few error messages, do not worry! it is because the database is empty

### 5. Using the application

I use PostMAN for testing the service.

First Action is to create a user

```
import requests

url = "http://127.0.0.1:8000/register"

payload="{\n\t\"username\": \"bruno\",\n\t\"password\": \"strongpassword\"\n}\n"
headers = {
'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```

Once the user is created we must authenticate

```
import requests

url = "http://127.0.0.1:8000/auth"

payload="{\n\t\"username\": \"bruno\",\n\t\"password\": \"strongpassword\"\n}\n"
headers = {
'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```

The service will reply with a JWT token that we then will need to pass in the headers of our next calls to the endpoints

We can now start populating the database.
I suggest to have a look at the data first. The data provided are 10 "completed" tests. I suggest to fiddle a bit with the data, changing for example the status or changing the time stamps.

To insert a test/cartridge

```
import requests

url = "http://127.0.0.1:8000/cartridge/DN4110004145919"

payload="{\n\t\"cartridgeId\": \"DN4110004145919\",\n\t\"testStatus\": \"Error\",\n\t\"departmentName\": \"DPT001\",\n\t\"boxName\": \"nudge_2294DC\",\n\t\"pattern\": \"CVD540\",\n\t\"hospitalName\": \"HSP001\",\n\t\"operatorName\": \"opt1\",\n\t\"organisationId\": \"ORG1\",\n\t\"participantId\": \"V8Z85\",\n\t\"trustName\": \"TRUST1\",\n\t\"submissionDateTime\": \"2021-03-04 10:59:40.000 UTC\",\n\t\"testStartDateTime\": \"2021-03-04 11:01:55.000 UTC\",\n\t\"lastUpdatedDateTime\": \"2021-03-04 13:55:58.192 UTC\"\n}"
headers = {
'Content-Type': 'application/json',
"Authorization": "JWT " + str(token),
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

```

After a couple of tests are in the database we can start visiting the endpoints for reporting and plotting of the data.

### 6. Reporting

The report end point is
`/tableReport`

If the user tries to access this endpoint at the very beginning (i.e. after starting the service for the very first time) will see an empty page with a default message

After populating the database the user can choose from a dropdown menu three datasets

- alldata - contains all the data contained inside the json file uploaded
- df_testStatus - pivot table that generates a count of the different test status (complete, testing, error,...)
- df_testingTime - pivot table that generates the testing mean and total time for a given hospital and pattern

if the user uploads new data, to see the new report just refresh the page

### 7 Plotting the data

The plot end point is
`/dashboard`

If the user tries to access this endpoint at the very beginning (i.e. after starting the service for the very first time) will see an empty page with a default message

After populating the database the user can choose see a few plots of the data:

- test outcome vs count
- mean test time vs pattern
- testtime vs hospitalname for a given test outcome that can be selected in the above dropdown menu

if the user uploads new data, to see the new plots just refresh the page

### 8. Tests

Test at the moment assume a state of the system where the database is empty (database file is deleted)

to run the tests, first start the service and then

`python tests/test.py`

### 9. deploy to AWS

to deploy to AWS, this is how I would do it

1.  first build an image

```
IMAGE_VERSION=${1:-latest} IMAGE_NAME="dnanudge_webapp" docker build -t $IMAGE_NAME:$IMAGE_VERSION .
```

2.  once the image is build push it to dockerhub

3.  Create a cloudformation template to generate Roles, for example something like this

```
export REGION="us-east-1"

echo ""
echo "creating role stack"
echo ""
aws cloudformation create-stack --capabilities CAPABILITY_IAM --stack-name ecs-roles --template-body file:///create_IAM_roles.yml

aws cloudformation wait stack-create-complete --stack-name ecs-roles
```

and export the roles, for example:

```echo "AutoscalingRole: $AutoscalingRole"
echo "EC2Role: $EC2Role"
echo "ECSRole: $ECSRole"
echo "ECSTaskExecutionRole: $ECSTaskExecutionRole"
```

4. add / extend permissions for example to access SSM parameter store, Xray,....

5.

crete a VPC stack, for example

```
echo ""
echo "creating vpc stack"
echo ""
aws cloudformation create-stack --capabilities CAPABILITY_IAM --stack-name ecs-core-infrastructure --template-body file:///core-infrastructure-setup.yml

aws cloudformation wait stack-create-complete --stack-name ecs-core-infrastructure
```

and export relevant info from the stack outputs, like vpc, subnets,...

6.

create a ALB (application load balancer) stack, for example

```
echo ""
echo "creating alb stack"
echo ""
aws cloudformation create-stack \
--stack-name external-alb \
--template-body file:///alb-external.yml

aws cloudformation wait stack-create-complete --stack-name external-alb
```

and export relevant info from the stack outputs, like alb security group id, dns names,...

7.

create a cluster

8.

create a task definition using the docker image (either coming from ecr or dockerhub)

9.  create a service

10. start the service
