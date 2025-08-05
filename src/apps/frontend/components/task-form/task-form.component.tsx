import * as React from 'react';
import './task-form.styles.css';

interface TaskFormProps {
  onSubmit: (data: { title: string; description: string }) => void;
  isLoading?: boolean;
}

const TaskForm: React.FC<TaskFormProps> = ({ onSubmit, isLoading = false }) => {
  const [newTaskTitle, setNewTaskTitle] = React.useState('');
  const [newTaskDescription, setNewTaskDescription] = React.useState('');

  const handleAddTask = () => {
    if (newTaskTitle.trim() && newTaskDescription.trim()) {
      onSubmit({
        title: newTaskTitle.trim(),
        description: newTaskDescription.trim(),
      });
      setNewTaskTitle('');
      setNewTaskDescription('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      e.preventDefault();
      handleAddTask();
    }
  };

  return (
    <div className="task-input-container">
      <div className="task-input-form">
        <div className="task-input-fields">
          <input
            type="text"
            className="task-input-title"
            placeholder="Add new task"
            value={newTaskTitle}
            onChange={(e) => setNewTaskTitle(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
          />
          <textarea
            className="task-input-description"
            placeholder="Description"
            value={newTaskDescription}
            onChange={(e) => setNewTaskDescription(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={isLoading}
            rows={2}
          />
        </div>
        <button
          type="button"
          className="task-add-button"
          onClick={handleAddTask}
          disabled={
            !newTaskTitle.trim() || !newTaskDescription.trim() || isLoading
          }
          title="Add task (Ctrl+Enter)"
        >
          +
        </button>
      </div>
    </div>
  );
};

export default TaskForm;
