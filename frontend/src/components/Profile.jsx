import { useEffect, useState } from "react";
import { API } from "../config/env";

export default function Profile() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function fetchProfile() {
    try {
      const res = await fetch(`${API.users}/get-profile`, {
        credentials: "include",
      });

      if (!res.ok) {
        throw new Error("Failed to fetch profile");
      }

      const json = await res.json();
      console.log("PROFILE RESPONSE:", json);

      /**
       * 🔑 Handle ALL ApiResponse shapes safely
       */
      const payload =
        json.data ??
        json.message?.data ??
        json.message;

      if (!payload || !payload.user) {
        throw new Error("Invalid profile payload");
      }

      setData(payload);
    } catch (e) {
      console.error(e);
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchProfile();
  }, []);

  /* ---------- RENDER FLOW (ORDER MATTERS) ---------- */

  if (loading) {
    return (
      <div className="min-h-screen flex justify-center items-center">
        Loading profile…
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex justify-center items-center text-red-500">
        {error}
      </div>
    );
  }

  if (!data || !data.user) {
    return (
      <div className="min-h-screen flex justify-center items-center text-gray-500">
        Profile data not available
      </div>
    );
  }

  const { user, orders } = data;

  return (
    <div className="min-h-screen bg-slate-100 px-6 py-6">
      <h1 className="text-3xl font-bold mb-6">👤 Profile</h1>

      {/* USER INFO */}
      <div className="bg-white p-4 rounded shadow mb-8">
        <p><b>Username:</b> {user.username}</p>
        <p><b>Email:</b> {user.email}</p>
      </div>

      {/* ORDERS */}
      <h2 className="text-2xl font-semibold mb-4">📦 Orders</h2>

      {orders.length === 0 ? (
        <p className="text-gray-500">No orders yet.</p>
      ) : (
        <div className="space-y-6">
          {orders.map((order) => (
            <div
              key={order.order_id}
              className="bg-white p-4 rounded shadow"
            >
              <div className="flex justify-between mb-2">
                <span><b>Order ID:</b> {order.order_id}</span>
                <span className="font-semibold text-blue-600">
                  ₹{order.total_amount}
                </span>
              </div>

              <p className="text-sm text-gray-600 mb-2">
                Status: {order.status}
              </p>

              <div className="border-t pt-2">
                {order.items.map((item, idx) => (
                  <div
                    key={idx}
                    className="flex justify-between text-sm py-1"
                  >
                    <span>
                      Product #{item.product_id} × {item.quantity}
                    </span>
                    <span>₹{item.price_snapshot}</span>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
