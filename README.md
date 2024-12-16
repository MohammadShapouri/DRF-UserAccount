
# Django Rest Framework User Account Manager

A user account management system based on the phone number validation in django rest framework.

# Dockerized version link:
https://github.com/MohammadShapouri/Dockerized-DRF-UserAccount


## Features
* A customizable OTP module for generating and verifying OTP codes and OTP configs.
* A module for generating and validating OTP configs.
* Creating, retrieving, updating, and deleting user accounts.
* Changing password and resetting password.
* Adding, retrieving, updating (setting default profile picture) and deleting profile pictures.
* Using celery for running tasks asynchronously.
* Different access levels and responses based on the user account type that sends requests. (Sperusers and staffs have the same access level as superusers in
  Django admin panel.)
* Sends OTP code for validating new accounts.
* Sends OTP code for validating new phone numbers if the phone number was changed during the update.



## Installation
__If you use windows, instead of using '_python3 -m_' and '_python3_', use '_python -m_' and _python_' in commands.__
* Run the following command in your terminal to clone this project or download it directly.
    ```
    $ git clone git@github.com:MohammadShapouri/DRF-UserAccount.git
    ```
* Install Redis and PostgreSQL.

* Navigate to the project folder (DRF-UserAccount folder).

* Create a .env file and fill it. (.env.sample is a sample file that shows which fields the .env file have.)

* Run the following command to create virtualenv. (If you haven't installed virtualenv package, you need to install virtualenv package first).
    ```
    $ python3 -m virtualenv venv
    ```

* Activate virtualenv.
    > Run the following command in Linux
    ```
    $ source venv/bin/activate
    ```
    > Run the following command in windows
    ```
    $ venv/Scripts/activate
    ```


* Run the following command to install the required frameworks and packages.
    ```
    $ pip install -r requirements.txt
    ```

* Navigate to the config folder.

* Run the following commands one by one to run the project.
    ```
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    $ python3 manage.py runserver
    ```

* Run the following command in the folder that contains manage.py to run celery.
  ```
    python -m celery -A config worker -l info

  ```


# Things to do in the future
* Saving OTP configs in DB and optimizing its app usage.
* ~~Dockerizing project. (Though it must be Dockerized after creating the project.)~~ _Done! Dockerized version is in another repository but it still needs some changes. (files in app folder are older than these files.)._
* ~~Adding profile picture IDs to user object data in the get method.~~ _Done!_
* Adding API for sending SMS.
* ~~using celery for sending sms.~~ _Done!_
* Writing test cases.
* ~~Adding change password and reset password view.~~ _Done!_
* Customizing Django admin panel.
* HASHING OTP CODES!!!
