-- Insert an Admin account
-- Email: admin@gearvn.com
-- Password: admin123
INSERT INTO users (email, password_hash, full_name, phone, role, status)
VALUES (
    'admin@gearvn.com', 
    '$2b$10$2Xr7zdhmiPrWK6g455SGX.cmNtFWBuRU4YlYn28seQ3qGASTYatSi', 
    'System Admin', 
    '0900000000', 
    'admin', 
    'active'
);
