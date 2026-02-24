-- Seeder for Roles
INSERT INTO Roles (role_name, description) VALUES
('Customer', 'Standard user who shops on the platform'),
('Admin', 'Administrator with full system access');

-- Seeder for Permissions
INSERT INTO Permissions (permission_key, description) VALUES
('view_products', 'Can browse and view product listings'),
('place_orders', 'Can place new orders'),
('view_orders', 'Can view own order history'),
('manage_users', 'Can create, update, and delete user accounts'),
('manage_products', 'Can add, update, and remove products'),
('view_all_orders', 'Can view all customer orders'),
('manage_roles', 'Can assign roles and permissions');

-- Seeder for Role_Permissions
-- Customer role permissions
INSERT INTO Role_Permissions (role_id, permission_id)
SELECT r.role_id, p.permission_id
FROM Roles r, Permissions p
WHERE r.role_name = 'Customer'
  AND p.permission_key IN ('view_products', 'place_orders', 'view_orders');

-- Admin role permissions
INSERT INTO Role_Permissions (role_id, permission_id)
SELECT r.role_id, p.permission_id
FROM Roles r, Permissions p
WHERE r.role_name = 'Admin'
  AND p.permission_key IN ('view_products', 'place_orders', 'view_orders',
                           'manage_users', 'manage_products',
                           'view_all_orders', 'manage_roles');