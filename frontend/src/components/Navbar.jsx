/* ═══════════════════════════════════════════════════════════════════
   Navbar.jsx  —  IR Research Platform top navigation
   ═══════════════════════════════════════════════════════════════════ */
import './Navbar.css'
import { LayoutDashboard, Target, Network } from 'lucide-react'

export default function Navbar({ activeTab, onTab }) {
  return (
    <nav className="navbar" role="navigation" aria-label="Main navigation">
      <div className="navbar-inner">
        <a className="navbar-brand" href="/" onClick={e => { e.preventDefault(); onTab('search') }}>
          <span className="brand-icon"><LayoutDashboard size={24} /></span>
          <span className="brand-text">
            <span className="brand-main">Coventry University</span>
            <span className="brand-sub">ST7071CEM | IR Research</span>
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
            <span className="tab-icon"><Target size={18} /></span>
            <span>Vertical Search</span>
          </button>
          <button
            id="tab-news"
            role="tab"
            aria-selected={activeTab === 'news'}
            className={`nav-tab ${activeTab === 'news' ? 'active' : ''}`}
            onClick={() => onTab('news')}
          >
            <span className="tab-icon"><Network size={18} /></span>
            <span>News Clustering</span>
          </button>
        </div>

        <div className="navbar-badge">
          <span className="badge-dot" />
          System Online
        </div>
      </div>
    </nav>
  )
}
