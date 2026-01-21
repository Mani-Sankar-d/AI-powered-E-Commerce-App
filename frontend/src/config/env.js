// api.js

/**
 * Vite injects env variables at build time.
 * VITE_* variables are exposed to the client.
 */
export const API_BASE = import.meta.env.VITE_API_BASE_URL;

/**
 * Optional safety check (recommended)
 */
if (!API_BASE) {
  console.warn(
    "VITE_API_BASE_URL is not set, falling back to localhost"
  );
}

const BASE = API_BASE;

export const API = {
  users: `${BASE}/api/users`,
  products: `${BASE}/api/products`,
};
