import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import TaskForm from '../components/TaskForm'
import TaskItem from '../components/TaskItem'


const DashBoardPage = () => {

  return (
    <div className="bg-linear-to-br from-slate-50 to-gray-100 min-h-screen w-full flex flex-col p-4 box-border">
      {/* Realistic Navigation Bar */}
      <nav className="w-full mb-6 p-5 px-8 shadow-md rounded-2xl bg-white border border-gray-100 font-bold text-2xl text-gray-900 flex justify-between items-center">
        <h1>Task Manager DashBoard</h1>
        <span className="text-sm font-normal text-gray-500 bg-gray-100 px-3 py-1 rounded-full border border-gray-200">
          v1.0
        </span>
      </nav>

      {/* Main Workspace Area */}
      <div className="flex-1 flex flex-col items-center justify-start w-full max-w-4xl mx-auto px-4">

        {/* Welcome Header */}
        <div className="w-full text-left text-xl font-extrabold text-gray-900 mb-5 self-start tracking-tight">
          Welcome Admin
        </div>

        {/* The Centered Workspace Form Box */}
        <TaskForm />

        {/* Tasks Display Section */}
        <div className="w-full max-w-md bg-white border border-gray-100 rounded-2xl p-6 shadow-xl self-center">
          <h3 className="text-lg font-bold text-gray-900 tracking-tight mb-4">
            Your Tasks
          </h3>
          <TaskItem />
        </div>
      </div>
    </div>
  )
}

export default DashBoardPage