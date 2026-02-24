import functools

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify)

from werkzeug.security import check_password_hash, generate_password_hash

from .init_db import get_db

from flask_jwt_extended import create_access_token

from datetime import datetime, timezone

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
users_bp = Blueprint('users', __name__, url_prefix='/users')

# ------------------------------- HELPER FUNCTIONS ---------------------------------------
def getUserByIdHelper(user_id, db, error, errcode):
    try:
        sql = "SELECT * FROM Users WHERE user_id = ?"
        results = db.execute(sql, (user_id,)).fetchone()
            
    except Exception as e:
        exception_type_name = e.__class__.__name__
        error.append(f"{exception_type_name} occurred during user login: {e}")
    else:
        if results:
            user = dict(results) 
            return {"message":"User successfully fetched" , "data": user} , 200
        else:
            print("results")
            error = "User not found"    
            errcode = 404     
        
    return { "errors": error }, errcode
  
# ------------------------------- AUTHENTICATION ROUTES ---------------------------------------
## CREATE USER
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' :
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        status = request.form['status']
        store_address_is_active = request.args.get('address', False)
        set_admin_is_active = request.args.get('admin', False)
        
        store_address_is_active = True if store_address_is_active == "1" else False
        set_admin_is_active = True if set_admin_is_active == "1" else False
        
        db = get_db();
        
        error = []
        errcode = 400
        
        if not email:
            error.append('Email is required.')
        if not password:
            error.append('Password is required.')
        if not first_name:
            error.append('First name is required.')
        if not last_name:
            error.append('Last name is required.')
       
            
        if error == []:
            role_sql = """ INSERT INTO User_Roles 
                            (user_id, role_id) 
                            VALUES (?, ?)
                            RETURNING user_id """
            try:
                sql = """
                        INSERT INTO Users 
                        (email, phone_number, password_hash, first_name, last_name, status) 
                        VALUES (?, ?, ?, ?, ?, ?)
                        RETURNING user_id
                        """
                password_hash = generate_password_hash(password)
                
                user_data = (email , phone_number, password_hash, first_name, last_name, status)
                
                user_id = db.execute(sql , user_data).fetchone()
                
                if set_admin_is_active:
                    user_id = db.execute(role_sql , (user_id[0], 2)).fetchone() 
                
            except Exception as e:
                exception_type_name = e.__class__.__name__
                error.append(f"An {exception_type_name}  occurred while registering user: {e}")
                errcode = 500
            else:
                if user_id and store_address_is_active:
                    adrs_type = request.form['type']
                    street = request.form['street']
                    city = request.form['city']
                    state = request.form['state']
                    postal_code = request.form['postal_code']
                    country = request.form['country']
                    
                    if not adrs_type:
                        error.append('Address type is required.')
                    if not street:
                        error.append('Street is required.')
                    if not city:
                        error.append('City is required.')
                    if not postal_code:
                        error.append('Postal code is required.')
                    if not country:
                        error.append('Country is required.')
            
                    if error == []:
                        try: 
                            adrs_sql = """
                            INSERT INTO Addresses 
                            (user_id, type, street, city, state, postal_code, country) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            RETURNING user_id
                            """
                            address_data = (user_id[0], adrs_type, street, city, state, postal_code, country)
                            
                            user_id = db.execute(adrs_sql , address_data).fetchone()
                            user_id = db.execute(role_sql , (user_id[0], 1)).fetchone() 
                            db.commit()
                            
                        except Exception as e:
                            exception_type_name = e.__class__.__name__ or "DatabaseError"
                            error.append(f"An {exception_type_name}  occurred while registering user: {e}")
                            errcode = 500
                        else:
                            return {"message": "User registered successfully.", "data": {"user_id": user_id[0]}}, 201
                else:
                    db.commit()
                    return {"message": "User registered successfully.", "data": {"user_id": user_id[0]}}, 201
       
        return { "errors": error }, errcode

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = []
        
        if not email:
            error.append("Email is required")
        if not password:
            error.append("Password is required")
    
        if error == []:
            try:
                
                sql = "SELECT U.user_id, U.password_hash, UR.role_id, R.role_name FROM Users AS U INNER JOIN User_Roles AS UR ON U.user_id = UR.user_id LEFT JOIN Roles AS R ON UR.role_id = R.role_id WHERE U.email = ?"
                
                #sql = "SELECT U.user_id, U.password_hash FROM Users AS U INNER JOIN User_Roles AS UR ON U.user_id = UR.user_id"
                
                #IMPLEMENTATION FOR CAUSE WHERE A USER CAN ONLY HAVE ONE ROLE (SUBJECT TO CHANGE)
                
                results = db.execute(sql, (email,)).fetchone()
                if results:
                    user = dict(results)
                
            except Exception as e:
                exception_type_name = e.__class__.__name__
                error.append(f"{exception_type_name} occurred during user login: {e}")
            else:
                if user is None:
                    error.append(f"Invalid credentials {user}")
                elif not check_password_hash(user['password_hash'] , password):
                    error.append("Invalid credentials")
                if error == []:
                    additional_claims = {"role_id" : user['role_id'] } # SUBJECT TO CHANGE
                    
                    access_token = create_access_token(identity=user['user_id'], additional_claims=additional_claims)
                    return {"message": "User Login Successful", "access_token": access_token}, 200
        return { "errors": error }, 400
            

