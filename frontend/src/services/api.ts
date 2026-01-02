import axios, { AxiosInstance, AxiosResponse } from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string, params?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.client.post(url, data);
    return response.data;
  }

  async put<T>(url: string, data?: any): Promise<T> {
    const response: AxiosResponse<T> = await this.client.put(url, data);
    return response.data;
  }

  async delete<T>(url: string): Promise<T> {
    const response: AxiosResponse<T> = await this.client.delete(url);
    return response.data;
  }
}

const apiClient = new APIClient();

// Auth API
export const authAPI = {
  login: (credentials: { email: string; password: string }) =>
    apiClient.post('/api/auth/login', credentials),
  register: (userData: { email: string; password: string; name: string }) =>
    apiClient.post('/api/auth/register', userData),
  verifyToken: () => apiClient.get('/api/auth/verify'),
  logout: () => apiClient.post('/api/auth/logout'),
};

// Evolution API
export const evolutionAPI = {
  getRuns: () => apiClient.get('/api/evolution/runs'),
  getRun: (id: string) => apiClient.get(`/api/evolution/runs/${id}`),
  startRun: (config: any) => apiClient.post('/api/evolution/runs', config),
  stopRun: (id: string) => apiClient.post(`/api/evolution/runs/${id}/stop`),
  pauseRun: (id: string) => apiClient.post(`/api/evolution/runs/${id}/pause`),
  resumeRun: (id: string) => apiClient.post(`/api/evolution/runs/${id}/resume`),
  getRunStatus: (id: string) => apiClient.get(`/api/evolution/runs/${id}/status`),
  getRunMetrics: (id: string) => apiClient.get(`/api/evolution/runs/${id}/metrics`),
};

// Programs API
export const programsAPI = {
  getPrograms: (runId: string) => apiClient.get(`/api/programs?runId=${runId}`),
  getProgram: (id: string) => apiClient.get(`/api/programs/${id}`),
  getProgramDetails: (id: string) => apiClient.get(`/api/programs/${id}/details`),
  getProgramCode: (id: string) => apiClient.get(`/api/programs/${id}/code`),
  getProgramMetrics: (id: string) => apiClient.get(`/api/programs/${id}/metrics`),
  evaluateProgram: (id: string) => apiClient.post(`/api/programs/${id}/evaluate`),
};

// Visualization API
export const visualizationAPI = {
  getEvolutionData: (runId: string) => apiClient.get(`/api/visualization/evolution/${runId}`),
  getPerformanceData: (runId: string) => apiClient.get(`/api/visualization/performance/${runId}`),
  getTreeData: (runId: string) => apiClient.get(`/api/visualization/tree/${runId}`),
};

// Configuration API
export const configAPI = {
  getConfigs: () => apiClient.get('/api/config'),
  getConfig: (id: string) => apiClient.get(`/api/config/${id}`),
  createConfig: (config: any) => apiClient.post('/api/config', config),
  updateConfig: (id: string, config: any) => apiClient.put(`/api/config/${id}`, config),
  deleteConfig: (id: string) => apiClient.delete(`/api/config/${id}`),
};

export default apiClient;