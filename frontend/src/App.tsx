import { useEffect, useState } from 'react'

import { getAuthToken } from './api/client'
import LoginForm from './components/LoginForm'
import DashboardPage from './pages/DashboardPage'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => getAuthToken() !== null)

  useEffect(() => {
    const handleUnauthorized = () => setIsAuthenticated(false)
    window.addEventListener('auth:unauthorized', handleUnauthorized)
    return () => window.removeEventListener('auth:unauthorized', handleUnauthorized)
  }, [])

  return (
    <div className="min-h-screen bg-slate-50">
      {isAuthenticated ? (
        <DashboardPage onLogout={() => setIsAuthenticated(false)} />
      ) : (
        <LoginForm onAuthenticated={() => setIsAuthenticated(true)} />
      )}
    </div>
  )
}

export default App
