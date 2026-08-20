/**
 * App.jsx — ST7071CEM Information Retrieval Assignment
 * =====================================================
 * Root component for the integrated IR Research Platform.
 * Tab 1: Vertical Search Engine (Task 1 — VSM + Cosine Similarity)
 * Tab 2: News Document Clustering (Task 2 — K-Means, K=3)
 */
import { useState } from 'react'
import Navbar     from './components/Navbar'
import SearchPage from './pages/SearchPage'
import NewsPage   from './pages/NewsPage'
import './index.css'

export default function App() {
  const [activeTab, setActiveTab] = useState('search')

  return (
    <>
      {/* Decorative mesh background */}
      <div className="mesh-bg" aria-hidden="true" />

      <div className="app-shell">
        <Navbar activeTab={activeTab} onTab={setActiveTab} />

        {/* Tab panels — both remain mounted to preserve state */}
        <div
          id="panel-search"
          role="tabpanel"
          aria-labelledby="tab-search"
          style={{ display: activeTab === 'search' ? 'block' : 'none' }}
        >
          <SearchPage />
        </div>

        <div
          id="panel-news"
          role="tabpanel"
          aria-labelledby="tab-news"
          style={{ display: activeTab === 'news' ? 'block' : 'none' }}
        >
          <NewsPage />
        </div>

        <footer className="app-footer" style={{ marginTop: 'auto' }}>
          <div className="footer-content" style={{ textAlign: 'center', padding: '1.5rem', color: 'var(--text-secondary)', fontSize: '0.9rem', borderTop: '1px solid rgba(255,255,255,0.05)' }}>
            <p style={{ margin: 0 }}>Developed by <span style={{ color: 'var(--c-pol)', fontWeight: 600, letterSpacing: '0.5px' }}>Sadhana Adhikari</span></p>
          </div>
        </footer>
      </div>
    </>
  )
}
