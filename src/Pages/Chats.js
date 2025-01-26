import React, { useState, useEffect } from 'react';
import './CSS/Chats.css';
import darkPlus from "../Assets/Darkplus.svg"
import LightPlus from "../Assets/plus.svg"
import ClientAddForm from '../Components/ClientAddForm';
import AnalysisAddForm from '../Components/AnalysisAddForm';

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

const questionsGAD7 = {
    en: [
        "Feeling nervous, anxious, or on edge",
        "Not being able to stop or control worrying",
        "Worrying too much about different things",
        "Trouble relaxing",
        "Being so restless that it is hard to sit still",
        "Becoming easily annoyed or irritable",
        "Feeling afraid as if something awful might happen"
    ],
    ru: [
        "Нервничал(а), тревожился(ась) или был(а) раздражён(а)",
        "Не мог(ла) прекратить или контролировать своё беспокойство",
        "Слишком много беспокоился(ась) о разных вещах",
        "Было трудно расслабиться",
        "Был(а) настолько беспокоен(а), что не мог(ла) усидеть на месте",
        "Был(а) легко раздражим(а)",
        "Боялся(ась), как если бы могло случиться что-то ужасное"
    ]
};

const questionsPHQ9 = {
    en: [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself - or that you are a failure or have let yourself or your family down",
        "Trouble concentrating on things, such as reading the newspaper or watching television",
        "Moving or speaking so slowly that other people could have noticed? Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual",
        "Thoughts that you would be better off dead, or of hurting yourself in some way"
    ],
    ru: [
        "Вам не хотелось ничего делать",
        "У Вас было плохое настроение, Вы были подавлены или испытывали чувство безысходности",
        "Вам было трудно заснуть, у Вас был прерывистый сон, или Вы слишком много спали",
        "Вы были утомлены, или у Вас было мало сил",
        "У Вас был плохой аппетит, или Вы переедали",
        "Вы плохо о себе думали: считали себя неудачником (неудачницей), или были в себе разочарованы, или считали, что подвели свою семью",
        "Вам было трудно сосредоточиться (например, на чтении газеты или при просмотре телепередач)",
        "Вы двигались или говорили настолько медленно, что окружающие это замечали? Или, наоборот, были настолько суетливы или взбудоражены, что двигались больше обычного",
        "Вас посещали мысли о том, что Вам лучше было бы умереть, или о том, чтобы причинить себе какой-нибудь вред"
    ]
};

const getDepressionClassification = (score) => {
    if (score >= 20) return "Severe depression";
    if (score >= 15) return "Moderately severe depression";
    if (score >= 10) return "Moderate depression";
    if (score >= 5) return "Mild depression";
    return "Minimal depression";
};

const getAnxietyClassification = (score) => {
    if (score > 15) return "Severe Anxiety";
    if (score >= 10) return "Moderate Anxiety";
    if (score >= 5) return "Mild Anxiety";
    return "Minimal Anxiety";
};

