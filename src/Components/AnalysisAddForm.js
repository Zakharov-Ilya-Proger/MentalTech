import React, { useState } from 'react';
import './CSS/AnalysisAddForm.css';
import closeIcon from '../Assets/VectorLight.svg';
import closeIconDark from '../Assets/Vector.svg';
import checkIcon from '../Assets/Approve.svg';
import checkIconDark from '../Assets/DarkApprove.svg';

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

const AnalysisAddForm = ({ isLightTheme, closeForms, clientId, fetchAnalyses }) => {
    const [file, setFile] = useState(null);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [fileSelected, setFileSelected] = useState(false);
    const [fileName, setFileName] = useState('Выбрать файл');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true); // Set loading state to true
        const token = getTokenFromCookie();
        const formData = new FormData();
        formData.append('file', file);

        const date = new Date().toISOString(); // Get the current date and time
        const selectedLanguage = localStorage.getItem('selectedLanguage') || 'en'; // Get the selected language from local storage

        // Handle add analysis logic here
        try {
            const response = await fetch(`http://127.0.0.1:8000/analyses/add/${clientId}/${date}/${selectedLanguage}`, {
                method: 'POST',
                headers: {
                    'Authorization': token
                },
                body: formData,
            });
            const data = await response.json();
            setLoading(false); // Set loading state to false
            if (response.ok) {
                setError('');
                closeForms();
                fetchAnalyses(clientId); // Fetch analyses after successful addition
            } else {
                setError(data.detail);
            }
        } catch (err) {
            setLoading(false); // Set loading state to false
            setError('An error occurred. Please try again.');
        }
    };

    return (
        <div className={`analysis-add-form-container ${isLightTheme ? '' : 'dark'}`}>
            <img src={isLightTheme ? closeIcon : closeIconDark} alt="Close" className="close-icon" onClick={closeForms} />
            <div className="form-header">
                <h2>Add Analysis</h2>
            </div>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="file" className="file-label">
                        {fileName}
                    </label>
                    <input
                        type="file"
                        id="file"
                        onChange={(e) => {
                            const selectedFile = e.target.files[0];
                            if (selectedFile) {
                                setFile(selectedFile);
                                setFileName(selectedFile.name);
                                setFileSelected(true); // Set file selected state to true
                            }
                        }}
                        accept=".txt, .docx, .wav, .mp3"
                        className="file-input"
                    />
                    {fileSelected && <img src={isLightTheme ? checkIcon : checkIconDark} alt="Selected" className="check-icon" />}
                </div>
                <p className="file-note">
                    {localStorage.getItem('selectedLanguage') === 'en' ? 'Only .txt, .docx, .mp3, and .wav files are accepted.' : 'Принимаются только файлы форматов: .txt, .docx, .wav, .mp'}
                </p>
                {error && <p className="error">{error}</p>}
                {loading ? (
                    <div className="loading-spinner" />
                ) : (
                    <button type="submit">Add Analysis</button>
                )}
            </form>
        </div>
    );
};

export default AnalysisAddForm;
