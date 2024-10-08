import React, { useState } from 'react';
import api from '../api'; // Importing the Axios instance
import { useNavigate } from 'react-router-dom';
import { Container, Form, Button } from 'react-bootstrap';

const Register = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const navigate = useNavigate();

  // Handle form submission for registration
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('Registration data:', { username, password, email }); // Debugging

    try {
      // POST request to the backend's registration endpoint
      await api.post('/accounts/register/', { username, password, email });
      alert('Registration successful. Please log in.');
      navigate('/login');
    } catch (error) {
      console.error('Registration failed:', error);
      if (error.response) {
        // Server responded with a status other than 2xx
        console.log('Error response:', error.response.data);
        alert(`Registration failed: ${JSON.stringify(error.response.data)}`);
      } else if (error.request) {
        // Request was made but no response received
        console.log('Error request:', error.request);
        alert('Registration failed: No response from server.');
      } else {
        // Something else happened
        console.log('Error message:', error.message);
        alert(`Registration failed: ${error.message}`);
      }
    }
  };

  return (
    <Container className="mt-4">
      <h2>Register</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formUsername">
          <Form.Label>Username</Form.Label>
          <Form.Control
            type="text"
            name="username"
            placeholder="Enter username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group controlId="formEmail" className="mt-2">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="email"
            name="email"
            placeholder="Enter email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Form.Group>

        <Form.Group controlId="formPassword" className="mt-2">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            name="password"
            placeholder="Enter password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </Form.Group>

        <Button variant="primary" type="submit" className="mt-3">
          Register
        </Button>
      </Form>
    </Container>
  );
};

export default Register;
