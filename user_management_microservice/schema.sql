DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Roles;
DROP TABLE IF EXISTS User_Roles;
DROP TABLE IF EXISTS Permissions;
DROP TABLE IF EXISTS Role_Permissions;
DROP TABLE IF EXISTS Addresses;
DROP INDEX IF EXISTS idx_users_email;
DROP INDEX IF EXISTS idx_users_phone;
DROP INDEX IF EXISTS idx_addresses_user;



-- Users table
CREATE TABLE IF NOT EXISTS Users (
    user_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    email          TEXT NOT NULL UNIQUE,
    phone_number   TEXT UNIQUE,
    password_hash  TEXT NOT NULL,
    first_name     TEXT NOT NULL,
    last_name      TEXT NOT NULL,
    status         TEXT CHECK(status IN ('active','inactive','locked','deleted')) DEFAULT 'active',
    created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at     DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Roles table
CREATE TABLE IF NOT EXISTS Roles (
    role_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name   TEXT NOT NULL UNIQUE,
    description TEXT
);

-- User_Roles table (Many-to-Many between Users and Roles)
CREATE TABLE IF NOT EXISTS User_Roles (
    user_id     INTEGER NOT NULL,
    role_id     INTEGER NOT NULL,
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id) ON DELETE CASCADE
);

-- Permissions table
CREATE TABLE IF NOT EXISTS Permissions (
    permission_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    permission_key  TEXT NOT NULL UNIQUE,
    description     TEXT
);

-- Role_Permissions table (Many-to-Many between Roles and Permissions)
CREATE TABLE IF NOT EXISTS Role_Permissions (
    role_id        INTEGER NOT NULL,
    permission_id  INTEGER NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES Roles(role_id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES Permissions(permission_id) ON DELETE CASCADE
);

-- Addresses table
CREATE TABLE IF NOT EXISTS Addresses (
    address_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    type         TEXT CHECK(type IN ('billing','shipping')) NOT NULL,
    street       TEXT NOT NULL,
    city         TEXT NOT NULL,
    state        TEXT,
    postal_code  TEXT NOT NULL,
    country      TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);



-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_email ON Users(email);
CREATE INDEX IF NOT EXISTS idx_users_phone ON Users(phone_number);
CREATE INDEX IF NOT EXISTS idx_addresses_user ON Addresses(user_id);
