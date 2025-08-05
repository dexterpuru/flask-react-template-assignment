import * as React from 'react';
import { TaskList } from 'frontend/components';
import { Task } from 'frontend/types/tasks';
// import { useAccountContext } from 'frontend/contexts';
import { useTasks } from './tasks.hook';
import './tasks.style.css';

const TasksPage: React.FC = () => {
  // const { accountDetails: account } = useAccountContext();
  const {
    tasks,
    hasMore,
    isLoadingTasks,
    isCreatingTask,
    // isDeletingTask,
    createTaskError,
    updateTaskError,
    deleteTaskError,
    createTask,
    updateTask,
    deleteTask,
    loadMoreTasks,
  } = useTasks();

  const [deletingTaskId, setDeletingTaskId] = React.useState<
    string | undefined
  >(undefined);

  // Handlers
  const handleCreateNew = async (data: {
    title: string;
    description: string;
  }) => {
    await createTask(data);
  };

  const handleEdit = async (task: Task) => {
    await updateTask(task.id, {
      title: task.title,
      description: task.description,
    });
  };

  const handleDelete = async (taskId: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      setDeletingTaskId(taskId);
      await deleteTask(taskId);
      setDeletingTaskId(undefined);
    }
  };

  return (
    <div className="tasks-page">
      <div className="tasks-page-content">
        {/* Error Messages */}
        {createTaskError && (
          <div className="error-message">
            Failed to create task: {createTaskError.message}
          </div>
        )}
        {updateTaskError && (
          <div className="error-message">
            Failed to update task: {updateTaskError.message}
          </div>
        )}
        {deleteTaskError && (
          <div className="error-message">
            Failed to delete task: {deleteTaskError.message}
          </div>
        )}

        {/* Task List */}
        <TaskList
          tasks={tasks}
          onCreateNew={handleCreateNew}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onLoadMore={loadMoreTasks}
          hasMore={hasMore}
          isLoading={isLoadingTasks}
          isCreating={isCreatingTask}
          deletingTaskId={deletingTaskId}
        />
      </div>
    </div>
  );
};

export default TasksPage;
