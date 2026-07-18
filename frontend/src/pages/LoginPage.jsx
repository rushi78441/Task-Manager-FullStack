import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";

const API_URL = "http://127.0.0.1:8000"

const LoginPage = ({ setUserEmail }) => {
  const navigate = useNavigate();

  // Loading sign in states
  const [isLoading, setIsLoading] = useState(false);

  // Credentials state
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  // Error handling state (Nice to have for functional UIs!)
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("")
    setIsLoading(true)

    // simulate Login API Request / Login Logic
    try {
      await new Promise((resolve) => setTimeout(resolve, 1200))

      // now hit Login api and get response
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'Application/Json' },
        body: JSON.stringify({
          email: email,
          password: password
        })
      })

      const token = await response.json()

      if (!token) {
        console.log("Token is not generated")
        return
      }


      // if login successfully
      if (response.ok) {
        setIsLoading(false)

        // set token in local storage
        localStorage.setItem('user_token', token.access_token)

        setUserEmail(email)
        localStorage.setItem('saved_user', email)

        navigate("/dashboard")
        console.log("Logged in Successfully")
        return
      }

      if (response.status == 401) {
        console.log("Invalid credentials")
        setError("Invalid credentials")
      }
    } catch (err) {
      console.error("Network Erro", err)
    } finally {
      setIsLoading(false)
    }

  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-linear-to-br from-slate-50 to-gray-100 p-4 box-border">
      <div className="w-full max-w-md bg-white rounded-2xl p-8 shadow-xl border border-gray-100">

        {/* Header / Intro */}
        <div className="text-center mb-8">
          <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">
            Welcome Back
          </h2>
          <p className="text-sm text-gray-500 mt-2">
            Please sign in to access your dashboard
          </p>
        </div>

        {/* Error Message Box */}
        {error && (
          <div className="mb-4 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-5">

          {/* Email Field */}
          <div className="flex flex-col gap-1.5">
            <label htmlFor="email" className="text-sm font-semibold text-gray-700">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              name="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)} // Makes the input typable
              placeholder="admin@example.com"
              required
              disabled={isLoading}
              className="w-full bg-white border border-gray-300 rounded-lg py-2.5 px-3.5 text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 disabled:opacity-50"
            />
          </div>

          {/* Password Field */}
          <div className="flex flex-col gap-1.5">
            <div className="flex justify-between items-center">
              <label htmlFor="password" className="text-sm font-semibold text-gray-700">
                Password
              </label>
            </div>
            <input
              id="password"
              type="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)} // Makes the input typable
              placeholder="••••••••"
              required
              disabled={isLoading}
              className="w-full bg-white border border-gray-300 rounded-lg py-2.5 px-3.5 text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 disabled:opacity-50"
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full mt-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-4 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 active:scale-[0.98] disabled:bg-indigo-400 disabled:cursor-not-allowed"
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-2">
                {/* Subtle spinning loader utility */}
                <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Signing in...
              </span>
            ) : (
              "Sign in"
            )}
          </button>

        </form>
        {/* Footer Navigation link */}
        <div className="text-center mt-6">
          <p className="text-sm text-gray-600">
            Don't have an account?{" "}
            <Link to="/register" className="font-semibold text-indigo-600 hover:text-indigo-500 underline decoration-2 underline-offset-4">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;