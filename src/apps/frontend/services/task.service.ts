import APIService from 'frontend/services/api.service';
import { ApiResponse } from 'frontend/types';
import {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
  TasksResponse,
} from 'frontend/types';

export default class TaskService extends APIService {
  createTask = async (
    accountId: string,
    taskData: CreateTaskRequest,
  ): Promise<ApiResponse<Task>> => {
    const response = await this.apiClient.post<Task>(
      `/accounts/${accountId}/tasks`,
      {
        title: taskData.title,
        description: taskData.description,
      },
    );
    return new ApiResponse(response.data);
  };

  getTasks = async (
    accountId: string,
    page: number = 1,
    size: number = 10,
  ): Promise<ApiResponse<TasksResponse>> => {
    const response = await this.apiClient.get<TasksResponse>(
      `/accounts/${accountId}/tasks?page=${page}&size=${size}`,
    );
    return new ApiResponse(response.data);
  };

  getTask = async (
    accountId: string,
    taskId: string,
  ): Promise<ApiResponse<Task>> => {
    const response = await this.apiClient.get<Task>(
      `/accounts/${accountId}/tasks/${taskId}`,
    );
    return new ApiResponse(response.data);
  };

  updateTask = async (
    accountId: string,
    taskId: string,
    taskData: UpdateTaskRequest,
  ): Promise<ApiResponse<Task>> => {
    const response = await this.apiClient.patch<Task>(
      `/accounts/${accountId}/tasks/${taskId}`,
      {
        title: taskData.title,
        description: taskData.description,
      },
    );
    return new ApiResponse(response.data);
  };

  deleteTask = async (
    accountId: string,
    taskId: string,
  ): Promise<ApiResponse<void>> => {
    await this.apiClient.delete(`/accounts/${accountId}/tasks/${taskId}`);
    return new ApiResponse(undefined);
  };
}
