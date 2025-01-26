import React, { useState } from 'react';
import './CSS/Main.css';

const content = {
    en: {
        points: [
            { title: 'For Who?', description: 'Our services are designed for psychologists who need help in analyzing patient interviews. By uploading interview transcripts, our AI can predict how a person might fill out anxiety and depression questionnaires.' },
            { title: 'Why Us?', description: 'We offer innovative and effective solutions for mental well-being. Our technology uses advanced algorithms to provide personalized mental health support.' },
            { title: 'Why is it Necessary?', description: 'Mental health is crucial for overall well-being and productivity. Early detection and intervention can significantly improve quality of life.' },
            { title: 'How Does it Work?', description: 'Our technology uses advanced algorithms to analyze interview transcripts and predict how a person might fill out anxiety and depression questionnaires. This helps psychologists make more informed decisions.' },
            { title: 'Our Technologies', description: 'Our technologies are backed by years of research and development. We use state-of-the-art AI and machine learning techniques to ensure accuracy and reliability.' }
        ]
    },
    ru: {
        points: [
            { title: 'Для кого?', description: 'Наши услуги предназначены для психологов, которым нужна помощь в анализе интервью с пациентами. Загрузив расшифровку интервью, наша нейронная сеть может предсказать, как человек мог бы заполнить анкету тревожности и депрессии.' },
            { title: 'Почему мы?', description: 'Мы предлагаем инновационные и эффективные решения для психического благополучия. Наши технологии используют передовые алгоритмы для предоставления персонализированной поддержки психического здоровья.' },
            { title: 'Почему это необходимо?', description: 'Психическое здоровье важно для общего благополучия и продуктивности. Раннее выявление и вмешательство могут значительно улучшить качество жизни.' },
            { title: 'Как это работает?', description: 'Наши технологии используют передовые алгоритмы для анализа расшифровок интервью и предсказания, как человек мог бы заполнить анкету тревожности и депрессии. Это помогает психологам принимать более обоснованные решения.' },
            { title: 'Наши технологии', description: 'Наши технологии подкреплены годами исследований и разработок. Мы используем передовые методы искусственного интеллекта и машинного обучения для обеспечения точности и надежности.' }
        ]
    }
};

function Main({ isLightTheme, selectedLanguage }) {
    const [selectedPoint, setSelectedPoint] = useState(0);
    const currentContent = content[selectedLanguage];

    const handlePointClick = (index) => {
        setSelectedPoint(index);
    };

    if (window.innerHeight < 740) {
        return (
            <div className={`main ${isLightTheme ? '' : 'dark'} mobile`}>
                <div className="main-items">
                    {currentContent.points.map((point, index) => (
                        <div key={index} className="main-item mobile">
                            <h2>{point.title}</h2>
                            <p dangerouslySetInnerHTML={{ __html: point.description }}></p>
                        </div>
                    ))}
                </div>
            </div>
        );
    }

    return (
        <div className={`main ${isLightTheme ? '' : 'dark'}`}>
            <div className="main-points">
                <ul>
                    {currentContent.points.map((point, index) => (
                        <li
                            key={index}
                            onClick={() => handlePointClick(index)}
                            className={selectedPoint === index ? 'selected' : ''}
                        >
                            {point.title}
                        </li>
                    ))}
                </ul>
            </div>
            <div className="main-item">
                <h2>{currentContent.points[selectedPoint].title}</h2>
                <p dangerouslySetInnerHTML={{ __html: currentContent.points[selectedPoint].description }}></p>
            </div>
        </div>
    );
}

export default Main;
