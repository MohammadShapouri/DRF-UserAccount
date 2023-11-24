
# Django Rest Framework User Account Manager

A user account management system based on the phone number validation in django rest framework.


## Features
* A customizable OTP module for generating and verifing OTP codes and OTP configs.
* A module for generation and validating OTP configs.
* Creating, retriving, updating and deleting user account.
* Different access level and responses based on the user account type which sends request.
* Sends OTP code for validating new accounts.
* Sends OTP code for validating new phone numbers if phone number was changed during update.



## Installation
__If you use windows, instead of using '_python3 -m_' and '_python3_', use '_python -m_' and _python_' in commands.__
* Run the following command in your teminal to clone this project or download it directly.
    ```
    $ git clone git@github.com:MohammadShapouri/DRF-UserAccount.git
    ```

* Navigate to the project folder.

* Run the following command to create virtualenv. (If you haven't install virtualenv package, you need to install virtualenv package first).
    ```
    $ python3 -m virtualenv venv
    ```


* Activate virtualenv.
    > Run the following command in linux
    ```
    $ source venv/bin/activate
    ```
    > Run the following command in windows
    ```
    $ venv/Scripts/activate
    ```


* Run the following command to install required frameworks and packages.
    ```
    $ pip install -r requirements.txt
    ```

* Run the following commands one by one in the folder which contains manage.py file to run the project.
    ```
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    $ python3 manage.py runserver
    ```


# Things to do in future
* Dockerizing project. (Though it must be Dockerized after creating project.)
* Adding api for sending sms.
* Writing test cases.
* Adding change password and reset password view. 

