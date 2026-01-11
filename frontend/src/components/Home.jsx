import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const BACKEND_URL = "http://localhost:3000/api/";

export default function Home() {
  const navigate = useNavigate();

  const [products, setProducts] = useState([]);
  const [allProducts, setAllProducts] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  /* --------------------------------
     Fetch products (reusable)
  -------------------------------- */
  async function fetchProducts() {
    try {
      const res = await fetch(BACKEND_URL, {
        credentials: "include",
      });

      if (!res.ok) {
        throw new Error("Failed to fetch products");
      }

      const data = await res.json();
      setProducts(data.data || []);
      setAllProducts(data.data || []);
      setError("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  /* --------------------------------
     Initial fetch
  -------------------------------- */
  useEffect(() => {
    fetchProducts();
  }, []);

  /* --------------------------------
     Polling every 5 seconds
  -------------------------------- */
  useEffect(() => {
    const interval = setInterval(() => {
      fetchProducts();
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  /* --------------------------------
     Listen to navbar search events
  -------------------------------- */
  useEffect(() => {
    const handler = (e) => {
      setQuery(e.detail || "");
    };

    window.addEventListener("product-search", handler);
    return () => window.removeEventListener("product-search", handler);
  }, []);

  /* --------------------------------
     Local name-based search
  -------------------------------- */
  useEffect(() => {
    if (!query.trim()) {
      setProducts(allProducts);
      return;
    }

    const filtered = allProducts.filter((product) =>
      product.name?.toLowerCase().includes(query.toLowerCase())
    );

    setProducts(filtered);
  }, [query, allProducts]);

  /* --------------------------------
     Render states
  -------------------------------- */
  if (loading) {
    return (
      <div className="flex justify-center items-center h-[60vh]">
        <p className="text-lg text-gray-600">Loading products...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center h-[60vh]">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  /* --------------------------------
     UI
  -------------------------------- */
  return (
    <div className="min-h-screen bg-slate-100 px-6 py-6">
      <h1 className="text-3xl font-bold text-center mb-8">
        🛍️ Explore Products
      </h1>

      {products.length === 0 ? (
        <p className="text-center text-gray-500">No products found.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {products.map((product) => (
            <div
              key={product._id}
              className="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden"
            >
              {/* Image */}
              <div className="h-48 bg-gray-100">
                <img
                  src={product.img_url}
                  alt={product.name}
                  className="w-full h-full object-cover"
                />
              </div>

              {/* Info */}
              <div className="p-4 flex flex-col gap-2">
                <h3 className="text-lg font-semibold text-gray-800">
                  {product.name}
                </h3>

                {/* Status */}
                <span className="text-xs font-semibold">
                  Status:{" "}
                  <span
                    className={
                      product.status === "READY"
                        ? "text-green-600"
                        : product.status === "FAILED"
                        ? "text-red-600"
                        : "text-yellow-600"
                    }
                  >
                    {product.status}
                  </span>
                </span>

                {/* Caption only when READY */}
                {product.status === "READY" && (
                  <p className="text-sm text-gray-600">
                    {product.description}
                  </p>
                )}

                <span className="text-xl font-bold text-blue-600">
                  ₹{product.price}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
