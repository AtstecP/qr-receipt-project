// Dashboard.jsx (mobile-first, Tailwind)
// - Uses preconfigured axios client `api`
// - Bottom tab bar on mobile, sidebar only on >=lg

import React, { useState, useEffect, useCallback } from "react";
// If you DIDN'T set Vite path alias "@", use: import api from "../lib/api";
import api from "../lib/api";
import {
  FiHome,
  FiFileText,
  FiDollarSign,
  FiPieChart,
  FiSettings,
  FiLogOut,
} from "react-icons/fi";

const TabButton = ({ active, onPress, icon: Icon, label }) => (
  <button
    onClick={onPress}
    className={`flex flex-col items-center justify-center gap-1 flex-1 py-2.5 ${
      active ? "text-blue-600" : "text-gray-500"
    }`}
    aria-pressed={active}
  >
    <Icon className="text-xl" />
    <span className="text-xs">{label}</span>
  </button>
);

const Dashboard = ({ user, onLogout }) => {
  const [total, setTotal] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [qrCode, setQrCode] = useState(null);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("dashboard");
  const [businessMetrics, setBusinessMetrics] = useState({
    total: "0.00",
    total_today: "0.00",
  });
  const [recentActivity, setRecentActivity] = useState([]);

  const fetchStats = useCallback(async () => {
    try {
      const res = await api.get("/api/v1/receipts/stats", { timeout: 10000 });
      const data = res.data || {};
      setBusinessMetrics({
        total: (data.total ?? data.receipts_total ?? 0).toString(),
        total_today: (data.total_today ?? 0).toString(),
      });
      setRecentActivity(data.recent_receipts ?? []);
    } catch {
      // quiet on mobile
    }
  }, []);

  useEffect(() => {
    fetchStats();
  }, [fetchStats, qrCode]);

  const handleGetReceipt = useCallback(
    async (e) => {
      e?.preventDefault?.();
      if (!total) {
        setError("Please enter total amount");
        return;
      }
      const amount = Number(total);
      if (Number.isNaN(amount) || amount <= 0) {
        setError("Total must be a positive number");
        return;
      }

      setIsLoading(true);
      setError("");
      try {
        const { data } = await api.post(
          "/api/v1/receipts/",
          { total: amount },
          { timeout: 15000 }
        );
        // backend returns { pdf_endpoint: <base64 png> }
        setQrCode(data?.pdf_endpoint ?? null);
        await fetchStats();
      } catch (err) {
        const msg =
          err?.response?.data?.detail ||
          err?.response?.data?.message ||
          err?.message ||
          "Failed to generate receipt";
        setError(msg);
      } finally {
        setIsLoading(false);
      }
    },
    [total, fetchStats]
  );

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar (desktop/tablet only) */}
      <aside className="hidden lg:flex lg:w-64 bg-white shadow-md flex-col">
        <div className="p-4 border-b border-gray-200">
          <h1 className="text-xl font-bold text-gray-800 truncate">
            {user?.companyName || "Business"}
          </h1>
          <p className="text-sm text-gray-500">Receipt Management</p>
        </div>

        <nav className="p-4 space-y-2">
          {[
            { key: "dashboard", label: "Dashboard", icon: FiHome },
            { key: "receipts", label: "Receipts", icon: FiFileText },
            { key: "analytics", label: "Analytics", icon: FiPieChart },
            { key: "payments", label: "Payments", icon: FiDollarSign },
            { key: "settings", label: "Settings", icon: FiSettings },
          ].map((i) => (
            <button
              key={i.key}
              onClick={() => setActiveTab(i.key)}
              className={`flex items-center w-full p-3 rounded-lg transition-colors ${
                activeTab === i.key
                  ? "bg-blue-50 text-blue-600"
                  : "text-gray-600 hover:bg-gray-100"
              }`}
            >
              <i.icon className="mr-3 text-lg" />
              {i.label}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-gray-200 mt-auto">
          <button
            onClick={onLogout}
            className="flex items-center w-full p-3 rounded-lg text-gray-600 hover:bg-gray-100 transition-colors"
          >
            <FiLogOut className="mr-3" />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 p-4 sm:p-6 lg:p-8 pb-24 lg:pb-8">
        {/* Header (mobile) */}
        <div className="lg:hidden mb-4">
          <h1 className="text-2xl font-bold text-gray-800">
            {user?.companyName || "Business"}
          </h1>
          <p className="text-gray-600 text-sm">Receipt Management</p>
        </div>

        {/* Page Title */}
        <div className="mb-6">
          <h2 className="text-xl sm:text-2xl font-bold text-gray-800">
            Dashboard
          </h2>
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
                <label
                  htmlFor="total"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
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
                  !total || isLoading
                    ? "bg-blue-300"
                    : "bg-blue-600 hover:bg-blue-700 active:bg-blue-800"
                }`}
              >
                {isLoading ? "Generating…" : "Generate Receipt"}
              </button>

              {error && (
                <div
                  role="alert"
                  className="p-3 bg-red-50 text-red-700 rounded-lg text-sm"
                >
                  {error}
                </div>
              )}
            </form>
          </div>

          {/* QR card */}
          <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center justify-center">
            {qrCode ? (
              <>
                <h3 className="text-lg font-semibold text-gray-700 mb-3">
                  Receipt QR Code
                </h3>
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
            <h3 className="text-base sm:text-lg font-semibold text-gray-700 mb-2">
              Today’s Revenue
            </h3>
            <p className="text-2xl sm:text-3xl font-bold text-gray-900">
              ${Number(businessMetrics.total_today || 0).toFixed(2)}
            </p>
            <p className="text-gray-500 text-xs sm:text-sm mt-2">
              From 24 transactions
            </p>
          </div>

          <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-base sm:text-lg font-semibold text-gray-700 mb-2">
              Total Revenue
            </h3>
            <p className="text-2xl sm:text-3xl font-bold text-gray-900">
              ${Number(businessMetrics.total || 0).toFixed(2)}
            </p>
          </div>

          <div className="bg-white p-4 sm:p-6 rounded-xl shadow-sm border border-gray-100 sm:col-span-2">
            <h3 className="text-base sm:text-lg font-bold text-gray-700 mb-3">
              Recent Activity
            </h3>
            {recentActivity?.length > 0 ? (
              <ul className="divide-y divide-gray-100 -my-2">
                {recentActivity.map((item, index) => (
                  <li
                    key={index}
                    className="flex justify-between items-center py-2 text-gray-700"
                  >
                    <span className="font-medium">
                      ${Number(item?.total || 0).toFixed(2)}
                    </span>
                    <span className="text-xs sm:text-sm text-gray-500">
                      {item?.transaction_date
                        ? new Date(item.transaction_date).toLocaleString()
                        : "--"}
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
      </main>

      {/* Bottom tab bar (mobile only) */}
      <nav className="lg:hidden fixed bottom-0 inset-x-0 border-t border-gray-200 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/70">
        <div className="max-w-screen-md mx-auto flex">
          <TabButton
            active={activeTab === "dashboard"}
            onPress={() => setActiveTab("dashboard")}
            icon={FiHome}
            label="Home"
          />
          <TabButton
            active={activeTab === "receipts"}
            onPress={() => setActiveTab("receipts")}
            icon={FiFileText}
            label="Receipts"
          />
          <TabButton
            active={activeTab === "analytics"}
            onPress={() => setActiveTab("analytics")}
            icon={FiPieChart}
            label="Analytics"
          />
          <TabButton
            active={activeTab === "payments"}
            onPress={() => setActiveTab("payments")}
            icon={FiDollarSign}
            label="Payments"
          />
          <TabButton
            active={activeTab === "settings"}
            onPress={() => setActiveTab("settings")}
            icon={FiSettings}
            label="Settings"
          />
        </div>
      </nav>
    </div>
  );
};

export default Dashboard;
