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

        <footer className="app-footer">
          <div className="footer-content">
          </div>
        </footer>
      </div>
    </>
  )
}
