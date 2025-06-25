import { Cat, CatCreate, CatUpdate, CatListResponse } from '@/types/cat';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new ApiError(response.status, errorData.detail || 'Request failed');
  }
  return response.json();
}

export const catApi = {
  // Get all cats
  async getCats(): Promise<CatListResponse> {
    const response = await fetch(`${API_BASE_URL}/api/v1/cats/`);
    return handleResponse<CatListResponse>(response);
  },

  // Get single cat
  async getCat(id: number): Promise<Cat> {
    const response = await fetch(`${API_BASE_URL}/api/v1/cats/${id}`);
    return handleResponse<Cat>(response);
  },

  // Create new cat
  async createCat(catData: CatCreate): Promise<Cat> {
    const response = await fetch(`${API_BASE_URL}/api/v1/cats/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(catData),
    });
    return handleResponse<Cat>(response);
  },

  // Update cat salary
  async updateCat(id: number, catData: CatUpdate): Promise<Cat> {
    const response = await fetch(`${API_BASE_URL}/api/v1/cats/${id}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(catData),
    });
    return handleResponse<Cat>(response);
  },

  // Delete cat
  async deleteCat(id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/v1/cats/${id}`, {
      method: 'DELETE',
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      throw new ApiError(response.status, errorData.detail || 'Delete failed');
    }
  },
};

export { ApiError };
