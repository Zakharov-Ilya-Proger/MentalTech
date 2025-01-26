// LoginForm.js
import React, { useState } from 'react';
import './CSS/LoginForm.css';
import closeIcon from '../Assets/VectorLight.svg';
import closeIconDark from '../Assets/Vector.svg';

const LoginForm = ({ isLightTheme, closeForms, toggleToRegister, handleLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            setError('Invalid email address');
            return;
        }
        if (password.length < 6) {
            setError('Password must be at least 6 characters long');
            return;
        }
        // Handle login logic here
        try {
            const response = await fetch('https://metaltech.onrender.com/sing/in', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });
            const data = await response.json();
            if (response.ok) {
                handleLogin(data.token);
                setError('');
                closeForms();
            } else {
                setError(data.detail);
            }
        } catch (err) {
            setError('An error occurred. Please try again.');
        }
    };

    return (
        <div className={`login-form-container ${isLightTheme ? '' : 'dark'}`}>
            <img src={isLightTheme ? closeIcon : closeIconDark} alt="Close" className="close-icon" onClick={closeForms} />
            <div className="form-header">
                <h2>Log In</h2>
            </div>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="example@example.com"
                        required
                    />
                </div>
                <div className="form-group">
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        required
                    />
                </div>
                {error && <p className="error">{error}</p>}
                <button type="submit">Log In</button>
            </form>
            <p>Don't have an account? <span onClick={toggleToRegister}>Sign Up</span></p>
        </div>
    );
};

export default LoginForm;
