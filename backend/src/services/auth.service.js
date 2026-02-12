const db = require('../../config/database');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');

const signUp = async (userData) => {
    const { email, password, fullName, phone, gender, dob, address } = userData;

    // Use a transaction for atomicity
    const client = await db.connect();

    try {
        await client.query('BEGIN');

        // Hash password
        const salt = await bcrypt.genSalt(10);
        const passwordHash = await bcrypt.hash(password, salt);

        const userQuery = `
            INSERT INTO users (email, password_hash, full_name, phone, gender, date_of_birth, role)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id, email, full_name, phone, gender, date_of_birth, role, created_at;
        `;
        const userResult = await client.query(userQuery, [email, passwordHash, fullName, phone, gender, dob, userData.role || 'user']);
        const user = userResult.rows[0];

        // Insert default address
        const addressQuery = `
            INSERT INTO addresses (user_id, recipient, phone, line1, is_default)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, line1, province, district, ward;
        `;
        await client.query(addressQuery, [user.id, fullName, phone, address, true]);

        await client.query('COMMIT');
        return user;
    } catch (error) {
        await client.query('ROLLBACK');
        throw error;
    } finally {
        client.release();
    }
};

const login = async (email, password) => {
    const query = `SELECT * FROM users WHERE email = $1 AND status = 'active'`;
    const result = await db.query(query, [email]);

    const user = result.rows[0];
    if (!user) {
        throw new Error('Email hoặc mật khẩu không đúng');
    }

    const isMatch = await bcrypt.compare(password, user.password_hash);
    if (!isMatch) {
        throw new Error('Email hoặc mật khẩu không đúng');
    }

    // Generate token
    const token = jwt.sign(
        { id: user.id, email: user.email },
        process.env.JWT_SECRET || 'your_jwt_secret',
        { expiresIn: '7d' }
    );

    return {
        user: {
            id: user.id,
            email: user.email,
            fullName: user.full_name,
            role: user.role
        },
        token
    };
};

module.exports = {
    signUp,
    login
};
