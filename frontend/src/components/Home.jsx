import { useEffect, useState } from "react";
import { API } from "../config/env";

export default function Home() {
  const [products, setProducts] = useState([]);
  const [allProducts, setAllProducts] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function fetchProducts() {
    try {
      const res = await fetch(`${API.products}/`, {
        credentials: "include",
      });

      if (!res.ok) {
        throw new Error("Failed to fetch products");
      }

      const data = await res.json();
      console.log("PRODUCT RESPONSE:", data);

      /**
       * ✅ YOUR BACKEND CONTRACT:
       * products are in `message`
       */
      const list = Array.isArray(data.message)
        ? data.message
        : [];

      setProducts(list);
      setAllProducts(list);
      setError("");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  // fetch once (remove polling for now)
  useEffect(() => {
    fetchProducts();
  }, []);

  // listen to navbar search
  useEffect(() => {
    const handler = (e) => setQuery(e.detail || "");
    window.addEventListener("product-search", handler);
    return () => window.removeEventListener("product-search", handler);
  }, []);

  // local search
  useEffect(() => {
    if (!query.trim()) {
      setProducts(allProducts);
    } else {
      setProducts(
        allProducts.filter((p) =>
          p.name?.toLowerCase().includes(query.toLowerCase())
        )
      );
    }
  }, [query, allProducts]);

  /* ---------------- Render ---------------- */

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-gray-600">
        Loading products…
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center text-red-500">
        {error}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 px-6 py-6">
      <h1 className="text-3xl font-bold text-center mb-8">
        🛍 Explore Products
      </h1>

      {products.length === 0 ? (
        <p className="text-center text-gray-500">
          No products found.
        </p>
      ) : (
        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {products.map((p) => (
            <div
              key={p.id ?? p._id}
              className="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden"
            >
              {/* Image */}
              <div className="h-48 bg-gray-100">
                <img
                  src={p.img_url}
                  alt={p.name}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Info */}
              <div className="p-4 flex flex-col gap-2">
                <h3 className="font-semibold text-lg text-gray-800">
                  {p.name}
                </h3>

                {p.status && (
                  <span
                    className={`text-xs font-semibold ${
                      p.status === "READY"
                        ? "text-green-600"
                        : p.status === "FAILED"
                        ? "text-red-600"
                        : "text-yellow-600"
                    }`}
                  >
                    Status: {p.status}
                  </span>
                )}

                {p.status === "READY" && p.description && (
                  <p className="text-sm text-gray-600">
                    {p.description}
                  </p>
                )}

                <span className="text-xl font-bold text-blue-600">
                  ₹{p.price}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
