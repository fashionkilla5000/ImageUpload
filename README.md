# ImageUpload

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [How it works](#how-it-works)

## General info
API that allows any user to upload an image in PNG or JPG format.

## Technologies
* Python
* Djnago
* Imagekit
* TimestampSigner
	
## Setup
To run this project, first install requirements, next set up Database and then run django server:

```
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py makemigrations app
$ python manage.py migrate
$ python manage.py loaddata initial_data
$ python manage.py runserver
```

## How it works?
Firstly u need to register as admin, go to admin page, add users and give them Subscriptions in `UserSubscription`

* In your terminal paste this line and follow the instructions
```
python manage.py createsuperuser
```

To test it log as created user and star Uploading Image in `MyImageModel`
