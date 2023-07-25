## Kitchen Service Project

Kitchen Service (CRUD application) is a web application for managing recipes, 
cooks, and dish types in a restaurant kitchen.

[Restaurant Kitchen Service deployed to RENDER]()

## Entities:

1. Cook(UserAdmin)
2. Dish Type
3. Dish

## Setup:

### option 1
1. Clone the project:
+ ```git clone https://github.com/ihorvoskoboinikov/django_test_prodject.git```
2. Create virtual environment and activate it
+ ```python3 -m venv venv```
+ ```source venv/bin/activate```
3. Install dependencies
+ ```pip install -r requirements.txt```
4. Run migrations
+ ```python manage.py makemigrations```
+ ```python manage.py migrate```
5. Create superuser 
+ ```python manage.py createsuperuser```  (enter your username and password)
6. Run server on local host
+ ```python manage.py runserver```
___

## Usage:

> 1. Go to the url where our website was launched http://127.0.0.1:8000 enter your username and password
> 2. You can use all the features of the site:
>> + Create, update and delete cooks
>> + Create, update and delete dish types
>> + Create, update and delete dishes
>> + Add and delete dish from cook
>> + You can filter data by name on pages with a list of names
> 3. Since you are an administrator, you can follow the link http://127.0.0.1:8000/admin/ and assign access rights for
     employees

[Website Interface](demo.PNG)