import { useState, useEffect, useRef } from 'react'
import './Chat.css'

export default function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  // Persist session ID and user ID
  const sessionIdRef = useRef('session-' + Math.random().toString(36).substring(2, 15))
  const userId = 'user-1'
  const sessionCreatedRef = useRef(false)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const ensureSession = async () => {
    // If we think we created it, skip. 
    // (Optional: handle session expiration if needed, but for local dev this is fine)
    if (sessionCreatedRef.current) return;

    try {
      const sid = sessionIdRef.current;
      const url = `/apps/dundra/users/${userId}/sessions/${sid}`;
      console.log(`Creating session: ${url}`);

      // Send no body, just like the working curl command
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      if (res.ok || res.status === 400) {
        console.log("Session created or already exists");
        sessionCreatedRef.current = true;
      } else {
        const text = await res.text();
        console.error(`Failed to create session (${res.status}): ${text}`);
      }
    } catch (e) {
      console.error("Error creating session (network/other):", e);
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMsg = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setIsLoading(true)

    try {
      await ensureSession();

      // Create a temporary message for the assistant
      setMessages(prev => [...prev, { role: 'model', content: '' }])

      const payload = {
        app_name: 'dundra',
        user_id: userId,
        session_id: sessionIdRef.current,
        new_message: {
          role: 'user',
          parts: [{ text: userMsg.content }]
        },
        streaming: true
      };

      console.log("Sending payload to /run_sse:", JSON.stringify(payload, null, 2));

      const response = await fetch('/run_sse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText} (${response.status})`)
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let assistantContent = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        // Parse SSE format (data: ...)
        const lines = chunk.split('\n')
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const dataStr = line.slice(6)
            if (dataStr === '[DONE]') continue
            try {
              const data = JSON.parse(dataStr)

              let contentChunk = ''
              // ADK event structure usually has content which is a types.Content object
              if (data.content && data.content.parts) {
                for (const part of data.content.parts) {
                  if (part.text) contentChunk += part.text;
                }
              } else if (typeof data === 'string') {
                contentChunk = data;
              } else if (data.text) {
                contentChunk = data.text;
              }

              if (contentChunk) {
                assistantContent += contentChunk
                setMessages(prev => {
                  const newMsgs = [...prev]
                  newMsgs[newMsgs.length - 1] = { role: 'model', content: assistantContent }
                  return newMsgs
                })
              }
            } catch (e) {
              console.error("Error parsing SSE data", e)
            }
          }
        }
      }

    } catch (error) {
      console.error("Chat error:", error)
      setMessages(prev => [...prev, { role: 'error', content: `Error: ${error.message}` }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="welcome-message">
            <h2>Welcome to Dundra</h2>
            <p>Start by describing the D&D adventure you want to create.</p>
          </div>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.role === 'model' ? (
                <div dangerouslySetInnerHTML={{ __html: msg.content.replace(/\n/g, '<br/>') }} />
              ) : (
                msg.content
              )}
            </div>
          </div>
        ))}
        {isLoading && <div className="loading-indicator">Agents are working...</div>}
        <div ref={messagesEndRef} />
      </div>
      <form onSubmit={handleSubmit} className="chat-input-form">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Describe your story..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading || !input.trim()}>Send</button>
      </form>
    </div>
  )
}
