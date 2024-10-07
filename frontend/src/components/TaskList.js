import React, { useEffect, useState } from 'react';
import api from '../api';  // Import the Axios instance
import InfiniteScroll from 'react-infinite-scroll-component';  // Import infinite scroll package
import { Container, Button, Modal, Form } from 'react-bootstrap';  // Import Bootstrap components

const TaskList = () => {
  const [tasks, setTasks] = useState([]);  // Store tasks
  const [page, setPage] = useState(1);  // Page for infinite scrolling
  const [hasMore, setHasMore] = useState(true);  // To check if there are more tasks to load
  const [filter, setFilter] = useState({ category: '', priority: '' });  // Store filter settings
  const [search, setSearch] = useState('');  // Store search keyword
  const [showModal, setShowModal] = useState(false);  // Control modal visibility for adding tasks
  const [newTask, setNewTask] = useState({ title: '', description: '', due_date: '', priority: '' });  // New task details

  // Fetch tasks from the API with pagination and filters
  const fetchTasks = async () => {
    try {
      const response = await api.get('tasks/', { params: { page, search, ...filter } });
      setTasks((prevTasks) => [...prevTasks, ...response.data.results]);
      setPage(page + 1);  // Increment page for infinite scrolling
      if (!response.data.next) {
        setHasMore(false);  // No more tasks to load
      }
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  // Initial fetch and when filters/search changes
  useEffect(() => {
    setTasks([]);  // Reset task list
    setPage(1);  // Reset page
    setHasMore(true);  // Reset infinite scroll
    fetchTasks();  // Fetch tasks
  }, [filter, search]);

  // Handle form input changes for creating new tasks
  const handleChange = (e) => {
    setNewTask({ ...newTask, [e.target.name]: e.target.value });
  };

  // Submit new task to the API
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('tasks/', newTask);
      setTasks([response.data, ...tasks]);  // Add new task to the list
      handleClose();  // Close the modal
    } catch (error) {
      console.error('Error creating task:', error);
    }
  };

  // Handle modal opening
  const handleShow = () => setShowModal(true);

  // Handle modal closing
  const handleClose = () => setShowModal(false);

  // Task deletion
  const handleDelete = async (id) => {
    try {
      await api.delete(`tasks/${id}/`);
      setTasks(tasks.filter(task => task.id !== id));  // Remove deleted task from list
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  };

  return (
    <Container className="mt-4">
      <h2>Task List</h2>
      <Button variant="primary" onClick={handleShow} className="mb-3">Add Task</Button>

      {/* Filter options for category and priority */}
      <div className="filters mb-3">
        <select onChange={(e) => setFilter({ ...filter, category: e.target.value })} className="mr-2">
          <option value="">All Categories</option>
          <option value="Work">Work</option>
          <option value="Personal">Personal</option>
        </select>
        <select onChange={(e) => setFilter({ ...filter, priority: e.target.value })}>
          <option value="">All Priorities</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
      </div>

      {/* Search field */}
      <input
        type="text"
        placeholder="Search tasks"
        onChange={(e) => setSearch(e.target.value)}
        className="mb-3"
      />

      {/* Infinite Scroll Component */}
      <InfiniteScroll
        dataLength={tasks.length}
        next={fetchTasks}  // Fetch next page of tasks
        hasMore={hasMore}
        loader={<h4>Loading...</h4>}
        endMessage={<p>No more tasks</p>}
      >
        <ul>
          {tasks.map(task => (
            <li key={task.id}>
              {task.title} - {task.due_date} - {task.priority} - {task.category}
              <Button variant="danger" className="ml-3" onClick={() => handleDelete(task.id)}>
                Delete
              </Button>
            </li>
          ))}
        </ul>
      </InfiniteScroll>

      {/* Modal for Adding a New Task */}
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
