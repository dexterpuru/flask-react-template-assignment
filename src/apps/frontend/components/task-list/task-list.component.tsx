import * as React from 'react';
import { Button } from 'frontend/components';
import { Task } from 'frontend/types/tasks';
import { TaskForm } from 'frontend/components/task-form';
import TaskItem from './task-item.component';
import './task-list.styles.css';

interface TaskListProps {
  tasks: Task[];
  onCreateNew: (data: { title: string; description: string }) => void;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onLoadMore?: () => void;
  hasMore?: boolean;
  isLoading?: boolean;
  isCreating?: boolean;
  deletingTaskId?: string;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onCreateNew,
  onEdit,
  onDelete,
  onLoadMore,
  hasMore = false,
  isLoading = false,
  isCreating = false,
  deletingTaskId,
}) => {
  if (tasks.length === 0 && !isLoading) {
    return (
      <div className="task-list">
        <TaskForm onSubmit={onCreateNew} isLoading={isCreating} />

        <div className="task-list-empty">
          <h3>No tasks yet</h3>
          <p>Create your first task to get started.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="task-list">
      <TaskForm onSubmit={onCreateNew} isLoading={isCreating} />

      <div className="task-list-items">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            task={task}
            onEdit={onEdit}
            onDelete={onDelete}
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
