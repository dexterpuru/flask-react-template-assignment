import APIService from 'frontend/services/api.service';
import { ApiResponse, AccessToken } from 'frontend/types';
import {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
  TasksResponse,
} from 'frontend/types';

export default class TaskService extends APIService {
  private getAuthHeaders(accessToken: AccessToken) {
    return {
      headers: {
        Authorization: `Bearer ${accessToken.token}`,
      },
    };
  }

  createTask = async (
    accountId: string,
    taskData: CreateTaskRequest,
    accessToken: AccessToken,
  ): Promise<ApiResponse<Task>> => {
    const response = await this.apiClient.post<Task>(
      `/accounts/${accountId}/tasks`,
      {
        title: taskData.title,
        description: taskData.description,
      },
      this.getAuthHeaders(accessToken),
    );
    return new ApiResponse(response.data);
  };

  getTasks = async (
    accountId: string,
    page: number = 1,
    size: number = 10,
    accessToken: AccessToken,
  ): Promise<ApiResponse<TasksResponse>> => {
    const response = await this.apiClient.get<TasksResponse>(
      `/accounts/${accountId}/tasks?page=${page}&size=${size}`,
      this.getAuthHeaders(accessToken),
    );
    return new ApiResponse(response.data);
  };

  getTask = async (
    accountId: string,
    taskId: string,
    accessToken: AccessToken,
  ): Promise<ApiResponse<Task>> => {
    const response = await this.apiClient.get<Task>(
      `/accounts/${accountId}/tasks/${taskId}`,
      this.getAuthHeaders(accessToken),
    );
    return new ApiResponse(response.data);
  };

  updateTask = async (
    accountId: string,
    taskId: string,
    taskData: UpdateTaskRequest,
    accessToken: AccessToken,
  ): Promise<ApiResponse<Task>> => {
    const response = await this.apiClient.patch<Task>(
      `/accounts/${accountId}/tasks/${taskId}`,
      {
        title: taskData.title,
        description: taskData.description,
      },
      this.getAuthHeaders(accessToken),
    );
    return new ApiResponse(response.data);
  };

  deleteTask = async (
    accountId: string,
    taskId: string,
    accessToken: AccessToken,
  ): Promise<ApiResponse<void>> => {
    await this.apiClient.delete(
      `/accounts/${accountId}/tasks/${taskId}`,
      this.getAuthHeaders(accessToken),
    );
    return new ApiResponse(undefined);
  };
}
