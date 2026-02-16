import { useState } from 'react'
import Chat from './components/Chat'
import StoryLibrary from './components/StoryLibrary'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('chat')

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Dundra <span className="highlight">ADK</span></h1>
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
      </header>

      <main className="app-main">
        {activeTab === 'chat' ? <Chat /> : <StoryLibrary />}
      </main>
    </div>
  )
}

export default App
