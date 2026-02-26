
```markdown
# User Management Microservice

A **Flask-based microservice** for user management, designed for e-commerce platforms and applications requiring authentication and role-based access control.

---

## 📋 Prerequisites

Before running the application, ensure you have the following installed and configured:

### 🗄️ SQLite Installation
SQLite is required for database storage.

**Linux/macOS**
```bash
sudo apt-get update
sudo apt-get install sqlite3
```
Or on macOS (Homebrew):
```bash
brew install sqlite
```

**Windows**
1. Download the precompiled binaries from: `https://www.sqlite.org/download.html` [(sqlite.org in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fwww.sqlite.org%2Fdownload.html")
2. Extract the files to a folder (e.g., `C:\sqlite`).
3. Add the folder path to your **System Environment Variables** so you can run `sqlite3` from Command Prompt.
4. Verify installation:
   ```cmd
   sqlite3 --version
   ```

---

### 🛠️ Postman Installation & Configuration
Postman is a popular tool for testing REST APIs.

**Step 1: Download Postman**
- Visit [https://www.postman.com/downloads/](https://www.postman.com/downloads/)
- Choose the installer for your operating system (Windows, macOS, or Linux).
- Install using the default setup instructions.

**Step 2: Configure Postman**
1. Open Postman after installation.
2. Click **New → HTTP Request**.
3. Enter the API endpoint (e.g., `http://127.0.0.1:5000/register?address=0`).
4. Select the **HTTP method** (`POST`, `GET`, etc.).
5. Under the **Body** tab, choose **x-www-form-urlencoded**.
6. Add the required key-value pairs (e.g., `email`, `password`, etc.).
7. Click **Send** to test the request.
8. Review the response in the lower panel.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/cout-Rackeel/user-management-microservice.git
cd user-management-microservice
```

### 2. Configure Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv/Scripts/activate      # Windows PowerShell
```

### 3. Install Dependencies
Ensure you have **Python 3.9+** installed, then run:
```bash
pip install -r requirements.txt
```

### 4. Initialize the Database
Run the following command to set up the database schema:
```bash
flask --app user_management_microservice init-db
```

### 5. Run the Application
Start the server using the following command:

**Linux/macOS**
```bash
flask --app user_management_microservice run
```

**Windows (PowerShell)**
```powershell
flask --app user_management_microservice run
```

**Windows (Command Prompt)**
```cmd
flask --app user_management_microservice run
```

The service will be available at:
```
http://127.0.0.1:5000
```

---

## 📬 API Endpoints

### Register a New User (without address)
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/register?address=0`
- **Body (x-www-form-urlencoded):**
  ```
  email: customer1@gmail.com
  phone_number: 876-832-7333
  password: password
  first_name: Hugh
  last_name: Brown
  status: active
  ```

### Register a New User (with address)
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/register?address=1`
- **Body (x-www-form-urlencoded):**
  ```
  email: customer2@gmail.com
  phone_number: 876-834-7333
  password: password
  first_name: Kevin
  last_name: Brown
  status: active
  type: shipping
  street: 7 Glory Ave
  city: Spanish Town
  state: St. Catherine
  postal_code: JMACE25
  country: Jamaica
  ```

### Login
- **Method:** `POST`
- **URL:** `http://127.0.0.1:5000/login`
- **Body (x-www-form-urlencoded):**
  ```
  email: customer1@gmail.com
  password: password
  ```

### Get All Users
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/users`

### Get a Specific User
- **Method:** `GET`
- **URL:** `http://127.0.0.1:5000/users/<id>`

---
