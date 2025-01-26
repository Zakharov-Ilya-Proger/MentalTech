import React, { useState } from 'react';
import './CSS/RegisterForm.css';
import closeIcon from "../Assets/VectorLight.svg";
import closeIconDark from "../Assets/Vector.svg";

const RegisterForm = ({ isLightTheme, closeForms, toggleToLogin, handleLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
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
        if (password !== confirmPassword) {
            setError('Passwords do not match');
            return;
        }
        // Handle registration logic here
        try {
            const response = await fetch('https://metaltech.onrender.com/sing/up', {
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
        <div className={`register-form-container ${isLightTheme ? '' : 'dark'}`}>
            <img src={isLightTheme ? closeIcon : closeIconDark} alt="Close" className="close-icon" onClick={closeForms} />
            <div className="form-header">
                <h2>Sign Up</h2>
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
                <div className="form-group">
                    <input
                        type="password"
                        id="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Confirm Password"
                        required
                    />
                </div>
                {error && <p className="error">{error}</p>}
                <button type="submit">Sign Up</button>
            </form>
            <p>Already have an account? <span onClick={toggleToLogin}>Log In</span></p>
        </div>
    );
};

export default RegisterForm;
