// src/components/panels/ReceiptsPanel.jsx
import React, { useEffect, useState } from "react";
import api from "../../lib/api";

export default function ReceiptsPanel() {
  const [receipts, setReceipts] = useState([]);  // must stay an array
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchReceipts = async () => {
      try {
        setLoading(true);
        const res = await api.get("/api/v1/receipts/all");
        // console.log(res.data);  // <-- uncomment once to see the shape
        const d = res.data;

        // Normalize to an array no matter what the backend returns
        const list =
          Array.isArray(d) ? d :
          Array.isArray(d?.receipts) ? d.receipts :
          Array.isArray(d?.data) ? d.data :
          Array.isArray(d?.results) ? d.results :
          [];

        setReceipts(list);
      } catch (err) {
        const msg = err?.response?.data?.detail || err?.message || "Failed to load receipts";
        setError(msg);
      } finally {
        setLoading(false);
      }
    };

    fetchReceipts();
  }, []);

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border">
      <h3 className="text-lg font-semibold mb-4">All Receipts</h3>

      {loading && <p className="text-gray-500">Loading receipts…</p>}
      {error && <p className="text-red-500">{error}</p>}

      {!loading && !error && receipts.length === 0 && (
        <p className="text-gray-400">No receipts found.</p>
      )}

      <ul className="divide-y divide-gray-100">
        {receipts.map((r) => (
          <li key={r.receipt_id || r.id} className="flex justify-between items-center py-2">
            <span className="font-medium">
              ${Number(r.total || 0).toFixed(2)}
            </span>
            <span className="text-xs text-gray-500">
              {r.transaction_date ? new Date(r.transaction_date).toLocaleString() : "--"}
            </span>

            {/* Optional: open PDF */}
            {r.receipt_id && (
              <a
                href={`/api/v1/receipts/pdf/${r.receipt_id}`}
                className="ml-3 text-blue-600 text-xs"
              >
                PDF
              </a>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
