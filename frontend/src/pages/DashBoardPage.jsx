import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import TaskForm from '../components/TaskForm'
import TaskItem from '../components/TaskItem'

const API_URL = "http://127.0.0.1:8000"

const DashBoardPage = ({ userEmail }) => {
  const [tasks, setTasks] = useState([])
  const navigate = useNavigate()

    // Added a handler to instantly add newly created tasks to the array list
  const handleTaskAdded = (newSingleTask) => {
    setTasks(prevTasks => [...prevTasks, newSingleTask])
  }

  // fetch tasks when dahboardpage load
  const fetchTasks = async () => {
    const token = localStorage.getItem('user_token')

    if (!token) {
     console.log("No token found. Redirecting to login...")
      navigate('/login') 
      return
    }

    // simulate fetch API 
    try {
      const response = await fetch(`${API_URL}/tasks`, {
        method: 'GET',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `bearer ${token}`
        }
      })

      // check Repsonse
      if (response.ok) {
        const data = await response.json()
        setTasks(data)
      }
      else if(response.status == 401){
        localStorage.removeItem('user_token')
        navigate('/login')
      }
    }
    catch (err) {
      console.error(err)
    }
  };

  // Added useEffect so tasks download instantly when the dashboard opens!
  useEffect(() => {
    fetchTasks();
  }, []);

  // Handle Task Deleted
  const handleTaskDeleted = (deletedId) => {
    // prev Tasks before update
    // we just keep the tasks foltered with if task_id not deleted id , means task_id == deleted_id --> we simple do not filter or take it and save in setTasks
    setTasks(prevTasks => prevTasks.filter(task => task.task_id !== deletedId))
  }

  // const handleTaskUpdated
  const handleTaskUpdated = (updateId, newStatus) => {
    /*
    1. We take prevTasks (the absolute latest snapshot of our tasks list).
    2. We loop through every single task using .map() to create a modified list.
    3. We check if the current task's ID matches the one we want to update.
       - If it MATCHES: We copy all original details ({...task}) but overwrite the status field with newStatus.
       - If it DOES NOT MATCH: We return the task exactly as it was, untouched.
    */
    setTasks(prevTasks =>
      prevTasks.map(task =>
        task.task_id === updateId ? { ...task, status: newStatus } : task
      )
    )
  }


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
          Welcome {userEmail}
        </div>

        {/* The Centered Workspace Form Box */}
        <TaskForm onAddedTask={handleTaskAdded} />

        {/* Tasks Display Section */}
        <div className="w-full max-w-md bg-white border border-gray-100 rounded-2xl p-6 shadow-xl self-center">
          <h3 className="text-lg font-bold text-gray-900 tracking-tight mb-4">
            Your Tasks
          </h3>

          {/* Tasks Display */}
          {tasks.length === 0 ? (
            <p className="text-sm text-gray-400 italic text-center py-4">No tasks found. Create one above!</p>
          ) : (
            <div className="flex flex-col gap-3">
              {/* Loop Throgh tasks list  using .map function*/}
              {tasks.map((individialTask) => (
                <TaskItem
                  key={individialTask.task_id}  // mapping key to specific task -id
                  task={individialTask}
                  onTaskUpdated={handleTaskUpdated}
                  onTaskDeleted={handleTaskDeleted}
                />
              ))}
            </div>
          )}


        </div>
      </div>
    </div>
  )
}

export default DashBoardPage