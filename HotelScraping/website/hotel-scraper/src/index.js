import React from 'react';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import {createRoot} from "react-dom/client";
import reportWebVitals from './reportWebVitals.js';

import './index.css';

import SearchHotels from "./SearchHotels.js";
import ShowResults from "./ShowResults.js";

const container = document.getElementById("root")
const root = createRoot(container);

root.render(
    <Router>
        <Routes>
            <Route path="/" exact element={<SearchHotels />}/>
            <Route path="/ShowResults" element={<ShowResults />}/>
        </Routes>
    </Router>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
