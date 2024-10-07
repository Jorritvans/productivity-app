// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './components/Login';
import TaskList from './components/TaskList';
import PrivateRoute from './components/PrivateRoute';
import { Navbar, Nav, Container } from 'react-bootstrap';

function App() {
  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  return (
    <Router>
      {/* Navbar */}
      <Navbar bg="dark" variant="dark" expand="lg">
        <Container>
          <Navbar.Brand href="/">ProductivityApp</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="ml-auto">
              <Nav.Link href="/tasks">Tasks</Nav.Link>
              <Nav.Link onClick={handleLogout}>Logout</Nav.Link>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* Routes */}
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/tasks"
          element={
            <PrivateRoute>
              <TaskList />
            </PrivateRoute>
          }
        />
        <Route path="/" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
