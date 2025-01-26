// DropdownMenu.js
import React from 'react';
import './CSS/DropdownMenu.css';

const DropdownMenu = ({ isOpen, toggleMenu, isLightTheme, toggleTheme, selectedLanguage, changeLanguage, menuRef, handleLogout }) => {
    const languages = ['en', 'ru'];

    return (
        <div ref={menuRef} className={`dropdown-menu ${isOpen ? 'open' : ''} ${isLightTheme ? '' : 'dark'}`}>
            <ul>
                <li>
                    <div className={`menu-item ${isLightTheme ? '' : 'dark'}`}>
                        <span>Theme</span>
                        <label className="switch">
                            <input type="checkbox" checked={isLightTheme} onChange={toggleTheme} />
                            <span className="slider"></span>
                        </label>
                    </div>
                </li>
                <li>
                    <div className={`menu-item ${isLightTheme ? '' : 'dark'}`}>
                        <span>Lang</span>
                        <select value={selectedLanguage} onChange={(e) => changeLanguage(e)}>
                            {languages.map(lang => (
                                <option key={lang} value={lang}>
                                    {lang.toUpperCase()}
                                </option>
                            ))}
                        </select>
                    </div>
                </li>
                <li onClick={handleLogout}>
                    <div className="menu-item-log-out">
                        <span>Log Out</span>
                    </div>
                </li>
            </ul>
        </div>
    );
};

export default DropdownMenu;
