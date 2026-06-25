type FetchOptions = RequestInit & {
  params?: Record<string, string>;
};

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1") {
    this.baseUrl = baseUrl;
  }

  private async request<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
    const { params, ...init } = options;
    
    let url = `${this.baseUrl}${endpoint}`;
    if (params) {
      const searchParams = new URLSearchParams(params);
      url += `?${searchParams.toString()}`;
    }

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(init.headers as Record<string, string>),
    };

    // Add auth token if available in localStorage (client-side only)
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("servai_token");
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
    }

    const response = await fetch(url, {
      ...init,
      headers,
    });

    if (response.status === 401) {
      // In a real app, handle token expiration/refresh
      if (typeof window !== "undefined") {
        localStorage.removeItem("servai_token");
        // Could redirect to login here
      }
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || response.statusText || "API Request Failed");
    }

    return response.json() as Promise<T>;
  }

  get<T>(endpoint: string, options: FetchOptions = {}) {
    return this.request<T>(endpoint, { ...options, method: "GET" });
  }

  post<T>(endpoint: string, data?: unknown, options: FetchOptions = {}) {
    return this.request<T>(endpoint, {
      ...options,
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  patch<T>(endpoint: string, data?: unknown, options: FetchOptions = {}) {
    return this.request<T>(endpoint, {
      ...options,
      method: "PATCH",
      body: JSON.stringify(data),
    });
  }

  delete<T>(endpoint: string, options: FetchOptions = {}) {
    return this.request<T>(endpoint, { ...options, method: "DELETE" });
  }
}

export const api = new ApiClient();
