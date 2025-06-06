import { CloneRequest, CloneResponse, CloneResult } from '../types';

const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://your-api-domain.com' 
  : 'http://localhost:8000';

export const api = {
  async startClone(url: string): Promise<CloneResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/clone`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('Failed to start cloning:', error);
      throw new Error(`Failed to start cloning: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  },

  async getCloneResult(jobId: string): Promise<CloneResult> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/clone/${jobId}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          throw new Error('Clone job not found');
        }
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('Failed to get clone result:', error);
      throw new Error(`Failed to get clone result: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  },

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/clone/health`);
      return response.ok;
    } catch {
      return false;
    }
  }
};