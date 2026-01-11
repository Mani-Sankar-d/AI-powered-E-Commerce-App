import { useNavigate } from "react-router-dom";
import { useState } from "react";

const BACKEND_URL = "http://localhost:3000/api/users/logout";

export default function Navbar() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");

  const handleLogout = async () => {
    try {
      await fetch(
        BACKEND_URL,
        {
          method: "POST",
          credentials: "include",
        }
      );
    } catch (e) {
      // ignore
    } finally {
      navigate("/login", { replace: true });
    }
  };

  const handleSearch = () => {
    // emit search intent in a SAFE way
    window.dispatchEvent(
      new CustomEvent("product-search", { detail: search })
    );
  };

  return (
    <nav className="flex items-center justify-between px-6 py-3 bg-white shadow">
      {/* Logo */}
      <div
        className="text-xl font-bold text-blue-600 cursor-pointer"
        onClick={() => navigate("/home")}
      >
        AI-Commerce
      </div>

      {/* Search */}
      <div className="flex items-center gap-2">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search products..."
          className="px-3 py-2 border rounded w-64"
        />
        <button
          onClick={handleSearch}
          className="px-3 py-2 bg-blue-600 text-white rounded"
        >
          Search
        </button>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => navigate("/add-product")}
          className="px-4 py-2 bg-green-600 text-white rounded"
        >
          + Add Product
        </button>

        <button
          onClick={handleLogout}
          className="px-4 py-2 bg-red-500 text-white rounded"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
