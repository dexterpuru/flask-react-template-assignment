import * as React from 'react';
import { Button } from 'frontend/components';
import { Task } from 'frontend/types/tasks';
import TaskItem from './task-item.component';

interface TaskListProps {
  tasks: Task[];
  onCreateNew: () => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onView: (task: Task) => void;
  onLoadMore?: () => void;
  hasMore?: boolean;
  isLoading?: boolean;
  deletingTaskId?: string;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onCreateNew,
  onEdit,
  onDelete,
  onView,
  onLoadMore,
  hasMore = false,
  isLoading = false,
  deletingTaskId,
}) => {
  if (tasks.length === 0 && !isLoading) {
    return (
      <div className="task-list-empty">
        <h3>No tasks yet</h3>
        <p>Create your first task to get started.</p>
        <Button onClick={onCreateNew}>Create Task</Button>
      </div>
    );
  }

  return (
    <div className="task-list">
      <div className="task-list-header">
        <h2>Tasks</h2>
        <Button onClick={onCreateNew}>Create New Task</Button>
      </div>

      <div className="task-list-items">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onEdit={onEdit}
            onDelete={onDelete}
            onView={onView}
            isDeleting={deletingTaskId === task.id}
          />
        ))}
      </div>

      {hasMore && (
        <div className="task-list-load-more">
          <Button onClick={onLoadMore} disabled={isLoading}>
            {isLoading ? 'Loading...' : 'Load More'}
          </Button>
        </div>
      )}
    </div>
  );
};

export default TaskList;
