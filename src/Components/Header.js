// Header.js
import React, { useRef, useEffect, useState } from 'react';
import './CSS/Header.css';
import logo from '../Assets/Logo.svg';
import darkLogo from '../Assets/DarkLogo.svg';
import settings from '../Assets/setting.svg';
import darkSettings from '../Assets/DarkSetting.svg';
import DropdownMenu from './DropdownMenu';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';
import { useLocation } from 'react-router-dom';

function Header({ isLightTheme, toggleTheme, selectedLanguage, changeLanguage, isAuthenticated, handleLogout, handleLogin }) {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [showLoginForm, setShowLoginForm] = useState(false);
    const [showRegisterForm, setShowRegisterForm] = useState(false);
    const menuRef = useRef(null);
    const formRef = useRef(null);
    const location = useLocation();

    const toggleMenu = () => {
        setIsMenuOpen(prevState => !prevState);
    };

    const handleClickOutside = (event) => {
        if (menuRef.current && !menuRef.current.contains(event.target)) {
            setIsMenuOpen(false);
        }
        if (formRef.current && !formRef.current.contains(event.target)) {
            closeForms();
        }
    };

    useEffect(() => {
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const handleLoginClick = () => {
        setShowLoginForm(true);
        setShowRegisterForm(false);
    };

    const handleRegisterClick = () => {
        setShowRegisterForm(true);
        setShowLoginForm(false);
    };

    const closeForms = () => {
        setShowLoginForm(false);
        setShowRegisterForm(false);
    };

    const toggleToRegister = () => {
        setShowLoginForm(false);
        setShowRegisterForm(true);
    };

    const toggleToLogin = () => {
        setShowRegisterForm(false);
        setShowLoginForm(true);
    };

    return (
        <div className={`header-container ${isLightTheme ? '' : 'dark'}`}>
            <a href="https://mentaltech.ru/" className="header-logo-link" target="_blank" rel="noopener noreferrer">
                <div className="header-logo">
                    <img src={isLightTheme ? logo : darkLogo} alt="MentalTech" className="logo" />
                    <p className={`text-logo ${isLightTheme ? '' : 'dark'}`}>MentalTech</p>
                </div>
            </a>
            <div className="header-button">
                <img src={isLightTheme ? settings : darkSettings} alt="settings" className="settings" onClick={toggleMenu} />
                <DropdownMenu
                    isOpen={isMenuOpen}
                    toggleMenu={toggleMenu}
                    isLightTheme={isLightTheme}
                    toggleTheme={toggleTheme}
                    selectedLanguage={selectedLanguage}
                    changeLanguage={changeLanguage}
                    menuRef={menuRef}
                    handleLogout={handleLogout}
                />
                <div className="buttons">
                    {!isAuthenticated ? (
                        <>
                            <div className={`login-signup ${isLightTheme ? '' : 'dark'}`} onClick={handleLoginClick}>
                                <p>Log In</p>
                            </div>
                            <div className={`login-signup ${isLightTheme ? '' : 'dark'}`} onClick={handleRegisterClick}>
                                <p>Sign Up</p>
                            </div>
                        </>
                    ) : (
                        <>
                            {location.pathname === '/' ? (
                                <a href="/chats" className={`login-signup ${isLightTheme ? '' : 'dark'}`}>
                                    <p>Chats</p>
                                </a>
                            ) : (
                                <a href="/" className={`login-signup ${isLightTheme ? '' : 'dark'}`}>
                                    <p>Main</p>
                                </a>
                            )}
                        </>
                    )}
                </div>
            </div>
            {(showLoginForm || showRegisterForm) && (
                <div ref={formRef} className="form-overlay">
                    {showLoginForm && <LoginForm isLightTheme={isLightTheme} closeForms={closeForms} toggleToRegister={toggleToRegister} handleLogin={handleLogin} />}
                    {showRegisterForm && <RegisterForm isLightTheme={isLightTheme} closeForms={closeForms} toggleToLogin={toggleToLogin} handleLogin={handleLogin} />}
                </div>
            )}
        </div>
    );
}

export default Header;
