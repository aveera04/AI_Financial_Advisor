/**
 * API Service for communicating with the FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ChatMessage {
  content: string;
  files?: string[];
}

export interface ChatResponse {
  content: string;
  sources: Source[];
  model: string;
  agent_used: string;
  route_info: string;
  processing_time: number;
  is_regulatory: boolean;
}

export interface Source {
  id: string;
  title: string;
  url: string;
  hostname: string;
  reason: string;
  quality: 'high' | 'medium' | 'low';
  isUserUpload?: boolean;
  filename?: string;
}

export interface SystemStatus {
  initialized: boolean;
  models: Record<string, any>;
}

export interface InitRequest {
  model_provider?: string;
  api_key_name?: string;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Check API health
   */
  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  }

  /**
   * Initialize the AI system
   */
  async initialize(request: InitRequest = {}): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/initialize`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model_provider: request.model_provider || 'groq_oss',
        api_key_name: request.api_key_name || 'GROQ_API_KEY',
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to initialize system');
    }

    return response.json();
  }

  /**
   * Get system status
   */
  async getStatus(): Promise<SystemStatus> {
    const response = await fetch(`${this.baseUrl}/api/status`);
    if (!response.ok) {
      throw new Error('Failed to get system status');
    }
    return response.json();
  }

  /**
   * Send a chat message
   */
  async sendMessage(message: ChatMessage): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(message),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to process message');
    }

    return response.json();
  }

  /**
   * Get available models information
   */
  async getModels(): Promise<any> {
    const response = await fetch(`${this.baseUrl}/api/models`);
    if (!response.ok) {
      throw new Error('Failed to get models information');
    }
    return response.json();
  }
}

export const apiService = new ApiService();
