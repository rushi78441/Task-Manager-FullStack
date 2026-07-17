import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import {Routes , Route} from 'react-router-dom'
import DashBoardPage from './pages/DashBoardPage'
import LoginPage from './pages/LoginPage'

import './App.css'
import RegisterPage from './pages/RegisterPage'

function App() {
  return (
    <Routes>
      {/* Root path defaults to Login */}
      <Route path="/" element={<LoginPage />} />
      <Route path="/login" element={<LoginPage />} />
      
      {/* Register Page path */}
      <Route path='/register' element={<RegisterPage/>} />

      {/* Dashboard path */}
      <Route path="/dashboard" element={<DashBoardPage />} />
    </Routes>
  )
}

export default App
