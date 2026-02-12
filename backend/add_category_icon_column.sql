-- Migration: Add icon column to categories table
ALTER TABLE categories ADD COLUMN IF NOT EXISTS icon text DEFAULT 'info-circle';

-- Update existing categories with appropriate icons
UPDATE categories SET icon = 'laptop' WHERE slug = 'laptop';
UPDATE categories SET icon = 'global' WHERE slug = 'smartphone';
