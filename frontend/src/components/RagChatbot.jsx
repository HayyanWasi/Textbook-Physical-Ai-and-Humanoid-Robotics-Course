import { useState } from 'react';

const API_URL = 'http://localhost:8000/api/chat';

export default function RagChatbot({ context, placeholder }) {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setAnswer('');
    setSources([]);
    setError('');

    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, context }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || data.error || 'An error occurred. Please try again.');
      } else {
        setAnswer(data.answer);
        setSources(data.sources || []);
      }
    } catch {
      setError('Could not reach the backend. Make sure the server is running on port 8000.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: '1.25rem', marginTop: '2rem' }}>
      <p style={{ margin: '0 0 0.75rem', fontWeight: 600 }}>
        Ask about this chapter
      </p>

      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '0.5rem' }}>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={placeholder || 'Type your question here…'}
          rows={2}
          disabled={loading}
          style={{ flex: 1, padding: '0.5rem', borderRadius: 4, border: '1px solid #ccc', resize: 'vertical' }}
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          style={{ padding: '0.5rem 1rem', borderRadius: 4, cursor: loading ? 'wait' : 'pointer' }}
        >
          {loading ? '…' : 'Ask'}
        </button>
      </form>

      {loading && (
        <p style={{ marginTop: '0.75rem', color: '#666' }}>Searching the textbook…</p>
      )}

      {error && (
        <p style={{ marginTop: '0.75rem', color: '#c0392b' }}>{error}</p>
      )}

      {answer && (
        <div style={{ marginTop: '0.75rem' }}>
          <p style={{ margin: '0 0 0.5rem', whiteSpace: 'pre-wrap' }}>{answer}</p>
          {sources.length > 0 && (
            <details style={{ marginTop: '0.5rem' }}>
              <summary style={{ cursor: 'pointer', color: '#666', fontSize: '0.85rem' }}>
                Sources ({sources.length})
              </summary>
              <ul style={{ margin: '0.25rem 0 0 1rem', fontSize: '0.85rem', color: '#555' }}>
                {sources.map((s, i) => (
                  <li key={i}>{s.heading} — <em>{s.file}</em></li>
                ))}
              </ul>
            </details>
          )}
        </div>
      )}
    </div>
  );
}
