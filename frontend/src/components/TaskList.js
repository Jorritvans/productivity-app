import React, { useState, useEffect } from 'react';
import api from '../api';
import InfiniteScroll from 'react-infinite-scroll-component';
import { Container, Button, Modal, Form } from 'react-bootstrap';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [filter, setFilter] = useState({ category: '', priority: '' });
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    due_date: '',
    priority: '',
    category: '',
  });

  // Helper function to get the token
  const getToken = () => {
    return localStorage.getItem('token');
  };

  // Fetch tasks from the backend API
  const fetchTasks = async () => {
    try {
      const token = getToken();
      if (!token) {
        console.error('No token found in localStorage. Redirecting to login...');
        alert('You are not logged in. Please login first.');
        window.location.href = '/login';
        return;
      }

      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          page,
          search,
          ...filter,
        },
      };

      const response = await api.get('tasks/', config);

      if (response.status === 200 && Array.isArray(response.data.results)) {
        setTasks((prevTasks) => [...prevTasks, ...response.data.results]);
        setPage(page + 1);
        if (!response.data.next) {
          setHasMore(false);
        }
      } else {
        console.error('Unexpected response structure:', response.data);
      }
    } catch (error) {
      console.error('Error fetching tasks:', error.response || error.message);
      if (error.response && error.response.status === 401) {
        alert('Authorization failed. Please log in again.');
        window.location.href = '/login';
      }
    }
  };

  useEffect(() => {
    setTasks([]);
    setPage(1);
    setHasMore(true);
    fetchTasks();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter, search]);

  const handleChange = (e) => {
    setNewTask({ ...newTask, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const token = getToken();

      if (!token) {
        alert('Please login before adding a task.');
        return;
      }

      const config = {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      };

      const response = await api.post('tasks/', newTask, config);
      setTasks([response.data, ...tasks]);
      handleClose();
    } catch (error) {
      console.error('Error creating task:', error.response || error.message);
      if (error.response && error.response.status === 401) {
        alert('Authorization failed. Please log in again.');
        window.location.href = '/login';
      }
    }
  };

  const handleShow = () => setShowModal(true);
  const handleClose = () => setShowModal(false); // <-- This was missing

  const handleDelete = async (id) => {
    try {
      await api.delete(`tasks/${id}/`);
      setTasks(tasks.filter((task) => task.id !== id));
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  return (
    <Container className="mt-4">
      <h2>Task List</h2>
      <Button variant="primary" onClick={handleShow} className="mb-3">
        Add Task
      </Button>

      {/* Filters */}
      <div className="filters mb-3">
        <select
          onChange={(e) => setFilter({ ...filter, category: e.target.value })}
          className="mr-2"
        >
          <option value="">All Categories</option>
          <option value="Work">Work</option>
          <option value="Personal">Personal</option>
        </select>
        <select
          onChange={(e) => setFilter({ ...filter, priority: e.target.value })}
        >
          <option value="">All Priorities</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
      </div>

      {/* Search */}
      <input
        type="text"
        placeholder="Search tasks"
        onChange={(e) => setSearch(e.target.value)}
        className="mb-3"
      />

      {/* Infinite Scroll */}
      <InfiniteScroll
        dataLength={tasks.length}
        next={fetchTasks}
        hasMore={hasMore}
        loader={<h4>Loading...</h4>}
        endMessage={<p>No more tasks</p>}
      >
        <ul>
          {tasks.map((task) => (
            <li key={task.id}>
              {task.title} - {task.due_date} - {task.priority} - {task.category}
              <Button
                variant="danger"
                className="ml-3"
                onClick={() => handleDelete(task.id)}
              >
                Delete
              </Button>
            </li>
          ))}
        </ul>
      </InfiniteScroll>

      {/* Modal for Adding Task */}
      <Modal show={showModal} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Add New Task</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formTaskTitle">
              <Form.Label>Title</Form.Label>
              <Form.Control
                type="text"
                name="title"
                placeholder="Enter task title"
                value={newTask.title}
                onChange={handleChange}
                required
              />
            </Form.Group>

            <Form.Group controlId="formTaskDescription" className="mt-2">
              <Form.Label>Description</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                name="description"
                placeholder="Enter task description"
                value={newTask.description}
                onChange={handleChange}
              />
            </Form.Group>

            <Form.Group controlId="formTaskDueDate" className="mt-2">
              <Form.Label>Due Date</Form.Label>
              <Form.Control
                type="date"
                name="due_date"
                value={newTask.due_date}
                onChange={handleChange}
                required
              />
            </Form.Group>

            <Form.Group controlId="formTaskPriority" className="mt-2">
              <Form.Label>Priority</Form.Label>
              <Form.Control
                as="select"
                name="priority"
                value={newTask.priority}
                onChange={handleChange}
                required
              >
                <option value="">Select Priority</option>
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </Form.Control>
            </Form.Group>

            <Form.Group controlId="formTaskCategory" className="mt-2">
              <Form.Label>Category</Form.Label>
              <Form.Control
                type="text"
                name="category"
                placeholder="Enter task category"
                value={newTask.category}
                onChange={handleChange}
              />
            </Form.Group>

            <Button variant="primary" type="submit" className="mt-3">
              Add Task
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </Container>
  );
};

export default TaskList;
