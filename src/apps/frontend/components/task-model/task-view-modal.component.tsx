import * as React from 'react';
import { Button } from 'frontend/components';
import { Task } from 'frontend/types/tasks';
import { ButtonKind } from 'frontend/types/button';

interface TaskViewModalProps {
  isOpen: boolean;
  onClose: () => void;
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  isDeleting?: boolean;
}

const TaskViewModal: React.FC<TaskViewModalProps> = ({
  isOpen,
  onClose,
  task,
  onEdit,
  onDelete,
  isDeleting = false,
}) => {
  if (!isOpen) return null;

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="task-modal-backdrop" onClick={handleBackdropClick}>
      <div className="task-modal">
        <div className="task-modal-header">
          <h2>Task Details</h2>
          <button
            type="button"
            className="task-modal-close"
            onClick={onClose}
            disabled={isDeleting}
          >
            ×
          </button>
        </div>
        <div className="task-modal-body">
          <div className="task-view-content">
            <div className="task-view-field">
              <label>Title:</label>
              <h3>{task.title}</h3>
            </div>
            <div className="task-view-field">
              <label>Description:</label>
              <p>{task.description}</p>
            </div>
          </div>
          <div className="task-view-actions">
            <Button onClick={() => onEdit(task)} disabled={isDeleting}>
              Edit Task
            </Button>
            <Button
              // type={ButtonType.BUTTON}
              onClick={() => onDelete(task.id)}
              disabled={isDeleting}
              kind={ButtonKind.SECONDARY}
            >
              {isDeleting ? 'Deleting...' : 'Delete Task'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskViewModal;
