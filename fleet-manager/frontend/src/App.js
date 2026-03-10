import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Vehicles from './pages/Vehicles';
import Drivers from './pages/Drivers';
import Incomes from './pages/Incomes';
import Expenses from './pages/Expenses';
import Maintenance from './pages/Maintenance';
import Sidebar from './components/Sidebar';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setIsAuthenticated(true);
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleLogin = (token, userData) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(userData));
    setIsAuthenticated(true);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        {isAuthenticated && <Sidebar user={user} onLogout={handleLogout} />}
        <div className={`flex-1 overflow-auto ${isAuthenticated ? 'ml-64' : ''}`}>
          <Routes>
            <Route 
              path="/login" 
              element={
                isAuthenticated ? 
                <Navigate to="/dashboard" /> : 
                <Login onLogin={handleLogin} />
              } 
            />
            <Route 
              path="/dashboard" 
              element={
                isAuthenticated ? 
                <Dashboard /> : 
                <Navigate to="/login" />
              } 
            />
            <Route 
              path="/vehicles" 
              element={
                isAuthenticated ? 
                <Vehicles /> : 
                <Navigate to="/login" />
              } 
            />
            <Route 
              path="/drivers" 
              element={
                isAuthenticated ? 
                <Drivers /> : 
                <Navigate to="/login" />
              } 
            />
            <Route 
              path="/incomes" 
              element={
                isAuthenticated ? 
                <Incomes /> : 
                <Navigate to="/login" />
              } 
            />
            <Route 
              path="/expenses" 
              element={
                isAuthenticated ? 
                <Expenses /> : 
                <Navigate to="/login" />
              } 
            />
            <Route 
              path="/maintenance" 
              element={
                isAuthenticated ? 
                <Maintenance /> : 
                <Navigate to="/login" />
              } 
            />
            <Route path="/" element={<Navigate to="/dashboard" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
