import * as React from 'react';
import { Task } from 'frontend/types/tasks';
// import { TaskForm } from 'frontend/components/task-form';

interface TaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  task?: Task;
  onSubmit: (data: { title: string; description: string }) => void;
  isLoading?: boolean;
  title: string;
}

const TaskModal: React.FC<TaskModalProps> = ({
  isOpen,
  onClose,
  // task,
  // onSubmit,
  isLoading = false,
  title,
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
          <h2>{title}</h2>
          <button
            type="button"
            className="task-modal-close"
            onClick={onClose}
            disabled={isLoading}
          >
            ×
          </button>
        </div>
        <div className="task-modal-body">
          {/* TaskForm component removed - TaskModal is unused */}
          <p>TaskModal is deprecated and unused</p>
        </div>
      </div>
    </div>
  );
};

export default TaskModal;
