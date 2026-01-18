const DEFAULT_API = "http://localhost:8000";

/**
 * Vite injects env at build time.
 * On Vercel/Netlify, you set this once in dashboard.
 */
export const API_BASE =
  import.meta.env.VITE_API_BASE_URL || DEFAULT_API;

export const API = {
  users: `${API_BASE}/api/users`,
  products: `${API_BASE}/api/products`,
};
