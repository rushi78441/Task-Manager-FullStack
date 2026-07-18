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

  // Simple state initialization: Read straight from memory on page refresh
  const [userEmail, setUserEmail] = useState(() => {
    return localStorage.getItem('saved_user') || '';
  });

  return (
    <Routes>
      {/* Root path defaults to Login */}
      <Route path="/" element={<LoginPage userEmail={userEmail} setUserEmail={setUserEmail} />} />
      <Route path="/login" element={<LoginPage userEmail={userEmail} setUserEmail={setUserEmail} />} />
      
      {/* Register Page path */}
      <Route path='/register' element={<RegisterPage userEmail={userEmail} setUserEmail={setUserEmail} />} />

      {/* Dashboard path */}
      <Route path="/dashboard" element={<DashBoardPage userEmail={userEmail} setUserEmail={setUserEmail} />} />
    </Routes>
  )
}

export default App
