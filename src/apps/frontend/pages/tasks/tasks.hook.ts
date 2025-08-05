import * as React from 'react';
import { TaskService } from 'frontend/services';
import {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
} from 'frontend/types/tasks';
import useAsync from 'frontend/contexts/async.hook';
import { useAccountContext } from 'frontend/contexts';
import { getAccessTokenFromStorage } from 'frontend/utils/storage-util';

export const useTasks = () => {
  const { accountDetails: account } = useAccountContext();
  const accessToken = getAccessTokenFromStorage();
  const taskService = React.useMemo(() => new TaskService(), []);
  const [tasks, setTasks] = React.useState<Task[]>([]);
  const [currentPage, setCurrentPage] = React.useState(1);
  const [totalTasks, setTotalTasks] = React.useState(0);
  const [hasMore, setHasMore] = React.useState(false);
  const pageSize = 10;

  if (!accessToken || !account) {
    throw new Error('User must be authenticated to use tasks');
  }

  // Create separate async hooks for each operation
  const loadTasksAsync = useAsync(async (page: number, size: number) =>
    taskService.getTasks(account.id, page, size, accessToken),
  );

  const createTaskAsync = useAsync(async (taskData: CreateTaskRequest) =>
    taskService.createTask(account.id, taskData, accessToken),
  );

  const updateTaskAsync = useAsync(
    async (taskId: string, taskData: UpdateTaskRequest) =>
      taskService.updateTask(account.id, taskId, taskData, accessToken),
  );

  const deleteTaskAsync = useAsync(async (taskId: string) =>
    taskService.deleteTask(account.id, taskId, accessToken),
  );

  const fetchTasks = React.useCallback(
    async (page: number = 1, append: boolean = false) => {
      try {
        const response = await loadTasksAsync.asyncCallback(page, pageSize);

        if (response) {
          const newTasks = append
            ? [...tasks, ...response.items]
            : response.items;
          setTasks(newTasks);
          setTotalTasks(response.total);
          setCurrentPage(page);
          setHasMore(response.total > newTasks.length);
        }
      } catch (error) {
        console.error('Failed to fetch tasks:', error);
      }
    },
    [loadTasksAsync.asyncCallback, pageSize, tasks],
  );

  const handleCreateTask = React.useCallback(
    async (taskData: CreateTaskRequest) => {
      try {
        const response = await createTaskAsync.asyncCallback(taskData);

        if (response) {
          setTasks((prevTasks) => [response, ...prevTasks]);
          setTotalTasks((prev) => prev + 1);
          return response;
        }
        return null;
      } catch (error) {
        console.error('Failed to create task:', error);
        return null;
      }
    },
    [createTaskAsync.asyncCallback],
  );

  const handleUpdateTask = React.useCallback(
    async (taskId: string, taskData: UpdateTaskRequest) => {
      try {
        const response = await updateTaskAsync.asyncCallback(taskId, taskData);

        if (response) {
          setTasks((prevTasks) =>
            prevTasks.map((task) => (task.id === taskId ? response : task)),
          );
          return response;
        }
        return null;
      } catch (error) {
        console.error('Failed to update task:', error);
        return null;
      }
    },
    [updateTaskAsync.asyncCallback],
  );

  const handleDeleteTask = React.useCallback(
    async (taskId: string) => {
      try {
        await deleteTaskAsync.asyncCallback(taskId);
        setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
        setTotalTasks((prev) => prev - 1);
        return true;
      } catch (error) {
        console.error('Failed to delete task:', error);
        return false;
      }
    },
    [deleteTaskAsync.asyncCallback],
  );

  const loadMoreTasks = React.useCallback(() => {
    if (hasMore && !loadTasksAsync.isLoading) {
      fetchTasks(currentPage + 1, true);
    }
  }, [hasMore, loadTasksAsync.isLoading, fetchTasks, currentPage]);

  const refreshTasks = React.useCallback(() => {
    fetchTasks(1, false);
  }, [fetchTasks]);

  // Load initial tasks
  React.useEffect(() => {
    if (account?.id) {
      fetchTasks(1, false);
    }
  }, [account?.id]); // Only depend on account.id to avoid infinite loop

  return {
    // Data
    tasks,
    totalTasks,
    hasMore,
    currentPage,

    // Loading states
    isLoadingTasks: loadTasksAsync.isLoading,
    isCreatingTask: createTaskAsync.isLoading,
    isUpdatingTask: updateTaskAsync.isLoading,
    isDeletingTask: deleteTaskAsync.isLoading,

    // Errors
    loadTasksError: loadTasksAsync.error,
    createTaskError: createTaskAsync.error,
    updateTaskError: updateTaskAsync.error,
    deleteTaskError: deleteTaskAsync.error,

    // Actions
    createTask: handleCreateTask,
    updateTask: handleUpdateTask,
    deleteTask: handleDeleteTask,
    loadMoreTasks,
    refreshTasks,
  };
};