function Chats({ isLightTheme, selectedLanguage }) {
    const [selectedPoint, setSelectedPoint] = useState(0);
    const [clients, setClients] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [showAddForm, setShowAddForm] = useState(false);
    const [selectedClient, setSelectedClient] = useState(null);
    const [analyses, setAnalyses] = useState([]);
    const [selectedAnalysis, setSelectedAnalysis] = useState(null);
    const [showAnalysisForm, setShowAnalysisForm] = useState(false);
    const [isAnalysisLoading, setIsAnalysisLoading] = useState(false);
    const [isMobileView, setIsMobileView] = useState(false);

    const fetchClients = () => {
        const token = getTokenFromCookie();
        setIsLoading(true);
        fetch('https://metaltech.onrender.com/clients/get', {
            headers: {
                'Authorization': token
            }
        })
            .then(response => response.json())
            .then(data => {
                setClients(data);
                setIsLoading(false);
            })
            .catch(error => {
                console.error('Error fetching clients:', error);
                setIsLoading(false);
            });
    };

    const fetchAnalyses = (clientId) => {
        const token = getTokenFromCookie();
        setIsAnalysisLoading(true);
        fetch(`https://metaltech.onrender.com/analyses/get/${clientId}`, {
            headers: {
                'Authorization': token
            }
        })
            .then(response => response.json())
            .then(data => {
                setAnalyses(data);
                setIsAnalysisLoading(false);
                setSelectedAnalysis(data.length > 0 ? data[0] : null);
            })
            .catch(error => {
                console.error('Error fetching analyses:', error);
                setIsAnalysisLoading(false);
            });
    };

    useEffect(() => {
        fetchClients();
    }, []);

    useEffect(() => {
        const handleResize = () => {
            setIsMobileView(window.innerWidth <= 768); // Adjust the breakpoint as needed
        };

        window.addEventListener('resize', handleResize);
        handleResize(); // Initial check

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    const handlePointClick = (index) => {
        setSelectedPoint(index);
        const client = clients[index];
        setSelectedClient(client);
        fetchAnalyses(client.id);
    };

    const handleAddClient = (newClient) => {
        fetchClients();
    };

    const handleAnalysisClick = (analysis) => {
        setSelectedAnalysis(analysis);
    };

    const toggleAddForm = () => {
        setShowAddForm(!showAddForm);
    };

    const toggleAnalysisForm = () => {
        setShowAnalysisForm(!showAnalysisForm);
    };

    const renderTable = (questions, answers) => {
        return (
            <table className="analysis-table">
                <thead>
                {isMobileView ?
                    <tr>
                        <th>№</th>
                        <th>Вопрос</th>
                        <th>0</th>
                        <th>1</th>
                        <th>2</th>
                        <th>3</th>
                    </tr>
                    : <tr>
                        <th>№</th>
                        <th>Вопрос</th>
                        <th>Никогда (0)</th>
                        <th>Несколько дней (1)</th>
                        <th>Более половины дней (2)</th>
                        <th>Почти каждый день (3)</th>
                    </tr>}
                </thead>
                <tbody>
                {questions.map((question, index) => (
                    <tr key={index}>
                        <td>{index + 1}</td>
                        <td>{question}</td>
                        <td className={answers[index] === '0' ? 'checked' : ''}>{answers[index] === '0' ? '✔' : ''}</td>
                        <td className={answers[index] === '1' ? 'checked' : ''}>{answers[index] === '1' ? '✔' : ''}</td>
                        <td className={answers[index] === '2' ? 'checked' : ''}>{answers[index] === '2' ? '✔' : ''}</td>
                        <td className={answers[index] === '3' ? 'checked' : ''}>{answers[index] === '3' ? '✔' : ''}</td>
                    </tr>
                ))}
                </tbody>
            </table>
        );
    };

    if (isMobileView) {
        return (
            <div className={`chats ${isLightTheme ? '' : 'dark'} mobile`}>
                <div className="chats-points-container mobile">
                    <div className="chats-points mobile">
                        <img src={isLightTheme ? LightPlus : darkPlus} className={'plus'} alt={'plus'} onClick={toggleAddForm} />
                        {isLoading ? (
                            <div className="loading-spinner"></div>
                        ) : (
                            <ul>
                                {clients.map((client, index) => (
                                    <li
                                        key={client.id}
                                        onClick={() => handlePointClick(index)}
                                        className={selectedPoint === index ? 'selected' : ''}
                                    >
                                        {client.name}
                                    </li>
                                ))}
                            </ul>
                        )}
                    </div>
                    {selectedClient && (
                        <div className="analyses-points mobile">
                            <img src={isLightTheme ? LightPlus : darkPlus} className={'plus'} alt={'plus'} onClick={toggleAnalysisForm} />
                            {isAnalysisLoading ? (
                                <div className="loading-spinner"></div>
                            ) : (
                                <ul>
                                    {analyses.map((analysis) => (
                                        <li
                                            key={analysis.id}
                                            onClick={() => handleAnalysisClick(analysis)}
                                            className={selectedAnalysis && selectedAnalysis.id === analysis.id ? 'selected' : ''}
                                        >
                                            {new Date(analysis.date).toLocaleString()}
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>
                    )}
                </div>
                <div className="chats-item mobile">
                    {selectedAnalysis ? (
                        <div>
                            <h2>Analysis Details</h2>
                            <p>Date: {new Date(selectedAnalysis.date).toLocaleString()}</p>
                            <p>Anxiety Total: {selectedAnalysis.dep_total}</p>
                            <p>Anxiety Classification: {getAnxietyClassification(selectedAnalysis.dep_total)}</p>
                            <h3>Anxiety Status:</h3>
                            {renderTable(questionsGAD7[selectedLanguage], selectedAnalysis.dep_stat)}
                            <p>Depression Total: {selectedAnalysis.anx_total}</p>
                            <p>Depression Classification: {getDepressionClassification(selectedAnalysis.anx_total)}</p>
                            <h3>Depression Status:</h3>
                            {renderTable(questionsPHQ9[selectedLanguage], selectedAnalysis.anx_stat)}
                        </div>
                    ) : (
                        <div>
                            <h2>Select an analysis or upload a new one</h2>
                        </div>
                    )}
                </div>
                {showAddForm && (
                    <ClientAddForm
                        isLightTheme={isLightTheme}
                        closeForms={toggleAddForm}
                        handleAddClient={handleAddClient}
                    />
                )}
                {showAnalysisForm && (
                    <AnalysisAddForm
                        isLightTheme={isLightTheme}
                        closeForms={toggleAnalysisForm}
                        clientId={selectedClient.id}
                        fetchAnalyses={fetchAnalyses}
                    />
                )}
            </div>
        );
    }

    return (
        <div className={`chats ${isLightTheme ? '' : 'dark'}`}>
            <div className="chats-points">
                <img src={isLightTheme ? LightPlus : darkPlus} className={'plus'} alt={'plus'} onClick={toggleAddForm} />
                {isLoading ? (
                    <div className="loading-spinner"></div>
                ) : (
                    <ul>
                        {clients.map((client, index) => (
                            <li
                                key={client.id}
                                onClick={() => handlePointClick(index)}
                                className={selectedPoint === index ? 'selected' : ''}
                            >
                                {client.name}
                            </li>
                        ))}
                    </ul>
                )}
            </div>
            {selectedClient && (
                <div className="analyses-points">
                    <img src={isLightTheme ? LightPlus : darkPlus} className={'plus'} alt={'plus'} onClick={toggleAnalysisForm} />
                    {isAnalysisLoading ? (
                        <div className="loading-spinner"></div>
                    ) : (
                        <ul>
                            {analyses.map((analysis) => (
                                <li
                                    key={analysis.id}
                                    onClick={() => handleAnalysisClick(analysis)}
                                    className={selectedAnalysis && selectedAnalysis.id === analysis.id ? 'selected' : ''}
                                >
                                    {new Date(analysis.date).toLocaleString()}
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            )}
            <div className="chats-item">
                {selectedAnalysis ? (
                    <div>
                        <h2>Analysis Details</h2>
                        <p>Date: {new Date(selectedAnalysis.date).toLocaleString()}</p>
                        <p>Anxiety Total: {selectedAnalysis.dep_total}</p>
                        <p>Anxiety Classification: {getAnxietyClassification(selectedAnalysis.dep_total)}</p>
                        <h3>Anxiety Status:</h3>
                        {renderTable(questionsGAD7[selectedLanguage], selectedAnalysis.dep_stat)}
                        <p>Depression Total: {selectedAnalysis.anx_total}</p>
                        <p>Depression Classification: {getDepressionClassification(selectedAnalysis.anx_total)}</p>
                        <h3>Depression Status:</h3>
                        {renderTable(questionsPHQ9[selectedLanguage], selectedAnalysis.anx_stat)}
                    </div>
                ) : (
                    <div>
                        <h2>Select an analysis or upload a new one</h2>
                    </div>
                )}
            </div>
            {showAddForm && (
                <ClientAddForm
                    isLightTheme={isLightTheme}
                    closeForms={toggleAddForm}
                    handleAddClient={handleAddClient}
                />
            )}
            {showAnalysisForm && (
                <AnalysisAddForm
                    isLightTheme={isLightTheme}
                    closeForms={toggleAnalysisForm}
                    clientId={selectedClient.id}
                    fetchAnalyses={fetchAnalyses}
                />
            )}
        </div>
    );
}

export default Chats;
