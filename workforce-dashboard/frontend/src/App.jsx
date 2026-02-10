import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Today from './pages/Today';
import Timesheet from './pages/Timesheet';
import Activity from './pages/Activity';
import Screenshots from './pages/Screenshots';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Today />} />
          <Route path="/timesheet" element={<Timesheet />} />
          <Route path="/activity" element={<Activity />} />
          <Route path="/screenshots" element={<Screenshots />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
