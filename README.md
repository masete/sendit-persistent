# sendit-persistent

## Badges
[![Build Status](https://travis-ci.org/masete/sendit-persistent.svg?branch=resolved_feedback)](https://travis-ci.org/masete/sendit-persistent) [![Maintainability](https://api.codeclimate.com/v1/badges/ad2303d54e880a08e46b/maintainability)](https://codeclimate.com/github/masete/sendit-persistent/maintainability) [![Coverage Status](https://coveralls.io/repos/github/masete/sendit-persistent/badge.svg?branch=develop)](https://coveralls.io/github/masete/sendit-persistent?branch=develop)



Send IT is a web application that helps clients to deliver their parcels in distant places according to their weigth and distance. It can be used by any one who wishes to ship their goods
##  Endpoints
|Endpoint|IPORTANCE|
|:---:|:---|

|Users *POST*|/api/auth/login|Login user and admin|
|Users *POST*|/api/auth/signup|Signup user|
|Parcels *POST*|/api/v1/parcel|create parcel order|
|Parcels*GET* |/api/v1/parcel|Get all parcel|
|Parcels *GET*|/api/v1/parcels/<int:parcel_id>/destination||
|Parcel *GET* Only Admin|/api/v1/parcels/<int:parcel_id>/status||
|Parcel *GET* Admin/user|[/api/v1/parcel||
|Admin *PUT* Only Admin|/api/v1/parcels/<int:parcel_id>/present_location||
|User *PUT* Only Admin|/api/v1/parcels/<int:parcel_id>/present_destination||
|Admin *PUT* Only Admin|/api/v1/parcels/<int:parcel_id>/present_status||
|Admin *PUT* Only Admin|/api/v1/parcels/<int:parcel_id>/present_location|Admin can chande location|


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
- Much appreciation goes to my fellow bootcamp candidates for your tireless efforts in helping me where I got stuck
- Lastly, thank you Andela for  the `Levelup35` program.
## Author
__MASETE NICHOLAS__
## Contact
[Twitter](https://twitter.com/masete)

