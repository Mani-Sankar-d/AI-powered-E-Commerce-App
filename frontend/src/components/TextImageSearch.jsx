import { useState } from "react";
import { API } from "../config/env";

export default function TextImageSearch() {
  const [query, setQuery] = useState("");
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const searchImages = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API.search}/search_by_text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(query),
      });

      if (response.status === 401) throw new Error("Unauthorized — please log in again");
      if (!response.ok) throw new Error(`Server error: ${response.status}`);

      const data = await response.json();
      setImages(Array.isArray(data) ? data : []);
    } catch (err) {
      console.error("Search error:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") searchImages();
  };

  return (
    <div className="min-h-screen bg-slate-100 px-6 py-6">
      <h1 className="text-3xl font-bold mb-6">🔍 Image Search</h1>

      <div className="flex gap-2 mb-8">
        <input
          type="text"
          placeholder="Search fashion..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          className="px-3 py-2 border rounded w-80 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />
        <button
          onClick={searchImages}
          disabled={loading}
          className="bg-purple-600 text-white px-5 py-2 rounded disabled:opacity-50"
        >
          {loading ? "Searching…" : "Search by Text"}
        </button>
      </div>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      {!loading && images.length === 0 && (
        <p className="text-gray-500">No results yet. Try searching something!</p>
      )}

      <div
        className="grid gap-4"
        style={{ gridTemplateColumns: "repeat(auto-fill, 200px)" }}
      >
        {images.map((img, index) => (
          <img
            key={index}
            src={`${import.meta.env.VITE_API_BASE_URL}${img}`}
            alt={`result-${index}`}
            className="w-48 h-48 object-cover rounded-xl shadow"
            onError={(e) => { e.target.style.display = "none"; }}
          />
        ))}
      </div>
    </div>
  );
}