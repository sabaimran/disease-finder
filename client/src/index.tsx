import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import App from './App';
import { DisorderDisplayBox } from './components/DisorderDisplayBox';
import { SymptomSearchBox } from './components/SymptomSearchBox';
import { MostRelevantDiseases } from './components/MostRelevantDiseases';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
    <React.StrictMode>
        <BrowserRouter>
        <Routes>
            <Route path="/" element={<App />} />
            <Route path="disorders" element={<DisorderDisplayBox />} />
            <Route path="symptoms" element={<SymptomSearchBox />} />
            <Route path="results" element={<MostRelevantDiseases />} />
        </Routes>
    </BrowserRouter>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
