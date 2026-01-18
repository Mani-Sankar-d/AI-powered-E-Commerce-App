import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { API } from "../config/env";

export default function AddProduct() {
  const nav = useNavigate();
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [image, setImage] = useState(null);
  const [desc, setDesc] = useState("");
  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState("");

  const submit = async (e) => {
    e.preventDefault();
    if (!name || !price || !image) {
      setErr("Name, price and image required");
      return;
    }

    try {
      setLoading(true);
      const fd = new FormData();
      fd.append("name", name);
      fd.append("price", price);
      fd.append("image", image);
      if (desc) fd.append("description", desc);

      const res = await fetch(`${API.products}/new-product`, {
        method: "POST",
        credentials: "include",
        body: fd,
      });

      if (!res.ok) throw new Error("Upload failed");
      nav("/home");
    } catch (e) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex items-center justify-center">
      <form
        onSubmit={submit}
        className="bg-white p-8 rounded-xl shadow w-full max-w-md space-y-4"
      >
        <h2 className="text-2xl font-bold text-center">Add Product</h2>

        <input
          placeholder="Product name"
          className="w-full border p-2 rounded"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <input
          type="number"
          placeholder="Price"
          className="w-full border p-2 rounded"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
        />

        <input
          type="file"
          accept="image/*"
          onChange={(e) => setImage(e.target.files[0])}
        />

        <textarea
          placeholder="Description (optional)"
          className="w-full border p-2 rounded"
          value={desc}
          onChange={(e) => setDesc(e.target.value)}
        />

        {err && <p className="text-red-500 text-sm">{err}</p>}

        <button
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 rounded"
        >
          {loading ? "Uploading…" : "Add Product"}
        </button>
      </form>
    </div>
  );
}
