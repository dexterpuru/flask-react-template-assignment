import * as React from 'react';
import { Button, FormControl, Input } from 'frontend/components';
import { ButtonType } from 'frontend/types/button';
import { Task } from 'frontend/types/tasks';

interface TaskFormProps {
  task?: Task;
  onSubmit: (data: { title: string; description: string }) => void;
  onCancel: () => void;
  isLoading?: boolean;
  submitText?: string;
}

const TaskForm: React.FC<TaskFormProps> = ({
  task,
  onSubmit,
  onCancel,
  isLoading = false,
  submitText = 'Save Task',
}) => {
  const [title, setTitle] = React.useState(task?.title || '');
  const [description, setDescription] = React.useState(task?.description || '');
  const [errors, setErrors] = React.useState<{
    title?: string;
    description?: string;
  }>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const newErrors: { title?: string; description?: string } = {};

    if (!title.trim()) {
      newErrors.title = 'Title is required';
    }

    if (!description.trim()) {
      newErrors.description = 'Description is required';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setErrors({});
    onSubmit({ title: title.trim(), description: description.trim() });
  };

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <FormControl label="Title" error={errors.title}>
        <Input
          id="task-title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title"
          disabled={isLoading}
        />
        {errors.title && <span className="error-text">{errors.title}</span>}
      </FormControl>

      <FormControl label="Description" error={errors.description}>
        <textarea
          id="task-description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description"
          disabled={isLoading}
          rows={4}
          className="task-description-textarea"
        />
        {errors.description && (
          <span className="error-text">{errors.description}</span>
        )}
      </FormControl>

      <div className="task-form-actions">
        <Button
          type={ButtonType.BUTTON}
          onClick={onCancel}
          disabled={isLoading}
        >
          Cancel
        </Button>
        <Button type={ButtonType.SUBMIT} disabled={isLoading}>
          {isLoading ? 'Saving...' : submitText}
        </Button>
      </div>
    </form>
  );
};

export default TaskForm;
