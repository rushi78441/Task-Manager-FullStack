import React, { useState } from 'react'

const TaskForm = () => {
  
  // form input states handling
  const [TaskTitle, setTaskTitle] = React.useState("")
  const [Descryption, setDescryption] = React.useState("")
  const [status , setStatus] = React.useState("Active")

  // Handle Submit
  const handleSubmit = async (e) => {
    e.preventDefault()
  }

  return (
    <div className="w-full max-w-md bg-white rounded-2xl p-6 shadow-xl border border-gray-100 mb-8">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <h2 className="text-lg font-bold text-gray-900 tracking-tight mb-1">
          Your Workspace
        </h2>

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
            <option value="Active">Active</option>
            <option value="Completed">Completed</option>
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