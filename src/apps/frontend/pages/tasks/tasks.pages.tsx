import * as React from 'react';
import { TaskList, TaskModal, TaskViewModal } from 'frontend/components';
import { Task } from 'frontend/types/tasks';
// import { useAccountContext } from 'frontend/contexts';
import { useTasks } from './tasks.hook';

const TasksPage: React.FC = () => {
  // const { accountDetails: account } = useAccountContext();
  const {
    tasks,
    hasMore,
    isLoadingTasks,
    isCreatingTask,
    isUpdatingTask,
    // isDeletingTask,
    createTaskError,
    updateTaskError,
    deleteTaskError,
    createTask,
    updateTask,
    deleteTask,
    loadMoreTasks,
  } = useTasks();

  // Modal states
  const [isCreateModalOpen, setIsCreateModalOpen] = React.useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = React.useState(false);
  const [isViewModalOpen, setIsViewModalOpen] = React.useState(false);
  const [selectedTask, setSelectedTask] = React.useState<Task | null>(null);
  const [deletingTaskId, setDeletingTaskId] = React.useState<
    string | undefined
  >(undefined);

  // Handlers
  const handleCreateNew = () => {
    setIsCreateModalOpen(true);
  };

  const handleCreateSubmit = async (data: {
    title: string;
    description: string;
  }) => {
    const newTask = await createTask(data);
    if (newTask) {
      setIsCreateModalOpen(false);
    }
  };

  const handleEdit = (task: Task) => {
    setSelectedTask(task);
    setIsEditModalOpen(true);
    setIsViewModalOpen(false);
  };

  const handleEditSubmit = async (data: {
    title: string;
    description: string;
  }) => {
    if (selectedTask) {
      const updatedTask = await updateTask(selectedTask.id, data);
      if (updatedTask) {
        setIsEditModalOpen(false);
        setSelectedTask(null);
      }
    }
  };

  const handleView = (task: Task) => {
    setSelectedTask(task);
    setIsViewModalOpen(true);
  };

  const handleDelete = async (taskId: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      setDeletingTaskId(taskId);
      const success = await deleteTask(taskId);
      setDeletingTaskId(undefined);

      if (success && selectedTask?.id === taskId) {
        setIsViewModalOpen(false);
        setSelectedTask(null);
      }
    }
  };

  const handleCloseModals = () => {
    setIsCreateModalOpen(false);
    setIsEditModalOpen(false);
    setIsViewModalOpen(false);
    setSelectedTask(null);
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
          onView={handleView}
          onLoadMore={loadMoreTasks}
          hasMore={hasMore}
          isLoading={isLoadingTasks}
          deletingTaskId={deletingTaskId}
        />

        {/* Create Task Modal */}
        <TaskModal
          isOpen={isCreateModalOpen}
          onClose={handleCloseModals}
          onSubmit={handleCreateSubmit}
          isLoading={isCreatingTask}
          title="Create New Task"
        />

        {/* Edit Task Modal */}
        <TaskModal
          isOpen={isEditModalOpen}
          onClose={handleCloseModals}
          task={selectedTask || undefined}
          onSubmit={handleEditSubmit}
          isLoading={isUpdatingTask}
          title="Edit Task"
        />

        {/* View Task Modal */}
        {selectedTask && (
          <TaskViewModal
            isOpen={isViewModalOpen}
            onClose={handleCloseModals}
            task={selectedTask}
            onEdit={handleEdit}
            onDelete={handleDelete}
            isDeleting={deletingTaskId === selectedTask.id}
          />
        )}
      </div>
    </div>
  );
};

export default TasksPage;
