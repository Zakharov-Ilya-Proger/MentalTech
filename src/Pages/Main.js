// Main.js
import React, { useState } from 'react';
import './CSS/Main.css';

const content = {
    en: {
        points: [
            {
                title: 'For Who?',
                description: `
                    <p>Our services are designed for a wide range of professionals and individuals, including:</p>
                    <ul>
                        <li><strong>Psychologists:</strong> Professionals who use our technology to analyze patient interviews and develop personalized treatment plans.</li>
                        <li><strong>Patients:</strong> Individuals seeking mental health support who can monitor their progress and access self-help resources.</li>
                        <li><strong>Researchers:</strong> Scientists and researchers who use our platform to analyze data and conduct studies in mental health.</li>
                        <li><strong>Educational Institutions:</strong> Universities and colleges that use our tools for teaching students and conducting research.</li>
                        <li><strong>Medical Institutions:</strong> Clinics and hospitals that use our technology to improve patient care and optimize psychologist workflows.</li>
                    </ul>
                `
            },
            {
                title: 'Why Us?',
                description: `
                    <p>We offer innovative and effective solutions for mental well-being. Our technology uses advanced algorithms to provide personalized mental health support. Here are some key benefits:</p>
                    <ul>
                        <li>Accelerated diagnosis and increased accuracy in analysis.</li>
                        <li>Access to the latest research and methodologies.</li>
                        <li>Personalized approach to mental health support.</li>
                        <li>Ability to track progress and access self-help resources.</li>
                    </ul>
                `
            },
            {
                title: 'Why is it Necessary?',
                description: `
                    <p>Mental health is crucial for overall well-being and productivity. Early detection and intervention can significantly improve quality of life. Our technology helps in:</p>
                    <ul>
                        <li>Identifying mental health issues early.</li>
                        <li>Providing personalized treatment plans.</li>
                        <li>Improving the efficiency and effectiveness of mental health services.</li>
                    </ul>
                `
            },
            {
                title: 'How Does it Work?',
                description: `
                    <p>Our technology uses advanced algorithms to analyze interview transcripts and predict how a person might fill out anxiety and depression questionnaires. This helps psychologists make more informed decisions. Here’s how it works:</p>
                    <ol>
                        <li>Upload the interview transcript.</li>
                        <li>Our AI analyzes the transcript using natural language processing.</li>
                        <li>The AI predicts how the person might fill out the questionnaires.</li>
                        <li>Psychologists use this information to make more informed decisions.</li>
                    </ol>
                `
            },
            {
                title: 'Our Technologies',
                description: `
                    <p>Our technologies are backed by years of research and development. We use state-of-the-art AI and machine learning techniques to ensure accuracy and reliability. Key features include:</p>
                    <ul>
                        <li>Advanced natural language processing.</li>
                        <li>Machine learning models trained on large datasets.</li>
                        <li>Continuous improvement through feedback and updates.</li>
                    </ul>
                `
            }
        ]
    },
    ru: {
        points: [
            {
                title: 'Для кого?',
                description: `
                    <p>Наши услуги предназначены для широкого круга профессионалов и индивидуальных пользователей, включая:</p>
                    <ul>
                        <li><strong>Психологи:</strong> Профессионалы, которые используют нашу технологию для анализа интервью с пациентами и разработки индивидуальных планов лечения.</li>
                        <li><strong>Пациенты:</strong> Люди, ищущие поддержку в области психического здоровья, которые могут отслеживать свой прогресс и получать доступ к ресурсам для самопомощи.</li>
                        <li><strong>Исследователи:</strong> Ученые и исследователи, которые используют нашу платформу для анализа данных и проведения исследований в области психического здоровья.</li>
                        <li><strong>Образовательные учреждения:</strong> Университеты и колледжи, которые используют наши инструменты для обучения студентов и проведения исследований.</li>
                        <li><strong>Медицинские учреждения:</strong> Клиники и больницы, которые используют нашу технологию для улучшения обслуживания пациентов и оптимизации работы психологов.</li>
                    </ul>
                `
            },
            {
                title: 'Почему мы?',
                description: `
                    <p>Мы предлагаем инновационные и эффективные решения для психического благополучия. Наши технологии используют передовые алгоритмы для предоставления персонализированной поддержки психического здоровья. Вот ключевые преимущества:</p>
                    <ul>
                        <li>Ускорение диагностики и повышение точности анализа.</li>
                        <li>Доступ к последним исследованиям и методикам.</li>
                        <li>Персонализированный подход к поддержке психического здоровья.</li>
                        <li>Возможность отслеживания прогресса и доступ к ресурсам для самопомощи.</li>
                    </ul>
                `
            },
            {
                title: 'Почему это необходимо?',
                description: `
                    <p>Психическое здоровье важно для общего благополучия и продуктивности. Раннее выявление и вмешательство могут значительно улучшить качество жизни. Наша технология помогает в:</p>
                    <ul>
                        <li>Раннем выявлении проблем психического здоровья.</li>
                        <li>Предоставлении индивидуальных планов лечения.</li>
                        <li>Улучшении эффективности и качества услуг в области психического здоровья.</li>
                    </ul>
                `
            },
            {
                title: 'Как это работает?',
                description: `
                    <p>Наши технологии используют передовые алгоритмы для анализа расшифровок интервью и предсказания, как человек мог бы заполнить анкету тревожности и депрессии. Это помогает психологам принимать более обоснованные решения. Вот как это работает:</p>
                    <ol>
                        <li>Загрузите расшифровку интервью.</li>
                        <li>Наша нейронная сеть анализирует расшифровку с использованием обработки естественного языка.</li>
                        <li>Нейронная сеть предсказывает, как человек мог бы заполнить анкету.</li>
                        <li>Психологи используют эту информацию для принятия более обоснованных решений.</li>
                    </ol>
                `
            },
            {
                title: 'Наши технологии',
                description: `
                    <p>Наши технологии подкреплены годами исследований и разработок. Мы используем передовые методы искусственного интеллекта и машинного обучения для обеспечения точности и надежности. Ключевые особенности включают:</p>
                    <ul>
                        <li>Передовая обработка естественного языка.</li>
                        <li>Модели машинного обучения, обученные на больших объемах данных.</li>
                        <li>Непрерывное улучшение через обратную связь и обновления.</li>
                    </ul>
                `
            }
        ]
    }
};

function Main({ isLightTheme, selectedLanguage }) {
    const [selectedPoint, setSelectedPoint] = useState(0);
    const currentContent = content[selectedLanguage];

    const handlePointClick = (index) => {
        setSelectedPoint(index);
    };

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