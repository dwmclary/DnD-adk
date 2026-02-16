import { useState, useEffect } from 'react'
import './StoryLibrary.css'

export default function StoryLibrary() {
  const [stories, setStories] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchStories()
  }, [])

  const fetchStories = async () => {
    try {
      const res = await fetch('/api/stories')
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
                <a href={story.url} target="_blank" rel="noopener noreferrer" className="view-btn">
                    Read Story
                </a>
            </div>
          </div>
        ))}
        {stories.length === 0 && !error && (
            <p className="no-stories">No stories found. Generate one in the Chat!</p>
        )}
      </div>
    </div>
  )
}
