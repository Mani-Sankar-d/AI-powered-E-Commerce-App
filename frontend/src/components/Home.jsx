import { useEffect, useState } from "react";
import { API } from "../config/env";

export default function Home() {
  const [products, setProducts] = useState([]);
  const [allProducts, setAllProducts] = useState([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // 🛒 CART STATE
  const [cart, setCart] = useState({});

  async function fetchProducts() {
    try {
      const res = await fetch(`${API.products}/`, {
        credentials: "include",
      });

      if (!res.ok) throw new Error("Failed to fetch products");

      const data = await res.json();
      const list = Array.isArray(data.message) ? data.message : [];

      setProducts(list);
      setAllProducts(list);
      setError("");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

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

  // ➕ ADD TO CART
  const addToCart = (pid) => {
    setCart((prev) => ({
      ...prev,
      [pid]: (prev[pid] || 0) + 1,
    }));
  };

  // ➖ REMOVE FROM CART
  const removeFromCart = (pid) => {
    setCart((prev) => {
      const copy = { ...prev };
      copy[pid]--;
      if (copy[pid] <= 0) delete copy[pid];
      return copy;
    });
  };

  // 💳 BUY
  const buyNow = async () => {
    try {
      const res = await fetch(`${API.products}/buy`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ items: cart }),
      });

      if (!res.ok) throw new Error("Purchase failed");

      setCart({});
      alert("Order placed successfully");
    } catch (e) {
      alert(e.message);
    }
  };

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
    <div className="min-h-screen bg-slate-100 px-6 py-6 pb-32">
      <h1 className="text-3xl font-bold text-center mb-8">
        🛍 Explore Products
      </h1>

      {products.length === 0 ? (
        <p className="text-center text-gray-500">No products found.</p>
      ) : (
        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {products.map((p) => (
            <div
              key={p.id}
              className="bg-white rounded-xl shadow hover:shadow-lg transition overflow-hidden"
            >
              <div className="h-48 bg-gray-100">
                <img
                  src={p.img_url}
                  alt={p.name}
                  className="w-full h-full object-cover"
                />
              </div>

              <div className="p-4 flex flex-col gap-2">
                <h3 className="font-semibold text-lg text-gray-800">
                  {p.name}
                </h3>

                {p.description && (
                  <p className="text-sm text-gray-600">{p.description}</p>
                )}

                <span className="text-xl font-bold text-blue-600">
                  ₹{p.price}
                </span>

                <button
                  onClick={() => addToCart(p.id)}
                  className="mt-2 bg-blue-600 text-white py-2 rounded"
                >
                  Add to Cart
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 🛒 CART PANEL */}
      {Object.keys(cart).length > 0 && (
        <div className="fixed bottom-6 right-6 bg-white shadow-xl p-4 rounded w-64">
          <p className="font-semibold mb-2">Cart</p>

          {Object.entries(cart).map(([pid, qty]) => (
            <div
              key={pid}
              className="flex justify-between items-center mb-1"
            >
              <span>
                #{pid} × {qty}
              </span>
              <div className="flex gap-1">
                <button
                  onClick={() => addToCart(pid)}
                  className="px-2 bg-green-500 text-white rounded"
                >
                  +
                </button>
                <button
                  onClick={() => removeFromCart(pid)}
                  className="px-2 bg-red-500 text-white rounded"
                >
                  −
                </button>
              </div>
            </div>
          ))}

          <button
            onClick={buyNow}
            className="mt-3 bg-green-600 text-white px-4 py-2 rounded w-full"
          >
            Buy
          </button>
        </div>
      )}
    </div>
  );
}
