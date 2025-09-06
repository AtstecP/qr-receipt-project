// src/components/Dashboard.jsx
import React, { useState, useEffect, useCallback } from "react";
import api from "../lib/api";
import {
  FiHome, FiFileText, FiDollarSign, FiPieChart, FiSettings, FiLogOut,
} from "react-icons/fi";

import DashboardPanel from "./panels/DashboardPanel";
import ReceiptsPanel from "./panels/ReceiptsPanel";
import AnalyticsPanel from "./panels/AnalyticsPanel";
import PaymentsPanel from "./panels/PaymentsPanel";
import SettingsPanel from "./panels/SettingsPanel";

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

export default function Dashboard({ user, onLogout }) {
  const [activeTab, setActiveTab] = useState("dashboard");

  // >>> the states you were passing to DashboardPanel
  const [total, setTotal] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [qrCode, setQrCode] = useState(null);
  const [error, setError] = useState("");
  const [businessMetrics, setBusinessMetrics] = useState({
    total: "0.00",
    total_today: "0.00",
  });
  const [recentActivity, setRecentActivity] = useState([]);

  // load stats
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
      /* silent */
    }
  }, []);

  useEffect(() => {
    fetchStats();
  }, [fetchStats, qrCode]);

  // create receipt
  const handleGetReceipt = useCallback(
    async (e) => {
      e?.preventDefault?.();
      if (!total) return setError("Please enter total amount");

      const amount = Number(total);
      if (Number.isNaN(amount) || amount <= 0) {
        return setError("Total must be a positive number");
      }

      setIsLoading(true);
      setError("");
      try {
        const { data } = await api.post("/api/v1/receipts/", { total: amount }, { timeout: 15000 });
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

  const renderActive = () => {
    switch (activeTab) {
      case "dashboard":
        return (
          <DashboardPanel
            user={user}
            total={total}
            isLoading={isLoading}
            error={error}
            qrCode={qrCode}
            setTotal={setTotal}
            setQrCode={setQrCode}
            setError={setError}
            handleGetReceipt={handleGetReceipt}
            businessMetrics={businessMetrics}
            recentActivity={recentActivity}
          />
        );
      case "receipts":
        return <ReceiptsPanel />;
      case "analytics":
        return <AnalyticsPanel />;
      case "payments":
        return <PaymentsPanel />;
      case "settings":
        return <SettingsPanel onLogout={onLogout} />;
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
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
          ].map((item) => {
            const Icon = item.icon; // ✅ not <i.icon />
            return (
              <button
                key={item.key}
                onClick={() => setActiveTab(item.key)}
                className={`flex items-center w-full p-3 rounded-lg transition-colors ${
                  activeTab === item.key
                    ? "bg-blue-50 text-blue-600"
                    : "text-gray-600 hover:bg-gray-100"
                }`}
              >
                <Icon className="mr-3 text-lg" />
                {item.label}
              </button>
            );
          })}
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
      <main className="flex-1 p-4 sm:p-6 lg:p-8 pb-24 lg:pb-8">{renderActive()}</main>

      {/* Bottom tabs (mobile) */}
      <nav className="lg:hidden fixed bottom-0 inset-x-0 border-t border-gray-200 bg-white/95 backdrop-blur">
        <div className="max-w-screen-md mx-auto flex">
          <TabButton active={activeTab === "dashboard"} onPress={() => setActiveTab("dashboard")} icon={FiHome} label="Home" />
          <TabButton active={activeTab === "receipts"}  onPress={() => setActiveTab("receipts")}  icon={FiFileText} label="Receipts" />
          <TabButton active={activeTab === "analytics"} onPress={() => setActiveTab("analytics")} icon={FiPieChart} label="Analytics" />
          <TabButton active={activeTab === "payments"}  onPress={() => setActiveTab("payments")}  icon={FiDollarSign} label="Payments" />
          <TabButton active={activeTab === "settings"}  onPress={() => setActiveTab("settings")}  icon={FiSettings} label="Settings" />
        </div>
      </nav>
    </div>
  );
}
