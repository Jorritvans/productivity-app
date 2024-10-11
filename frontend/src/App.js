import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar, Nav, Container } from 'react-bootstrap';

import Login from './components/Login';
import Register from './components/Register';
import TaskList from './components/TaskList';

// Helper function to check if the user is authenticated
const isAuthenticated = () => {
  const token = localStorage.getItem('access_token');
  return !!token; // Return true if the token exists
};

function App() {
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = '/login'; // Redirect to login on logout
  };

  return (
    <Router>
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand href="/">ProductivityApp</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ms-auto">
              {isAuthenticated() ? (
                <>
                  <Nav.Link href="/tasks">Tasks</Nav.Link>
                  <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
                </>
              ) : (
                <>
                  <Nav.Link href="/login">Login</Nav.Link>
                  <Nav.Link href="/register">Register</Nav.Link>
                </>
              )}
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Routes>
        <Route path="/login" element={isAuthenticated() ? <Navigate to="/tasks" /> : <Login />} />
        <Route path="/register" element={isAuthenticated() ? <Navigate to="/tasks" /> : <Register />} />
        <Route path="/tasks" element={isAuthenticated() ? <TaskList /> : <Navigate to="/login" />} />
        <Route path="/" element={isAuthenticated() ? <Navigate to="/tasks" /> : <Navigate to="/login" />} />
        <Route path="*" element={<Navigate to="/" />} /> {/* Catch-all route */}
      </Routes>
    </Router>
  );
}

export default App;
