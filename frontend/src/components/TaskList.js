import React, { useEffect, useState } from 'react';
import api from '../api';

const TaskList = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    const fetchTasks = async () => {
      const response = await api.get('tasks/');
      setTasks(response.data);
    };
    fetchTasks();
  }, []);

  return (
    <ul>
      {tasks.map(task => (
        <li key={task.id}>
          {task.title} - {task.due_date} - {task.priority}
        </li>
      ))}
    </ul>
  );
};

export default TaskList;
