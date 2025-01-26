import React, { useState } from 'react';
import './CSS/ClientAddForm.css';
import closeIcon from '../Assets/VectorLight.svg';
import closeIconDark from '../Assets/Vector.svg';

// Function to get the token from the cookie
const getTokenFromCookie = () => {
    const name = "authToken=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const cookieArray = decodedCookie.split(';');
    for (let i = 0; i < cookieArray.length; i++) {
        let cookie = cookieArray[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1);
        }
        if (cookie.indexOf(name) === 0) {
            return cookie.substring(name.length, cookie.length);
        }
    }
    return "";
};

const ClientAddForm = ({ isLightTheme, closeForms, handleAddClient }) => {
    const [username, setName] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (username.trim() === '') {
            setError('Name is required');
            return;
        }
        const token = getTokenFromCookie();
        // Handle add client logic here
        try {
            const response = await fetch('https://metaltech.onrender.com/clients/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': token
                },
                body: JSON.stringify({ username }),
            });
            const data = await response.json();
            if (response.ok) {
                handleAddClient(data);
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
        <div className={`client-add-form-container ${isLightTheme ? '' : 'dark'}`}>
            <img src={isLightTheme ? closeIcon : closeIconDark} alt="Close" className="close-icon" onClick={closeForms} />
            <div className="form-header">
                <h2>Add Client</h2>
            </div>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <input
                        type="text"
                        id="name"
                        value={username}
                        onChange={(e) => setName(e.target.value)}
                        placeholder="Client Name"
                        required
                    />
                </div>
                {error && <p className="error">{error}</p>}
                <button type="submit">Add Client</button>
            </form>
        </div>
    );
};

export default ClientAddForm;
