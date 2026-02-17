import { useState } from 'react'
import Chat from './components/Chat'
import StoryLibrary from './components/StoryLibrary'
import Login from './components/Login'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import './App.css'

function AuthenticatedApp() {
  const [activeTab, setActiveTab] = useState('chat')
  const { currentUser, logout } = useAuth()

  if (!currentUser) {
    return <Login />
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-left">
          <h1>Dundra <span className="highlight">ADK</span></h1>
        </div>
        <div className="header-right">
          <nav className="app-nav">
            <button
              className={activeTab === 'chat' ? 'active' : ''}
              onClick={() => setActiveTab('chat')}
            >
              Chat Agent
            </button>
            <button
              className={activeTab === 'library' ? 'active' : ''}
              onClick={() => setActiveTab('library')}
            >
              Story Library
            </button>
          </nav>
          <button onClick={logout} className="logout-btn">Logout</button>
        </div>
      </header>

      <main className="app-main">
        {activeTab === 'chat' ? <Chat /> : <StoryLibrary />}
      </main>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <AuthenticatedApp />
    </AuthProvider>
  )
}

export default App
