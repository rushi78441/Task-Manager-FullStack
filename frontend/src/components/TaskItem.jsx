import React from 'react';

const API_URL = "http://127.0.0.1:8000"

const TaskItem = ({ task, onTaskDeleted, onTaskUpdated }) => {

  const token = localStorage.getItem('user_token')
  const isCompleted = task.status === "completed"

  const handleToggle = async () => {
    const nextStatus = isCompleted ? "active" : "completed"

    // Simulate Status Toggle API 
    try {
      const repsonse = await fetch(`${API_URL}/tasks/${task.task_id}`, {
        method: 'PATCH',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `bearer ${token}`
        },
        body: JSON.stringify({
          task_title: task.task_title,
          descryption: task.descryption || "",
          status: nextStatus
        })
      })

      // check response
      if (repsonse.ok) {
        onTaskUpdated(task.task_id, nextStatus)
        console.log("Task Status Updated successfully")
      }
    } catch (err) {
      console.error("Cannot Change Status of Task", err)
    }

  };

  // Handle Delete Task Button
  const handleDelete = async (e) => {
    e.preventDefault()

    // Simulate Delete API
    try {
      // delet api response
      const response = await fetch(`${API_URL}/tasks/${task.task_id}`, {
        method: 'DELETE',
        headers: { "Authorization": `bearer ${token}` }
      })

      // check reposne
      if (response.ok) {
        onTaskDeleted(task.task_id)
        console.log("Task Deleted Successfully")
      }
    } catch (err) {
      console.error("Error Deleting Tasks", err)
    }
  }

  return (
    <div className="flex items-center justify-between p-3.5 bg-slate-50 rounded-xl border border-gray-100 hover:border-gray-200 transition-all">
      <div className="flex items-center gap-3">
        <input
          id={`status_toggle_${task.task_id}`}
          name="status_toggle"
          type="checkbox"
          checked={isCompleted}
          onChange={handleToggle}
          className="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 transition-all duration-200 cursor-pointer"
        />
        <label
          htmlFor={`status_toggle_${task.task_id}`}
          className={`font-semibold transition-all cursor-pointer ${isCompleted ? "line-through text-gray-400 font-normal" : "text-gray-700"
            }`}
        >
          {task.task_title}
        </label>
      </div>

      <div className="flex items-center gap-3">
        {/* Status Badge */}
        <span className={`text-xs font-semibold px-2.5 py-1 rounded-full uppercase tracking-wider border ${isCompleted
          ? "bg-green-50 text-green-700 border-green-100"
          : "bg-indigo-50 text-indigo-700 border-indigo-100"
          }`}>
          {task.status}
        </span>


        {/* Action Button: Delete Task */}
        <button
          className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all active:scale-95"
          aria-label="Delete task"
          onClick={handleDelete}
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default TaskItem;