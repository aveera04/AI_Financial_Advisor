/**
 * API Service for Financial Advisor Backend
 * Handles all communication with the FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface Source {
  id: string;
  title: string;
  url: string;
  hostname: string;
  reason: string;
  quality: 'high' | 'medium' | 'low';
}

export interface ChatRequest {
  message: string;
  session_id?: string;
  tone?: 'concise' | 'detailed';
}

export interface ChatResponse {
  content: string;
  sources: Source[];
  model: string;
  is_regulatory: boolean;
  timestamp: string;
  session_id: string;
}

export interface ModelInfo {
  orchestrator: string;
  ipo_agent: string;
  stock_agent: string;
  tools: string[];
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  model_info: Record<string, string>;
}

class ApiService {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Send a chat message to the financial advisor
   */
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  /**
   * Get model information
   */
  async getModelInfo(): Promise<ModelInfo> {
    const response = await fetch(`${this.baseUrl}/models`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  /**
   * Check if the API is available
   */
  async isAvailable(): Promise<boolean> {
    try {
      await this.healthCheck();
      return true;
    } catch {
      return false;
    }
  }
}

// Export a singleton instance
export const apiService = new ApiService();

export default apiService;
