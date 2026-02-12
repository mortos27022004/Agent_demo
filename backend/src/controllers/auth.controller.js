const authService = require('../services/auth.service');

const signup = async (req, res, next) => {
    try {
        const user = await authService.signUp(req.body);
        res.status(201).json({
            status: 'success',
            data: { user }
        });
    } catch (error) {
        if (error.code === '23505') { // Unique violation
            return res.status(400).json({
                status: 'error',
                message: 'Email đã được sử dụng'
            });
        }
        next(error);
    }
};

const login = async (req, res, next) => {
    try {
        const { email, password } = req.body;
        const result = await authService.login(email, password);
        res.status(200).json({
            status: 'success',
            data: result
        });
    } catch (error) {
        res.status(401).json({
            status: 'error',
            message: error.message
        });
    }
};

module.exports = {
    signup,
    login
};
