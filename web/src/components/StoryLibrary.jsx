import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import './StoryLibrary.css'

export default function StoryLibrary() {
  const { currentUser } = useAuth()
  const [stories, setStories] = useState([])
  const [error, setError] = useState(null)
  const [selectedStory, setSelectedStory] = useState(null)

  useEffect(() => {
    fetchStories()
  }, [])

  const fetchStories = async () => {
    try {
      const token = await currentUser.getIdToken();
      const res = await fetch('/api/stories', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      if (!res.ok) throw new Error("Failed to fetch stories")
      const data = await res.json()
      setStories(data)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="library-container">
      <div className="library-header">
        <h2>Adventures</h2>
        <button onClick={fetchStories} className="refresh-btn">Refresh</button>
      </div>
      
      {error && <div className="error-banner">{error}</div>}
      
      <div className="stories-grid">
        {stories.map((story, idx) => (
          <div key={idx} className="story-card">
            <div className="story-icon">📜</div>
            <div className="story-info">
                <h3>{story.name}</h3>
                <p>{new Date(story.created).toLocaleDateString()} {new Date(story.created).toLocaleTimeString()}</p>
                <div className="story-meta">
                    <span className={`tag ${story.source}`}>{story.source}</span>
                </div>
            </div>
            <div className="story-actions">
              <button
                onClick={(e) => {
                  e.preventDefault()
                  setSelectedStory(story)
                }}
                className="view-btn"
                style={{ width: '100%', border: 'none', cursor: 'pointer' }}
              >
                    Read Story
              </button>
            </div>
          </div>
        ))}
        {stories.length === 0 && !error && (
            <p className="no-stories">No stories found. Generate one in the Chat!</p>
        )}
      </div>

      {selectedStory && (
        <div className="story-modal-overlay" onClick={() => setSelectedStory(null)}>
          <div className="story-modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>{selectedStory.name}</h3>
              <button className="close-modal-btn" onClick={() => setSelectedStory(null)}>×</button>
            </div>
            <div className="story-iframe-container">
              <iframe
                src={selectedStory.url}
                className="story-iframe"
                title={selectedStory.name}
              />
            </div>
          </div>
        </div>
      )}
    </div>

  )
}
