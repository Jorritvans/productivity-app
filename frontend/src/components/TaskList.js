import React, { useEffect, useState } from 'react';
import api from '../api';

const TaskList = () => {
    const [tasks, setTasks] = useState([]);
    const [filter, setFilter] = useState({ category: '', priority: '' });
  
    useEffect(() => {
      const fetchTasks = async () => {
        const response = await api.get('tasks/', { params: filter });
        setTasks(response.data);
      };
      fetchTasks();
    }, [filter]);
  
    return (
      <div>
        <select onChange={(e) => setFilter({ ...filter, category: e.target.value })}>
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
        <ul>
          {tasks.map(task => (
            <li key={task.id}>
              {task.title} - {task.category} - {task.priority}
            </li>
          ))}
        </ul>
      </div>
    );
  };
  

export default TaskList;
