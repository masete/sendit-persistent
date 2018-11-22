# sendit-persistent

## Badges
[![Build Status](https://travis-ci.org/masete/sendit-persistent.svg?branch=resolved_feedback)](https://travis-ci.org/masete/sendit-persistent) [![Maintainability](https://api.codeclimate.com/v1/badges/ad2303d54e880a08e46b/maintainability)](https://codeclimate.com/github/masete/sendit-persistent/maintainability) [![Coverage Status](https://coveralls.io/repos/github/masete/sendit-persistent/badge.svg?branch=develop)](https://coveralls.io/github/masete/sendit-persistent?branch=develop) 



Send IT is a web application that helps clients to deliver their parcels in distant places according to their weigth and distance. It can be used by any one who wishes to ship their goods

## Features
As an admin, am entitled to two specific routes, but i can still access some users routes without editing anything:
- Change status of an order parcel
- Change location of an order parcel
- View all orders created
- And all Normal users routes except cancel parcel and change destination

As a normal user, am entitled to the following features:
- A user can create a parcel
- A user can view all parcels
- A user can retrieve a single parcel
- A user can cancel a parcel
- A user can change the destination of a parcel
. A user can get all parcels that he/she posted

## Endpoints
HTTP Method | End point | Action
-----------|-----------|----------
POST | api/auth/login | Login a user/admin
POST | api/auth/signup | Register a user
POST | api/v1/parcel | Create a parcel order
GET | api/v1/parcel | Retrieve all parcel orders
GET | api/v1/parcel/parcel_id | Retrieve a single parcel order
GET | api/v1/user | Retrieve all registered users
GET | api/v1/users/user_id/parcel | Retrieve order parcels by a single user
PUT | api/v1/parcels/parcel_id/destination| User change destination
PUT | api/v1/parcels/parcel_id/status| Admin change status
PUT | api/v1/parcels/parcel_id/present_location| Admin Modify location

## Project Installation
|Action|Command Neeeded|
|---|---|
|*Installation*|`$ https://github.com/masete/sendit-persistent.git`|

### Using the project
|Action|Command Needed|
|---|---|
|Project root| `$ cd Sendit `|
|Environment creation|`$ virtualenv venv -p python3`|
|Activate Environment `Linux` or `Mac` |`$ source venv/bin/activate`|
|Activate Environment *Windows*|`c:/ .\venv\Scripts\activate venv/bin/activate`|
|Install project Dependencies|`$ pip install -r requirements.txt`|

## Python Version Supported
`Python 3.6 and above`

### Testing the app
`$ pytest --cov app/tests -cov-report term-missing`

### Running the app

`$ python3 run.py`



### CREDITS
- Much appreciation goes to my fellow bootcamp candidates, TEAM-POWER and both my LFA's of week1 and week2 for your tireless efforts in helping me where I got stuck
- Lastly, thank you Andela for  the `Levelup35` program.
## Author
__MASETE NICHOLAS__
## Contact
[Twitter](https://twitter.com/masete)

