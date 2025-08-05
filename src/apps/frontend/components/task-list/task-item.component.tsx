import * as React from 'react';
import { Task } from 'frontend/types/tasks';

interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  isDeleting?: boolean;
}

const TaskItem: React.FC<TaskItemProps> = ({
  task,
  onEdit,
  onDelete,
  isDeleting = false,
}) => {
  const [isEditing, setIsEditing] = React.useState(false);
  const [editTitle, setEditTitle] = React.useState(task.title);
  const [editDescription, setEditDescription] = React.useState(
    task.description,
  );

  const handleStartEdit = () => {
    setIsEditing(true);
    setEditTitle(task.title);
    setEditDescription(task.description);
  };

  const handleSaveEdit = () => {
    if (editTitle.trim() && editDescription.trim()) {
      onEdit({
        ...task,
        title: editTitle.trim(),
        description: editDescription.trim(),
      });
      setIsEditing(false);
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditTitle(task.title);
    setEditDescription(task.description);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      e.preventDefault();
      handleSaveEdit();
    } else if (e.key === 'Escape') {
      e.preventDefault();
      handleCancelEdit();
    }
  };

  return (
    <div className="task-item">
      <div className="task-item-content">
        {isEditing ? (
          <div className="task-edit-form">
            <input
              type="text"
              className="task-input-title"
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              onKeyDown={handleKeyDown}
              style={{ marginBottom: '0.5rem' }}
              autoFocus
            />
            <textarea
              className="task-input-description"
              value={editDescription}
              onChange={(e) => setEditDescription(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={3}
            />
          </div>
        ) : (
          <>
            <h3 className="task-title">{task.title}</h3>
            <p className="task-description">{task.description}</p>
          </>
        )}
      </div>
      <div className="task-item-actions">
        {isEditing ? (
          <>
            <button
              type="button"
              className="task-action-icon save"
              onClick={handleSaveEdit}
              disabled={!editTitle.trim() || !editDescription.trim()}
              title="Save changes (Ctrl+Enter)"
            >
              ✓
            </button>
            <button
              type="button"
              className="task-action-icon cancel"
              onClick={handleCancelEdit}
              title="Cancel editing (Esc)"
            >
              ×
            </button>
          </>
        ) : (
          <>
            <button
              type="button"
              className="task-action-icon edit"
              onClick={handleStartEdit}
              disabled={isDeleting}
              title="Edit task"
            >
              ✏️
            </button>
            <button
              type="button"
              className="task-action-icon delete"
              onClick={() => onDelete(task.id)}
              disabled={isDeleting}
              title="Delete task"
            >
              {isDeleting ? '...' : '×'}
            </button>
          </>
        )}
      </div>
    </div>
  );
};

export default TaskItem;
