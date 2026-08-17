/* ═══════════════════════════════════════════════════════════════════
   Navbar.jsx  —  IR Research Platform top navigation
   ═══════════════════════════════════════════════════════════════════ */
import './Navbar.css'
import { Microscope, Search, Newspaper } from 'lucide-react'

export default function Navbar({ activeTab, onTab }) {
  return (
    <nav className="navbar" role="navigation" aria-label="Main navigation">
      <div className="navbar-inner">
        <a className="navbar-brand" href="/" onClick={e => { e.preventDefault(); onTab('search') }}>
          <span className="brand-icon"><Microscope size={24} /></span>
          <span className="brand-text">
            <span className="brand-main">IR Research</span>
            <span className="brand-sub">ST7071CEM</span>
          </span>
        </a>

        <div className="navbar-tabs" role="tablist">
          <button
            id="tab-search"
            role="tab"
            aria-selected={activeTab === 'search'}
            className={`nav-tab ${activeTab === 'search' ? 'active' : ''}`}
            onClick={() => onTab('search')}
          >
            <span className="tab-icon"><Search size={18} /></span>
            <span>Vertical Search</span>
          </button>
          <button
            id="tab-news"
            role="tab"
            aria-selected={activeTab === 'news'}
            className={`nav-tab ${activeTab === 'news' ? 'active' : ''}`}
            onClick={() => onTab('news')}
          >
            <span className="tab-icon"><Newspaper size={18} /></span>
            <span>News Clustering</span>
          </button>
        </div>

        <div className="navbar-badge">
          <span className="badge-dot" />
          Coventry University
        </div>
      </div>
    </nav>
  )
}
