import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { API } from "../config/env";

export default function Navbar() {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");

  const logout = async () => {
    try {
      await fetch(`${API.users}/logout`, {
        method: "POST",
        credentials: "include",
      });
    } finally {
      navigate("/login", { replace: true });
    }
  };

  return (
    <nav className="sticky top-0 z-50 bg-white border-b shadow-sm px-6 py-3 flex items-center justify-between">
      <div
        className="text-xl font-bold text-blue-600 cursor-pointer"
        onClick={() => navigate("/home")}
      >
        AI-Commerce
      </div>

      <div className="flex gap-2">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search products…"
          className="px-3 py-2 border rounded w-64"
        />
        <button
          onClick={() =>
            window.dispatchEvent(
              new CustomEvent("product-search", { detail: search })
            )
          }
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Search
        </button>
      </div>

      <div className="flex gap-2">
        <button
        onClick={() => navigate("/profile")}
        className="bg-indigo-600 text-white px-4 py-2 rounded">
        Profile
        </button>
        <button
          onClick={() => navigate("/add-product")}
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          + Add
        </button>
        <button
          onClick={logout}
          className="bg-red-500 text-white px-4 py-2 rounded"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
