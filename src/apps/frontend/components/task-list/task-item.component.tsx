import * as React from 'react';
import { Button } from 'frontend/components';
import { ButtonKind, ButtonType } from 'frontend/types/button';
import { Task } from 'frontend/types/tasks';

interface TaskItemProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onView: (task: Task) => void;
  isDeleting?: boolean;
}

const TaskItem: React.FC<TaskItemProps> = ({
  task,
  onEdit,
  onDelete,
  onView,
  isDeleting = false,
}) => {
  return (
    <div className="task-item">
      <div className="task-item-content" onClick={() => onView(task)}>
        <h3 className="task-title">{task.title}</h3>
        <p className="task-description">{task.description}</p>
      </div>
      <div className="task-item-actions">
        <Button
          type={ButtonType.BUTTON}
          onClick={() => onEdit(task)}
          disabled={isDeleting}
        >
          Edit
        </Button>
        <Button
          type={ButtonType.BUTTON}
          onClick={() => onDelete(task.id)}
          disabled={isDeleting}
          kind={ButtonKind.PRIMARY}
        >
          {isDeleting ? 'Deleting...' : 'Delete'}
        </Button>
      </div>
    </div>
  );
};

export default TaskItem;
