import React, { useState } from 'react';

const MainPage = ({ user, onLogout }) => {
  const [total, setTotal] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [receiptData, setReceiptData] = useState(null);

  const handleGetReceipt = async () => {
    if (!total) return;
    
    setIsLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // Mock response
      setReceiptData({
        id: Math.random().toString(36).substring(2, 9),
        total: parseFloat(total),
        date: new Date().toLocaleString(),
        items: [
          { name: 'Product 1', price: (total * 0.4).toFixed(2) },
          { name: 'Product 2', price: (total * 0.6).toFixed(2) }
        ]
      });
    } catch (error) {
      console.error('Error fetching receipt:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 p-4">
      <div className="backdrop-blur-lg bg-white/30 p-8 rounded-2xl shadow-2xl w-full max-w-md border border-white/20 transition-all duration-300 hover:shadow-xl">
        <div className="flex justify-between items-center mb-6">
          <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-8 w-8 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
              />
            </svg>
          </div>
          <button 
            onClick={onLogout}
            className="text-white/80 hover:text-white text-sm font-medium transition-colors"
          >
            Sign Out
          </button>
        </div>

        <h2 className="text-3xl font-bold text-center text-white mb-2">
          Welcome {user?.companyName || 'User'}!
        </h2>
        <p className="text-center text-white/80 mb-8">Generate your receipt</p>

        <div className="space-y-6">
          <div>
            <label htmlFor="total" className="block text-sm font-medium text-white/80 mb-1">
              Total Amount
            </label>
            <div className="relative">
              <input
                type="number"
                id="total"
                value={total}
                onChange={(e) => setTotal(e.target.value)}
                placeholder="0.00"
                className="w-full px-4 py-3 bg-white/20 text-white placeholder-white/50 rounded-lg border border-white/30 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all"
              />
              <span className="absolute right-3 top-3 text-white/50">$</span>
            </div>
          </div>

          <button
            onClick={handleGetReceipt}
            disabled={!total || isLoading}
            className={`w-full py-3 px-4 rounded-lg font-semibold text-white transition-all duration-300 ${
              !total || isLoading
                ? "bg-blue-400 cursor-not-allowed"
                : "bg-white/20 hover:bg-white/30 hover:shadow-lg"
            } flex items-center justify-center`}
          >
            {isLoading ? (
              <>
                <svg
                  className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Generating...
              </>
            ) : (
              'Get Receipt'
            )}
          </button>

          {receiptData && (
            <div className="mt-6 p-4 bg-white/20 rounded-lg border border-white/30 backdrop-blur-sm animate-fadeIn">
              <h3 className="font-bold text-lg text-white mb-2">Receipt #{receiptData.id}</h3>
              <p className="text-white/80 mb-1">Date: {receiptData.date}</p>
              <div className="border-t border-white/30 my-2"></div>
              <div className="space-y-2 mb-3">
                {receiptData.items.map((item, index) => (
                  <div key={index} className="flex justify-between text-white">
                    <span>{item.name}</span>
                    <span>${item.price}</span>
                  </div>
                ))}
              </div>
              <div className="border-t border-white/30 my-2"></div>
              <div className="flex justify-between font-bold text-white">
                <span>Total:</span>
                <span>${receiptData.total.toFixed(2)}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MainPage;