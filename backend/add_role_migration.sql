-- Migration script to add role to users table
ALTER TABLE users ADD COLUMN role text NOT NULL DEFAULT 'user';
-- Optional: Add index if we often filter by role
CREATE INDEX idx_users_role ON users(role);
