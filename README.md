
# FineArt DRF Project

This is a backend project developed using Django Rest Framework for managing expenses, incomes, and other financial transactions. The project allows users to manage their financial transactions, including bank receipts and view the total of their expenses, incomes, and other financial details.


## Installation

To run this project, you will need Python 3.8+ and pip installed on your system. Clone the repository to your local machine using the following command:

```bash
  git clone https://github.com/hamzamgit/financial-app-backend.git
```

Go to the project directory

```bash
  cd financial-app-backend
```

Create a virtual environment:

```bash
  python3 -m venv env
```

Activate the virtual environment:

```bash
  source env/bin/activate
```

Install the project requirements:

```bash
  pip install -r requirements.txt
```
    
## Running the Project

Before running the project, make sure to apply the migrations:

```bash
  python manage.py migrate
```

Create a superuser:
```bash
  python manage.py createsuperuser
```

Start the development server:
```bash
  python manage.py runserver
```
This will start the server at http://127.0.0.1:8000/. You can then access the APIs by navigating to http://127.0.0.1:8000/api/

The following APIs are available:

    register:Registers a new user
    login: Logs in an existing user
    profile: Manages the user profile
    change-password: Changes the user password
    send-reset-password-email: Sends an email to reset the user password
    reset-password: Resets the user password
    type: Manages payment types
    category: Manages payment categories
    payments: Manages payments
    transaction: Manages transactions
    total-transaction: Shows the total of expenses, income, and other transactions

You can access these APIs using the appropriate HTTP methods (GET, POST, PUT, DELETE) and the appropriate endpoints. For more details, please refer to the code documentation.

## Contributing

This project was developed by Muhammad Shahzad. If you want to contribute to this project, please fork the repository and create a pull request.



