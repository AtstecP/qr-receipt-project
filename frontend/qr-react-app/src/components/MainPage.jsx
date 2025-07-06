import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  FiHome,
  FiFileText,
  FiDollarSign,
  FiPieChart,
  FiSettings,
  FiLogOut
} from 'react-icons/fi';

const Dashboard = ({ user, onLogout }) => {
  const [total, setTotal] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [qrCode, setQrCode] = useState(null);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [businessMetrics, setBusinessMetrics] = useState({
    thisMonthRevenue: '0',
    todayRevenue: '1,542',
  });
  const [recentActivity, setRecentActivity] = useState([]);

  const API_BASE_URL = "http://localhost:8000";

  const handleGetReceipt = async () => {
    if (!total) {
      setError('Please enter total amount');
      return;
    }

    setIsLoading(true);
    setError('');
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/v1/receipts/`,
        {
          total: Number(total),
        },
        { withCredentials: true }
      );

      setQrCode(response.data.pdf_endpoint);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to generate receipt');
    } finally {
      setIsLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API_BASE_URL}/api/v1/receipts/stats`, {
        withCredentials: true,
      });

      const data = res.data;

      setBusinessMetrics((prev) => ({
        ...prev,
        thisMonthRevenue: data.total?.toLocaleString() || "0",
      }));

      setRecentActivity(data.recent_receipts || []);
    } catch (error) {
      console.error("Failed to fetch stats:", error);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar */}
      <div className="w-64 bg-white shadow-md">
        <div className="p-4 border-b border-gray-200">
          <h1 className="text-xl font-bold text-gray-800">
            {user?.companyName || 'Business'}
          </h1>
          <p className="text-sm text-gray-500">Receipt Management</p>
        </div>

        <nav className="p-4 space-y-2">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`flex items-center w-full p-3 rounded-lg transition-colors ${
              activeTab === 'dashboard'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <FiHome className="mr-3" />
            Dashboard
          </button>
          <button
            onClick={() => setActiveTab('receipts')}
            className={`flex items-center w-full p-3 rounded-lg transition-colors ${
              activeTab === 'receipts'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <FiFileText className="mr-3" />
            Receipts
          </button>
          <button
            onClick={() => setActiveTab('analytics')}
            className={`flex items-center w-full p-3 rounded-lg transition-colors ${
              activeTab === 'analytics'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <FiPieChart className="mr-3" />
            Analytics
          </button>
          <button
            onClick={() => setActiveTab('payments')}
            className={`flex items-center w-full p-3 rounded-lg transition-colors ${
              activeTab === 'payments'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <FiDollarSign className="mr-3" />
            Payments
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            className={`flex items-center w-full p-3 rounded-lg transition-colors ${
              activeTab === 'settings'
                ? 'bg-blue-50 text-blue-600'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <FiSettings className="mr-3" />
            Settings
          </button>
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
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
          <p className="text-gray-600">
            Welcome back! Here's your business overview.
          </p>
        </div>

        {/* Receipt Generator & QR Code */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 lg:col-span-2">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">
              Generate New Receipt
            </h3>
            <div className="space-y-4">
              <div>
                <label
                  htmlFor="total"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Total Amount
                </label>
                <div className="relative">
                  <input
                    type="number"
                    id="total"
                    value={total}
                    onChange={(e) => setTotal(e.target.value)}
                    placeholder="0.00"
                    className="w-full px-4 py-2 bg-gray-50 text-gray-900 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <span className="absolute right-3 top-2.5 text-gray-400">
                    $
                  </span>
                </div>
              </div>

              <button
                onClick={handleGetReceipt}
                disabled={!total || isLoading}
                className={`w-full py-2 px-4 rounded-lg font-medium text-white transition-colors ${
                  !total || isLoading
                    ? 'bg-blue-300 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700'
                }`}
              >
                {isLoading ? 'Generating...' : 'Generate Receipt'}
              </button>

              {error && (
                <div className="p-3 bg-red-50 text-red-700 rounded-lg text-sm">
                  {error}
                </div>
              )}
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col items-center justify-center">
            {qrCode ? (
              <>
                <h3 className="text-lg font-semibold text-gray-700 mb-4">
                  Receipt QR Code
                </h3>
                <img
                  src={`data:image/png;base64,${qrCode}`}
                  alt="Receipt QR Code"
                  className="w-48 h-48 bg-white p-2 rounded-lg border border-gray-200"
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
                <p className="mb-2">QR Code will appear here</p>
                <p className="text-sm">
                  Generate a receipt to display the QR code
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Business Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6">
          {/* This Month Revenue */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">
              This Month Revenue
            </h3>
            <p className="text-3xl font-bold text-gray-900">
              ${businessMetrics.thisMonthRevenue}
            </p>
            <p className="text-green-500 text-sm mt-2">+12% from last month</p>
          </div>

          {/* Today's Revenue (still static for now) */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">
              Today's Revenue
            </h3>
            <p className="text-3xl font-bold text-gray-900">
              ${businessMetrics.todayRevenue}
            </p>
            <p className="text-gray-500 text-sm mt-2">
              From 24 transactions
            </p>
          </div>

          {/* Recent Activity */}
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 md:col-span-2">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">
              Recent Activity
            </h3>
            {recentActivity.length > 0 ? (
              <ul className="space-y-2">
                {recentActivity.map((item, index) => (
                  <li
                    key={index}
                    className="flex justify-between text-gray-700 border-b border-gray-100 pb-2"
                  >
                    <span>${item.total.toFixed(2)}</span>
                    <span className="text-sm text-gray-500">
                      {new Date(item.transaction_date).toLocaleString()}
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="h-32 flex items-center justify-center text-gray-400">
                <p>No recent transactions.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
