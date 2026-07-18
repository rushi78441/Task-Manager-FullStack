import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

const API_URL = "http://127.0.0.1:8000"

const RegisterPage = ({ setUserEmail }) => {
    const navigate = useNavigate();

    // Loading and error states
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");
    const [successMsg, setSuccessMsg] = useState("");

    // Registration fields state
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("")
        setSuccessMsg("")

        // simple frontend password matching test
        if (password != confirmPassword) {
            setError("Password Do not match!")
            return
        }

        // set loading if password matched
        setIsLoading(true)

        // Simulate Register API Request / Registration Logic
        try {
            // getting response
            const response = await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: { "Content-Type": 'application/json' },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            })

            if (response.status == 400) {
                setError("Account already exists")
                console.log("Account already exits")
                return
            }

            // Micro delay for resolve first register api reuest 
            await new Promise((resolve) => setTimeout(resolve, 100));

            // if response generated , means backend registered user successfully, we will directly move this user in dashboard page
            if (response.ok) {
                setSuccessMsg("Account Created Successfully! Logging you in")

                // now login user 
                const loginResponse = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                })

                // Check if login resposne is not ok(get some error)
                if (!loginResponse.ok) {
                    setError("Account Created, but Failed to log in.")
                    console.error("Failed to login User", error)
                    return
                }

                // if logic resposne ok 
                if (loginResponse.ok) {
                    // Now set User Email set in APP parent component , so that child dashboard page will able to render that state
                    // now get the login reponse and token
                    const tokenData = await loginResponse.json()
                    localStorage.setItem('user_token', tokenData.access_token)

                    // Now set User Email set in APP parent component , so that child dashboard page will able to render that state
                    setUserEmail(email)
                    localStorage.setItem('saved_user', email)
                    navigate('/dashboard')
                    console.log("Account Registered and Logged in Successfully!")
                    return
                }
            }
        }
        catch (err) {
            console.error("Network Error, Can not reach the server", err)
        }
        finally {
            setIsLoading(false)
        }
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-linear-to-br from-slate-50 to-gray-100 p-4 box-border">
            <div className="w-full max-w-md bg-white rounded-2xl p-8 shadow-xl border border-gray-100">

                {/* Header / Intro */}
                <div className="text-center mb-6">
                    <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">
                        Create Account
                    </h2>
                    <p className="text-sm text-gray-500 mt-2">
                        Get started with Task-Master today
                    </p>
                </div>

                {/* Error Message Box */}
                {error && (
                    <div className="mb-4 p-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg">
                        {error}
                    </div>
                )}

                {/* Success Message Box */}
                {successMsg && (
                    <div className="mb-4 p-3 text-sm text-green-600 bg-green-50 border border-green-200 rounded-lg">
                        {successMsg}
                    </div>
                )}

                {/* Form */}
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    {/* Email Field */}
                    <div className="flex flex-col gap-1.5">
                        <label htmlFor="email" className="text-sm font-semibold text-gray-700">
                            Email Address
                        </label>
                        <input
                            id="email"
                            type="email"
                            required
                            disabled={isLoading}
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="admin@example.com"
                            className="w-full bg-white border border-gray-300 rounded-lg py-2.5 px-3.5 text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 disabled:opacity-50"
                        />
                    </div>

                    {/* Password Field */}
                    <div className="flex flex-col gap-1.5">
                        <label htmlFor="password" className="text-sm font-semibold text-gray-700">
                            Password
                        </label>
                        <input
                            id="password"
                            type="password"
                            required
                            disabled={isLoading}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                            className="w-full bg-white border border-gray-300 rounded-lg py-2.5 px-3.5 text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200 disabled:opacity-50"
                        />
                    </div>

                    {/* Confirm Password Field */}
                    <div className="flex flex-col gap-1.5">
                        <label htmlFor="confirmPassword" className="text-sm font-semibold text-gray-700">
                            Confirm Password
                        </label>
                        <input
                            id="confirmPassword"
                            type="password"
                            required
                            disabled={isLoading}
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="••••••••"
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
                                <svg className="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                                </svg>
                                Creating account...
                            </span>
                        ) : (
                            "Sign up"
                        )}
                    </button>

                </form>

                {/* Footer Navigation link */}
                <div className="text-center mt-6">
                    <p className="text-sm text-gray-600">
                        Already have an account?{" "}
                        <Link to="/" className="font-semibold text-indigo-600 hover:text-indigo-500 underline decoration-2 underline-offset-4">
                            Sign in
                        </Link>
                    </p>
                </div>

            </div>
        </div>
    );
};

export default RegisterPage;