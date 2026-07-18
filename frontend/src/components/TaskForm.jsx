import React, { useState } from 'react'

const API_URL = "http://127.0.0.1:8000"

const TaskForm = ({ onAddedTask }) => {

  // form input states handling
  const [TaskTitle, setTaskTitle] = React.useState("")
  const [Descryption, setDescryption] = React.useState("")
  const [status, setStatus] = React.useState("active")
  const [error, setError] = React.useState("")
  const [successMsg, setSuccessMdg] = React.useState("")


  // Handle Submit
  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // grab the token to authorize that the user is valid and authorized to creat task
    const token = localStorage.getItem('user_token')

    if (!token) {
      setError("You are not Authorized to create task")
      console.error("No Token found , please log in again")
    }

    // Simulate tasks creation API Request / Task creation Logic
    try {
      await new Promise((resolve) => setTimeout(resolve, 1000))

      // Hitting Tasks creation api
      const response = await fetch(`${API_URL}/tasks`, {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `bearer ${token}`
        },
        body: JSON.stringify({
          task_title: TaskTitle,
          descryption: Descryption || "",
          status : status || "active"
        })
      })

      // check response generated successfully
      if (response.ok) {
        const newlyCreatedTask = await response.json()

        // Notify Dashboard so it inserts it onto the user screen immediately
        if (onAddedTask) {
          onAddedTask(newlyCreatedTask)
        }

        setSuccessMdg("Task Created and Added Successfully!")
        setTaskTitle("")
        setDescryption("")
        setStatus("active")
        return
      }
    } catch (err) {
      console.error("Failed to create Task", error)
    }
  };

  return (
    <div className="w-full max-w-md bg-white rounded-2xl p-6 shadow-xl border border-gray-100 mb-8">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <h2 className="text-lg font-bold text-gray-900 tracking-tight mb-1">
          Your Workspace
        </h2>

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

        <div className="flex flex-col gap-3.5 w-full">
          <input
            className="w-full bg-white border border-gray-300 rounded-lg py-2.5 px-3.5 text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200"
            type="text"
            placeholder="Enter your Task Title"
            name="new task"
            value={TaskTitle}
            onChange={(e) => setTaskTitle(e.target.value)}
          />
          <input
            className="w-full bg-white border border-gray-300 rounded-lg py-2.5 px-3.5 text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200"
            type="text"
            placeholder="Enter Task Description"
            name="description"
            value={Descryption}
            onChange={(e) => setDescryption(e.target.value)}
          />
          <select
            className="w-full bg-white border border-gray-300 rounded-lg py-2.5 px-3.5 text-gray-900 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all duration-200"
            name="task_status"
            id="status"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="active">Active</option>
            <option value="completed">Completed</option>
          </select>

          <button
            className="w-full mt-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 px-4 rounded-lg shadow-md hover:shadow-lg transition-all duration-200 active:scale-[0.98]"
            type="submit"
          >
            Add New Task
          </button>
        </div>
      </form>
    </div>
  )
}

export default TaskForm