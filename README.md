# Picpay Simplified

## Description

Picpay back-end challenge project. I'm not in the selection process, I did it just for fun.

## Project Structure
```
+---app
|   +---api
|   |   +---v1
|   |   \---v2
|   +---blueprints
|   +---services
|   +---static
|   |   +---css
|   |   |   +---login
|   |   |   \---main
|   |   \---js
|   +---templates
|   |   +---login
|   |   \---main
```

## Installation and Configuration

### Requirements
- Python (version 3.11)

### Installation

1. Clone the repository: `git clone ssh:git@github.com:erosnoxx/PicPay.git`
2. Access the project directory: `cd PicPay`
3. Create a virtual environment (optional but recommended): `python -m venv venv`
4. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Init database: `flask db init`
7. Install migrations: `flask db migrate`
8. Upgrade migrations: `flask db upgrade`

## Usage

1. Execute the command to start the application: `flask run`
2. Access the application in your browser using the local address `http://localhost:5000`

## Contribution
Contributions are acceptable! Please, send me pull requests.

## License
This project are under MIT licence.

## API
### Route `/api/v1/users/<id>` - Method: GET
- **Description**: Fetches details of a specific user.
- **Path Parameters**:
  - `id`: ID of the user to retrieve.
- **Success Response**:
  - Code 200: Returns user details in JSON format.
  ```json
  {
    "id": "string",
    "fullname": "string",
    "socialname": "string",
    "cpf": "string",
    "email": "string",
    "balance": "number",
    "type": "string"
  }
  ```
- **Error Response**:
  - Code 404: User not found.

### Route `/api/v1/users` - Method: POST
- **Description**: Creates a new user.
- **Request Body**:
  ```json
  {
    "fullname": "string",
    "socialname": "string",
    "cpf": "string",
    "email": "string",
    "password": "string",
    "amount": "number",
    "type": "string"
  }
  ```
- **Success Response**:
  - Code 201: Returns details of the new user in JSON format.

- **Error Response**:
  - Code 400: Invalid data.

### Route `/api/v1/transactions/<id>` - Method: GET
- **Description**: Retrieves transactions of a specific user.
- **Path Parameters**:
  - `id`: ID of the user to list transactions.
- **Success Response**:
  - Code 200: Returns user transactions in JSON format.

- **Error Response**:
  - Code 404: User not found.

### Route `/api/v1/transactions` - Method: POST
- **Description**: Creates a new transaction between users.
- **Request Body**:
  ```json
  {
    "id_payer": "string",
    "id_payee": "string",
    "amount": "number"
  }
  ```
- **Success Response**:
  - Code 201: Returns details of the transaction in JSON format.

- **Error Response**:
  - Code 400: Unauthorized transfer or invalid data.

### Route `/api/v1/balance` - Method: POST
- **Description**: Updates a user's balance.
- **Request Body**:
  ```json
  {
    "id_owner": "string",
    "amount": "number"
  }
  ```
- **Success Response**:
  - Code 201: Returns details of the updated balance in JSON format.

- **Error Response**:
  - Code 400: Invalid data.
  - Code 404: User not found.

---

