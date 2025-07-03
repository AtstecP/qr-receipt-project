import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { FiLogIn, FiUserPlus, FiBriefcase, FiMail, FiLock } from "react-icons/fi";

const LoginRegister = ({ onLoginSuccess }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const API_BASE_URL = "http://127.0.0.1:8000";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      if (isLogin) {
        const response = await axios.post(`${API_BASE_URL}/api/v1/login`, {
          email,
          password,
        });

        // localStorage.setItem("jwtToken", response.data.token);
       document.cookie = `token=${response.data.token}; path=/; secure; samesite=strict`;

        localStorage.setItem("userEmail", email);
        // axios.defaults.headers.common["Authorization"] = `Bearer ${response.data.token}`;
        onLoginSuccess(email);
        navigate("/");
      } else {
        await axios.post(`${API_BASE_URL}/api/v1/register`, {
          company_name: companyName,
          email,
          password,
        });

        const response = await axios.post(`${API_BASE_URL}/api/v1/login`, {
          email,
          password,
        });
        //localStorage.setItem("jwtToken", loginResponse.data.token);
        localStorage.setItem("userEmail", email);
        // axios.defaults.headers.common["Authorization"] = `Bearer ${loginResponse.data.token}`;
        document.cookie = `token=${response.data.token}; path=/; secure; samesite=strict`;
        onLoginSuccess(email);
        navigate("/");
      }
    } catch (err) {
      let errorMessage = "Something went wrong";
      if (err.response) {
        if (err.response.status === 403) {
          errorMessage = "Invalid email or password";
        } else {
          errorMessage = err.response.data.detail || err.response.statusText;
        }
      } else if (err.request) {
        errorMessage = "No response from server";
      }
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="w-full max-w-md bg-white rounded-xl shadow-md overflow-hidden">
        {/* Header Section */}
        <div className="bg-blue-600 p-6 text-center">
          <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center mx-auto mb-4 backdrop-blur-sm">
            {isLogin ? (
              <FiLogIn className="h-8 w-8 text-white" />
            ) : (
              <FiUserPlus className="h-8 w-8 text-white" />
            )}
          </div>
          <h2 className="text-2xl font-bold text-white">
            {isLogin ? "Welcome Back" : "Create Account"}
          </h2>
          <p className="text-blue-100 mt-1">
            {isLogin ? "Sign in to your account" : "Get started with our platform"}
          </p>
        </div>

        {/* Form Section */}
        <div className="p-6">
          {error && (
            <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div className="space-y-2">
                <label htmlFor="company" className="block text-sm font-medium text-gray-700">
                  Company Name
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <FiBriefcase className="h-5 w-5 text-gray-400" />
                  </div>
                  <input
                    type="text"
                    id="company"
                    placeholder="Your Company LLC"
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    className="pl-10 w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    required={!isLogin}
                  />
                </div>
              </div>
            )}

            <div className="space-y-2">
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiMail className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="email"
                  id="email"
                  placeholder="your@email.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-10 w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>
            </div>

            <div className="space-y-2">
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <FiLock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  type="password"
                  id="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-10 w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className={`w-full py-2.5 px-4 rounded-lg font-medium text-white transition-colors ${isLoading
                  ? "bg-blue-400 cursor-not-allowed"
                  : "bg-blue-600 hover:bg-blue-700"
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
                  Processing...
                </>
              ) : isLogin ? (
                "Sign In"
              ) : (
                "Create Account"
              )}
            </button>
          </form>

          <div className="mt-6 text-center">
            <button
              type="button"
              onClick={() => setIsLogin(!isLogin)}
              className="text-sm text-blue-600 hover:text-blue-800 font-medium"
            >
              {isLogin ? (
                <>Don't have an account? <span className="font-semibold">Sign up</span></>
              ) : (
                <>Already have an account? <span className="font-semibold">Sign in</span></>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginRegister;