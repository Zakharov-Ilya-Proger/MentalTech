import React, { useState, useEffect } from 'react';
import './CSS/Cookie.css';

const CookieConsent = ({ onAccept }) => {
    const [isVisible, setIsVisible] = useState(true);

    useEffect(() => {
        const handleEscapeKey = (event) => {
            if (event.key === 'Escape') {
                setIsVisible(false);
            }
        };

        document.addEventListener('keydown', handleEscapeKey);
        return () => {
            document.removeEventListener('keydown', handleEscapeKey);
        };
    }, []);

    const handleAccept = () => {
        onAccept();
        setIsVisible(false);
    };
    return (
        <div className={`cookie-consent ${isVisible ? 'visible' : ''}`}>
            <div className="cookie-content">
                <p>We use cookies to ensure you get the best experience on our website. By continuing to use our site, you accept our use of cookies.</p>
                <div className="cookie-buttons">
                    <button onClick={handleAccept}>Accept</button>
                </div>
            </div>
        </div>
    );
};

export default CookieConsent;
