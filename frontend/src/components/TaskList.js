import React, { useState, useEffect, useRef, useCallback } from 'react';
import api from '../api';
import InfiniteScroll from 'react-infinite-scroll-component';
import { Container, Button, Modal, Form, Badge } from 'react-bootstrap';
import { debounce } from 'lodash';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [filter, setFilter] = useState({ category: '', priority: '', state: '' });
  const [search, setSearch] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    due_date: '',
    priority: '',
    category: '',
    state: 'Open',
  });
  const [editTask, setEditTask] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Ref to track initial render
  const isFirstRender = useRef(true);

  // Fetch users (note: this function isn't used but kept here in case it's needed later)
  const fetchUsers = async () => {
    try {
      const response = await api.get('/accounts/users/');
      const users = response.data;
      // You can set the users state here if needed
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  useEffect(() => {
    let isCancelled = false;

    const initialize = async () => {
      if (isFirstRender.current) {
        isFirstRender.current = false;
        await fetchUsers();
        if (!isCancelled) {
          await fetchTasks(true);
        }
      } else {
        if (!isCancelled) {
          await fetchTasks(true);
        }
      }
    };

    initialize();

    return () => {
      isCancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter, search]);

  const fetchTasks = async (reset = false) => {
    setIsLoading(true);
    try {
      const config = {
        params: {
          page: reset ? 1 : page,
          search: search.trim(),
          ...filter,
        },
      };

      console.log('Fetching tasks with config:', config);

      const response = await api.get('/tasks/tasks/', config);
      console.log('Fetched tasks:', response.data);

      if (response.status === 200 && Array.isArray(response.data)) {
        if (reset) {
          setTasks(response.data);
          setPage(2);
          setHasMore(response.data.length > 0);
        } else {
          setTasks((prevTasks) => [...prevTasks, ...response.data]);
          setPage((prevPage) => prevPage + 1);
          setHasMore(response.data.length > 0);
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
    } finally {
      setIsLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilter((prevFilter) => {
      if (prevFilter[name] === value) return prevFilter; // No change
      return { ...prevFilter, [name]: value };
    });
  };

  // Debounce search input to prevent rapid calls
  const debouncedSetSearch = useCallback(
    debounce((value) => {
      setSearch(value);
    }, 500),
    []
  );

  const handleSearchChange = (e) => {
    debouncedSetSearch(e.target.value);
  };

  const handleChange = (e) => {
    setNewTask({ ...newTask, [e.target.name]: e.target.value });
  };

  const handleEditChange = (e) => {
    setEditTask({ ...editTask, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const taskData = {
        ...newTask,
        owners: [1], // Replace with actual logged-in user's ID
      };
      console.log('Task data to be submitted:', taskData);

      const response = await api.post('/tasks/tasks/', taskData);

      setTasks([response.data, ...tasks]);
      handleClose();
      setNewTask({
        title: '',
        description: '',
        due_date: '',
        priority: '',
        category: '',
        state: 'Open',
      });
    } catch (error) {
      console.error('Error creating task:', error.response || error.message);

      if (error.response && error.response.data) {
        alert(`Backend error: ${JSON.stringify(error.response.data)}`);
      }

      if (error.response && error.response.status === 401) {
        alert('Authorization failed. Please log in again.');
        window.location.href = '/login';
      }
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    try {
      const response = await api.put(`/tasks/tasks/${editTask.id}/`, editTask);
      setTasks(tasks.map((task) => (task.id === editTask.id ? response.data : task)));
      handleEditClose();
      setEditTask(null);
    } catch (error) {
      console.error('Error updating task:', error.response || error.message);
      if (error.response && error.response.status === 401) {
        alert('Authorization failed. Please log in again.');
        window.location.href = '/login';
      }
    }
  };

  const handleShow = () => setShowModal(true);
  const handleClose = () => setShowModal(false);

  const [showEditModal, setShowEditModal] = useState(false);
  const handleEditShow = (task) => {
    setEditTask(task);
    setShowEditModal(true);
  };
  const handleEditClose = () => setShowEditModal(false);

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;
    try {
      await api.delete(`/tasks/tasks/${id}/`);
      setTasks(tasks.filter((task) => task.id !== id));
    } catch (error) {
      console.error('Error deleting task:', error);
      alert('Failed to delete task.');
    }
  };

  return (
    <Container className="mt-4">
      <h2>Task List</h2>
      <Button variant="primary" onClick={handleShow} className="mb-3">
        Add Task
      </Button>

      {/* Filters */}
      <div className="filters mb-3 d-flex flex-wrap">
        <Form.Select
          name="category"
          value={filter.category}
          onChange={handleFilterChange}
          className="me-2 mb-2"
          aria-label="Filter by Category"
        >
          <option value="">All Categories</option>
          <option value="Work">Work</option>
          <option value="Personal">Personal</option>
          <option value="Others">Others</option>
        </Form.Select>
        <Form.Select
          name="priority"
          value={filter.priority}
          onChange={handleFilterChange}
          className="me-2 mb-2"
          aria-label="Filter by Priority"
        >
          <option value="">All Priorities</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </Form.Select>
        <Form.Select
          name="state"
          value={filter.state}
          onChange={handleFilterChange}
          className="me-2 mb-2"
          aria-label="Filter by State"
        >
          <option value="">All States</option>
          <option value="Open">Open</option>
          <option value="In Progress">In Progress</option>
          <option value="Done">Done</option>
        </Form.Select>
      </div>

      {/* Search */}
      <Form.Control
        type="text"
        placeholder="Search tasks"
        defaultValue={search}
        onChange={handleSearchChange}
        className="mb-3"
      />

      {/* Infinite Scroll */}
      <InfiniteScroll
        dataLength={tasks.length}
        next={() => fetchTasks(false)} // Load more tasks
        hasMore={hasMore}
        loader={isLoading ? <h4>Loading...</h4> : null}
        endMessage={!isLoading && <p>No more tasks</p>}
      >
        <ul className="list-group">
          {tasks.map((task, index) => (
            <li
              key={`${task.id}-${index}`}
              className="list-group-item d-flex justify-content-between align-items-center"
            >
              <div>
                <h5>{task.title}</h5>
                <p>
                  Due: {task.due_date} | Priority:{' '}
                  <Badge
                    bg={
                      task.priority === 'High'
                        ? 'danger'
                        : task.priority === 'Medium'
                        ? 'warning'
                        : 'success'
                    }
                  >
                    {task.priority}
                  </Badge>{' '}
                  | Category: {task.category} | State: {task.state}
                </p>
              </div>
              <div>
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => handleEditShow(task)}
                  className="me-2"
                >
                  Edit
                </Button>
                <Button variant="danger" size="sm" onClick={() => handleDelete(task.id)}>
                  Delete
                </Button>
              </div>
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
              <Form.Select
                name="priority"
                value={newTask.priority}
                onChange={handleChange}
                required
              >
                <option value="">Select Priority</option>
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
              </Form.Select>
            </Form.Group>

            <Form.Group controlId="formTaskCategory" className="mt-2">
              <Form.Label>Category</Form.Label>
              <Form.Select
                name="category"
                value={newTask.category}
                onChange={handleChange}
                required
              >
                <option value="">Select Category</option>
                <option value="Work">Work</option>
                <option value="Personal">Personal</option>
                <option value="Others">Others</option>
              </Form.Select>
            </Form.Group>

            <Form.Group controlId="formTaskState" className="mt-2">
              <Form.Label>State</Form.Label>
              <Form.Select
                name="state"
                value={newTask.state}
                onChange={handleChange}
                required
              >
                <option value="Open">Open</option>
                <option value="In Progress">In Progress</option>
                <option value="Done">Done</option>
              </Form.Select>
            </Form.Group>

            <Button variant="primary" type="submit" className="mt-3">
              Add Task
            </Button>
          </Form>
        </Modal.Body>
      </Modal>

      {/* Modal for Editing Task */}
      <Modal show={showEditModal} onHide={handleEditClose}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Task</Modal.Title>
        </Modal.Header>
        {editTask && (
          <Modal.Body>
            <Form onSubmit={handleUpdate}>
              <Form.Group controlId="formEditTaskTitle">
                <Form.Label>Title</Form.Label>
                <Form.Control
                  type="text"
                  name="title"
                  placeholder="Enter task title"
                  value={editTask.title}
                  onChange={handleEditChange}
                  required
                />
              </Form.Group>

              <Form.Group controlId="formEditTaskDescription" className="mt-2">
                <Form.Label>Description</Form.Label>
                <Form.Control
                  as="textarea"
                  rows={3}
                  name="description"
                  placeholder="Enter task description"
                  value={editTask.description}
                  onChange={handleEditChange}
                />
              </Form.Group>

              <Form.Group controlId="formEditTaskDueDate" className="mt-2">
                <Form.Label>Due Date</Form.Label>
                <Form.Control
                  type="date"
                  name="due_date"
                  value={editTask.due_date}
                  onChange={handleEditChange}
                  required
                />
              </Form.Group>

              <Form.Group controlId="formEditTaskPriority" className="mt-2">
                <Form.Label>Priority</Form.Label>
                <Form.Select
                  name="priority"
                  value={editTask.priority}
                  onChange={handleEditChange}
                  required
                >
                  <option value="">Select Priority</option>
                  <option value="Low">Low</option>
                  <option value="Medium">Medium</option>
                  <option value="High">High</option>
                </Form.Select>
              </Form.Group>

              <Form.Group controlId="formEditTaskCategory" className="mt-2">
                <Form.Label>Category</Form.Label>
                <Form.Select
                  name="category"
                  value={editTask.category}
                  onChange={handleEditChange}
                  required
                >
                  <option value="">Select Category</option>
                  <option value="Work">Work</option>
                  <option value="Personal">Personal</option>
                  <option value="Others">Others</option>
                </Form.Select>
              </Form.Group>

              <Form.Group controlId="formEditTaskState" className="mt-2">
                <Form.Label>State</Form.Label>
                <Form.Select
                  name="state"
                  value={editTask.state}
                  onChange={handleEditChange}
                  required
                >
                  <option value="Open">Open</option>
                  <option value="In Progress">In Progress</option>
                  <option value="Done">Done</option>
                </Form.Select>
              </Form.Group>

              <Button variant="primary" type="submit" className="mt-3">
                Update Task
              </Button>
            </Form>
          </Modal.Body>
        )}
      </Modal>
    </Container>
  );
};

export default TaskList;
