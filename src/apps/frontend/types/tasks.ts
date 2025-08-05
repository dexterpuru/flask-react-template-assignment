export interface Task {
  id: string;
  account_id: string;
  title: string;
  description: string;
}

export interface CreateTaskRequest {
  title: string;
  description: string;
}

export interface UpdateTaskRequest {
  title: string;
  description: string;
}

export interface TasksResponse {
  items: Task[];
  total: number;
  page: number;
  size: number;
}
