import { useState } from "react";
import { API } from "../config/env";

export default function ImageSearch() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [images, setImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setImages([]);
  };

  const searchImages = async () => {
    if (!file) return;

    setLoading(true);
    setError("");

    try {
      const fd = new FormData();
      fd.append("image", file);

      const response = await fetch(`${API.search}/search_by_image`, {
        method: "POST",
        credentials: "include",
        body: fd, // FormData — do NOT set Content-Type, browser sets it with boundary
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

  return (
    <div className="min-h-screen bg-slate-100 px-6 py-6">
      <h1 className="text-3xl font-bold mb-6">🖼️ Search by Image</h1>

      <div className="flex items-center gap-4 mb-8">
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="border rounded px-3 py-2 bg-white"
        />
        <button
          onClick={searchImages}
          disabled={loading || !file}
          className="bg-purple-600 text-white px-5 py-2 rounded disabled:opacity-50"
        >
          {loading ? "Searching…" : "Search by Image"}
        </button>
      </div>

      {/* Preview of uploaded image */}
      {preview && (
        <div className="mb-8">
          <p className="text-sm text-gray-500 mb-2">Your image:</p>
          <img
            src={preview}
            alt="preview"
            className="w-48 h-48 object-cover rounded-xl shadow"
          />
        </div>
      )}

      {error && <p className="text-red-500 mb-4">{error}</p>}

      {!loading && images.length === 0 && !preview && (
        <p className="text-gray-500">Upload an image to find similar items.</p>
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