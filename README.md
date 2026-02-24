

```markdown
# User Management Microservice

A Flask-based microservice for user management.

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/cout-Rackeel/user-management-microservice.git
cd user-management-microservice
```

### 2. Install Dependencies
Make sure you have Python 3.9+ installed, then run:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Set the Flask app environment variable and start the server:

**Linux/macOS**
```bash
export FLASK_APP=user_management_microservice
flask run
```

**Windows (PowerShell)**
```powershell
set FLASK_APP=user_management_microservice
flask run
```

The service will be available at:
```
http://127.0.0.1:5000
```

---

## Using Postman

You can test the API endpoints with [Postman](https://www.postman.com/):

- **Register a new user **
  - Method: `POST`
  - URL: `http://127.0.0.1:5000/register?address=0`
  - Body (x-www-form-urlencoded):
    ```
      email:customer1@gmail.com
      phone_number:876-832-7333
      password:password
      first_name:Hugh
      last_name:Brown
      status:active
    ```

- **Register a new user with address**
  - Method: `POST`
  - URL: `http://127.0.0.1:5000/register?address=1`
  - Body (x-www-form-urlencoded):
    ```
      email:customer2@gmail.com
      phone_number:876-834-7333
      password:password
      first_name:Kevin
      last_name:Brown
      status:active
      type:shipping
      street:7 Glory Ave
      city:Spanish Town
      state:St.Catherine
      postal_code:JMACE25
      country:Jamaica
    ```

- **Login**
  - Method: `POST`
  - URL: `http://127.0.0.1:5000/login`
  - Body (x-www-form-urlencoded):
    ```
      email: customer1@gmail.com,
      password: password
    ```

- **Get all users**
  - Method: `GET`
  - URL: `http://127.0.0.1:5000/users`

- **Get a specific user**
  - Method: `GET`
  - URL: `http://127.0.0.1:5000/users/<id>`
```

-
