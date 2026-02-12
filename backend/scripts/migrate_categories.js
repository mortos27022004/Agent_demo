require('dotenv').config();
const db = require('../config/database');

async function migrate() {
    try {
        console.log('Starting migration: Updating categories table...');

        await db.query(`
            ALTER TABLE categories 
            ADD COLUMN IF NOT EXISTS status text NOT NULL DEFAULT 'active';
            
            ALTER TABLE categories 
            ADD COLUMN IF NOT EXISTS attributes jsonb NOT NULL DEFAULT '[]';
        `);

        console.log('Migration successful: columns added to categories table.');
        process.exit(0);
    } catch (error) {
        console.error('Migration failed:', error);
        process.exit(1);
    }
}

migrate();