@auth_bp.route('/add-role', methods=['POST'])
def addRole():
    role_name = request.form['role_name']
    db = get_db()
    error = None
    
    if not role_name:
        error.append("Role name is required")
    
    if error is None:
        try:
                db.execute(
                    "INSERT INTO Roles (role_name) VALUES (?)",
                    (role_name,),
                )
                db.commit()
        except Exception as e:
                exception_type_name = e.__class__.__name__
                error = f"{exception_type_name} occurred during user login: {e}"
        else:
            return "Role added"
        
    return "Error adding role"

@auth_bp.route('/add-permission', methods=['POST'])
def addPermission():
    permission_key = request.form['permission_key']
    description = request.form['description']
    db = get_db()
    error = None
    
    if not permission_key:
        error = "Permission key  is required"
    
    if error is None:
        try:
            sql =   """
                    INSERT INTO Permissions 
                        (permission_key, description) 
                    VALUES
                        (?, ?),
                    """
            db.execute(sql , (permission_key, description))
            db.commit()
        except Exception as e:
                exception_type_name = e.__class__.__name__
                error = f"{exception_type_name} occurred during user login: {e}"
        else:
            return "Permissions added"
        
    return { "errors": error }
    
    
# ------------------------------- USER MANAGEMENT ROUTES ---------------------------------------
@users_bp.route('/', methods=['GET'])
def getUsers():
    if request.method == 'GET':
        db = get_db()
        error = None
        try:
            # sql = """ 
            #     SELECT * FROM Users AS U 
            #     INNER JOIN Addresses AS A ON U.user_id = A.user_id
            # """
            
            sql = """ 
                SELECT * FROM Users AS U 
            """
            
            users = db.execute(sql).fetchall()
            users = [dict(row) for row in users]
            response = {
                
            }
        except Exception as e:
            exception_type_name = e.__class__.__name__
            error.append(f"{exception_type_name} occurred during user login: {e}")
        else:
            return {"message":"Users successfully fetched" , "data": users} , 200
        
        return { "errors": error }, 400

@users_bp.route('/<int:user_id>', methods=['GET'])
def getUserById(user_id):
    if request.method == 'GET':
        db = get_db()
        error = None
        errcode = 400
        return getUserByIdHelper(user_id, db, error, errcode)
    
@users_bp.route('/<int:user_id>', methods=['PUT'])
def updateUser(user_id):
     if request.method == 'PUT':
        db = get_db()
        error = None
        errcode = 400
        is_password_change_active = request.args.get('password', False)
        is_status_change_active = request.args.get('status', False)
        
        is_password_change_active = True if is_password_change_active == "1" else False
        is_status_change_active = True if is_status_change_active == "1" else False
        
        user = getUserByIdHelper(user_id, db, error, errcode)[0]['data']
        
        if "errors" in user:
            return user , 404
        else:
            
            updatedUser = {
                'user_id' : user_id,
                'email' : request.form.get('email') if ('email' in request.form and request.form.get('email') ) else user['email'],
                'phone_number' : request.form.get('phone_number') if ('phone_number' in request.form and request.form.get('phone_number') ) else user['phone_number'],
                'password_hash' : generate_password_hash(request.form.get('password')) if ('password' in request.form and request.form.get('password') and is_password_change_active) else user['password_hash'],
                'first_name' : request.form.get('first_name') if ('first_name' in request.form and request.form.get('first_name') ) else user['first_name'],
                'last_name' : request.form.get('last_name') if ('last_name' in request.form and request.form.get('last_name') ) else user['last_name'],
                'status' : request.form.get('status') if ('status' in request.form and request.form.get('status') and is_status_change_active) else user['status'],
                'created_at' : user['created_at'],
                'updated_at' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            
            try:
                sql = """UPDATE Users SET email = ?, phone_number = ?, password_hash = ?, first_name = ?, last_name = ?, status = ?, updated_at = ? WHERE user_id = ?"""
                
                db.execute(sql , (updatedUser['email'], updatedUser['phone_number'], updatedUser['password_hash'], updatedUser['first_name'], updatedUser['last_name'], updatedUser['status'], updatedUser['updated_at'], user_id))
                
                db.commit()
            except Exception as e:
                exception_type_name = e.__class__.__name__
                error.append(f"{exception_type_name} occurred during user update: {e}")
                errcode = 500
            else:
                return {"message": "User updated successfully." , "data": updatedUser , "password": is_password_change_active , "status": is_status_change_active}, 200
            return { "errors": error }, errcode

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def deleteUser(user_id):
    if request.method == 'DELETE':
        db = get_db()
        error = None
        errcode = 400
        
        sql = """ DELETE FROM Users WHERE user_id = ? """
        
        try:
            db.execute(sql, (user_id,))
            db.commit()
        except Exception as e:
            exception_type_name = e.__class__.__name__
            error.append(f"{exception_type_name} occurred during user update: {e}")
            errcode = 500
        else:
            return {"message": "User deleted successfully." , "data": {} } , 200
        return { "errors": error }, errcode
    
