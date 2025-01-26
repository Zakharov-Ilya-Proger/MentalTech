import './App.css';
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Header from "./Components/Header";
import Footer from "./Components/Footer";
import Main from "./Pages/Main";
import Chats from "./Pages/Chats"; // Импортируем компонент Chats
import { useEffect, useState } from "react";
import CookieConsent from "./Components/Cookie";

const App = () => {
    const [showCookieConsent, setShowCookieConsent] = useState(true);
    const [isLightTheme, setIsLightTheme] = useState(() => {
        const savedTheme = localStorage.getItem('lightTheme');
        return savedTheme === 'true';
    });
    const [selectedLanguage, setSelectedLanguage] = useState(() => {
        const savedLanguage = localStorage.getItem('selectedLanguage');
        return savedLanguage || 'en';
    });
    const [isAuthenticated, setIsAuthenticated] = useState(() => {
        const authToken = document.cookie.split('; ').find(row => row.startsWith('authToken='));
        return authToken ? true : false;
    });

    useEffect(() => {
        const hasConsented = localStorage.getItem('cookieConsent');
        if (hasConsented) {
            setShowCookieConsent(false);
        }
    }, []);

    useEffect(() => {
        localStorage.setItem('lightTheme', isLightTheme);
    }, [isLightTheme]);

    useEffect(() => {
        localStorage.setItem('selectedLanguage', selectedLanguage);
    }, [selectedLanguage]);

    const handleAccept = () => {
        localStorage.setItem('cookieConsent', 'true');
        setShowCookieConsent(false);
    };

    const handleDecline = () => {
        window.location.href = '/cookies-required';
    };

    const toggleTheme = () => {
        setIsLightTheme(prevTheme => !prevTheme);
    };

    const changeLanguage = (event) => {
        setSelectedLanguage(event.target.value);
    };

    const handleLogin = (token) => {
        const expires = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toUTCString(); // 30 дней
        document.cookie = `authToken=${token}; path=/; expires=${expires}`;
        setIsAuthenticated(true);
    };

    const handleLogout = () => {
        document.cookie = "authToken=; expires=Thu, 01 Jan 1970 00:00:00 GMT";
        setIsAuthenticated(false);
    };

    return (
        <div className={`body${isLightTheme ? '' : '-dark'}`}>
            <BrowserRouter>
                <Header
                    isLightTheme={isLightTheme}
                    toggleTheme={toggleTheme}
                    selectedLanguage={selectedLanguage}
                    changeLanguage={changeLanguage}
                    isAuthenticated={isAuthenticated}
                    handleLogout={handleLogout}
                    handleLogin={handleLogin} // Передаем функцию handleLogin
                />
                <Routes>
                    <Route path="/" element={
                        <Main
                            isLightTheme={isLightTheme}
                            selectedLanguage={selectedLanguage}
                            handleLogin={handleLogin}
                        />}
                    />
                    <Route path="/chats" element={
                        <Chats
                            isLightTheme={isLightTheme}
                            selectedLanguage={selectedLanguage}
                        />}
                    />
                </Routes>
                <Footer isLightTheme={isLightTheme}
                        selectedLanguage={selectedLanguage}/>
            </BrowserRouter>
            {showCookieConsent && <CookieConsent onAccept={handleAccept} onDecline={handleDecline} />}
        </div>
    );
};

export default App;
