// src/components/panels/DashboardPanel.jsx
import React from "react";

export default function DashboardPanel({
  user,
  total = "",
  isLoading = false,
  error = "",
  qrCode = null,
  setTotal = () => {},
  setQrCode = () => {},
  setError = () => {},
  handleGetReceipt = () => {},
  businessMetrics = { total_today: 0, total: 0 },   // ← default object
  recentActivity = [],                               // ← default array
}) {
  return (
    <>
      {/* Header (mobile) */}
      <div className="lg:hidden mb-4">
        <h1 className="text-2xl font-bold text-gray-800">
          {user?.companyName || "Business"}
        </h1>
        <p className="text-gray-600 text-sm">Receipt Management</p>
      </div>

      <div className="mb-6">
        <h2 className="text-xl sm:text-2xl font-bold text-gray-800">Dashboard</h2>
        <p className="text-gray-600 text-sm sm:text-base">
          Welcome back! Here’s your business overview.
        </p>
      </div>

      {/* Generator + QR */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 mb-6">
        {/* Generator card */}
        <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100 lg:col-span-2">
          <h3 className="text-lg font-semibold text-gray-700 mb-3">
            Generate New Receipt
          </h3>

          <form onSubmit={handleGetReceipt} className="space-y-4">
            <div>
              <label htmlFor="total" className="block text-sm font-medium text-gray-700 mb-1">
                Total Amount
              </label>
              <div className="relative">
                <input
                  id="total"
                  value={total}
                  onChange={(e) => {
                    setError("");
                    setTotal(e.target.value);
                  }}
                  inputMode="decimal"
                  step="0.01"
                  min="0"
                  placeholder="0.00"
                  className="w-full h-12 px-4 bg-gray-50 text-gray-900 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-base"
                />
                <span className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400">
                  $
                </span>
              </div>
            </div>

            <button
              type="submit"
              disabled={!total || isLoading}
              className={`w-full h-12 rounded-lg font-medium text-white transition-colors ${
                !total || isLoading ? "bg-blue-300" : "bg-blue-600 hover:bg-blue-700 active:bg-blue-800"
              }`}
            >
              {isLoading ? "Generating…" : "Generate Receipt"}
            </button>

            {error && (
              <div role="alert" className="p-3 bg-red-50 text-red-700 rounded-lg text-sm">
                {error}
              </div>
            )}
          </form>
        </div>

        {/* QR card */}
        <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center justify-center">
          {qrCode ? (
            <>
              <h3 className="text-lg font-semibold text-gray-700 mb-3">Receipt QR Code</h3>
              <img
                src={`data:image/png;base64,${qrCode}`}
                alt="Receipt QR Code"
                className="w-48 h-48 sm:w-56 sm:h-56 bg-white p-2 rounded-lg border border-gray-200 object-contain"
              />
              <button
                onClick={() => setQrCode(null)}
                className="mt-4 text-sm text-blue-600 hover:text-blue-800"
              >
                Generate New QR Code
              </button>
            </>
          ) : (
            <div className="text-center text-gray-400">
              <p className="mb-1">QR Code will appear here</p>
              <p className="text-sm">Generate a receipt to display the QR</p>
            </div>
          )}
        </div>
      </div>

      {/* Metrics & Activity */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
        <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-base sm:text-lg font-semibold text-gray-700 mb-2">Today’s Revenue</h3>
          <p className="text-2xl sm:text-3xl font-bold text-gray-900">
            ${Number(businessMetrics.total_today || 0).toFixed(2)}
          </p>
          <p className="text-gray-500 text-xs sm:text-sm mt-2">From 24 transactions</p>
        </div>

        <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-base sm:text-lg font-semibold text-gray-700 mb-2">Total Revenue</h3>
          <p className="text-2xl sm:text-3xl font-bold text-gray-900">
            ${Number(businessMetrics.total || 0).toFixed(2)}
          </p>
        </div>

        <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100 sm:col-span-2">
          <h3 className="text-base sm:text-lg font-bold text-gray-700 mb-3">Recent Activity</h3>
          {recentActivity?.length > 0 ? (
            <ul className="divide-y divide-gray-100 -my-2">
              {recentActivity.map((item, index) => (
                <li key={index} className="flex justify-between items-center py-2 text-gray-700">
                  <span className="font-medium">${Number(item?.total || 0).toFixed(2)}</span>
                  <span className="text-xs sm:text-sm text-gray-500">
                    {item?.transaction_date ? new Date(item.transaction_date).toLocaleString() : "--"}
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <div className="h-24 flex items-center justify-center text-gray-400">
              <p>No recent transactions.</p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
