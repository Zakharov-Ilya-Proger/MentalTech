// Footer.js
import React from 'react';
import './CSS/Footer.css';
import logo from '../Assets/Logo.svg';
import dark_logo from '../Assets/DarkLogo.svg';

function Footer({ isLightTheme, selectedLanguage }) {
    return (
        <div className={`footer-container ${isLightTheme ? '' : 'dark'}`}>
            <div className="logo-footer">
                <img src={isLightTheme? logo : dark_logo} alt="MentalTech" className="logo-img" />
                <p className="text-logo-footer">MentalTech</p>
            </div>
            <div className="contact-buttons">
                <a href="#" className="contact-link">Contact Us</a>
                <a href="#" className="contact-link">Main</a>
                <a href="https://mentaltech.ru/" className="contact-link">About</a>
            </div>
            <div className="social-networks">
                <a href="#" className="social-link">Tg</a>
                <a href="#" className="social-link">Vk</a>
                <a href="#" className="social-link">Ig</a>
                <a href="#" className="social-link">Tw</a>
            </div>
            <div className="copyright">
                <p>&copy; 2025 MentalTech. All rights reserved.</p>
            </div>
        </div>
    );
}

export default Footer;
