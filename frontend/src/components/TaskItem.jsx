import React from 'react'

const TaskItem = ({ task, onToggleComplete, onDelete }) => {
  return (
    <div className="flex items-center justify-between p-3.5 bg-slate-50 rounded-xl border border-gray-100 hover:border-gray-200 transition-all">
      <div className="flex items-center gap-3">
        <input
          id="status_toggle"
          name="status_toggle"
          type="checkbox"
          className="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 transition-all duration-200"
        />
        <label htmlFor="status_toggle" className="font-semibold text-gray-700">
          Task 1
        </label>
      </div>
      <span className="text-xs font-semibold px-2.5 py-1 bg-indigo-50 text-indigo-700 rounded-full uppercase tracking-wider border border-indigo-100">
        Active
      </span>
    </div>
  )
}

export default TaskItem