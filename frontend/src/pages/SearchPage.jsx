/* ═══════════════════════════════════════════════════════════════════
   SearchPage.jsx  —  Task 1: Vertical Search Engine
   ═══════════════════════════════════════════════════════════════════ */
import { useState, useRef, useEffect } from 'react'
import { useSearch } from '../hooks/useSearch'
import { Calendar, User, Search, Database, Users, Clock, Zap, AlertTriangle, AlertCircle } from 'lucide-react'
import { triggerCrawl } from '../api/client'
import './SearchPage.css'

/* ── Score bar helper ───────────────────────────────────────── */
function ScoreBar({ score }) {
  const pct = Math.round(score * 100)
  const cls  = pct >= 50 ? 'high' : pct >= 20 ? 'mid' : 'low'
  return (
    <div className="score-bar-wrap" title={`Cosine similarity: ${score}`}>
      <span className="score-label">Relevance</span>
      <div className="score-track">
        <div className={`score-fill score-${cls}`} style={{ width: `${Math.max(pct, 2)}%` }} />
      </div>
      <span className={`score-val score-${cls}`}>{score.toFixed(4)}</span>
    </div>
  )
}

/* ── Single result card ─────────────────────────────────────── */
function ResultCard({ item, rank }) {
  const authorList = Array.isArray(item.authors) ? item.authors : []
  const profiles   = item.author_profiles || {}
  return (
    <article className="result-card animate-fadeUp" style={{ animationDelay: `${rank * 50}ms` }}>
      <div className="card-rank">#{rank}</div>
      <div className="card-body">
        <a
          className="card-title"
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          id={`result-${rank}`}
        >
          {item.title || 'Untitled Publication'}
        </a>

        <div className="card-meta">
          {item.publication_date && (
            <span className="meta-chip chip-date">
              <Calendar size={14} style={{ display: 'inline', verticalAlign: 'text-bottom', marginRight: '4px' }} />
              {item.publication_date}
            </span>
          )}
          {authorList.length > 0 && (
            <span className="meta-chip chip-authors">
              <User size={14} style={{ display: 'inline', verticalAlign: 'text-bottom', marginRight: '4px' }} />{' '}
              {authorList.map((a, i) => (
                <span key={i}>
                  {profiles[a]
                    ? <a href={profiles[a]} target="_blank" rel="noopener noreferrer" className="author-link">{a}</a>
                    : <span>{a}</span>
                  }
                  {i < authorList.length - 1 && ', '}
                </span>
              ))}
            </span>
          )}
        </div>

        <ScoreBar score={item.score} />
      </div>
    </article>
  )
}

/* ── Skeleton ───────────────────────────────────────────────── */
function SkeletonCard() {
  return (
    <div className="result-card skeleton-card">
      <div className="skeleton" style={{ width: 28, height: 28, borderRadius: 6 }} />
      <div className="card-body">
        <div className="skeleton" style={{ width: '65%', height: 18, marginBottom: 10 }} />
        <div className="skeleton" style={{ width: '40%', height: 13, marginBottom: 14 }} />
        <div className="skeleton" style={{ width: '100%', height: 8, borderRadius: 4 }} />
      </div>
    </div>
  )
}

/* ── Pagination ─────────────────────────────────────────────── */
function Pagination({ page, pages, onPage }) {
  if (pages <= 1) return null
  const nums = []
  for (let i = 1; i <= pages; i++) nums.push(i)
  return (
    <nav className="pagination" aria-label="Search result pages">
      <button
        className="page-btn" onClick={() => onPage(page - 1)}
        disabled={page <= 1} aria-label="Previous page"
      >‹</button>
      {nums.map(n => (
        <button
          key={n}
          id={`page-${n}`}
          className={`page-btn ${n === page ? 'active' : ''}`}
          onClick={() => onPage(n)}
          aria-current={n === page ? 'page' : undefined}
        >{n}</button>
      ))}
      <button
        className="page-btn" onClick={() => onPage(page + 1)}
        disabled={page >= pages} aria-label="Next page"
      >›</button>
    </nav>
  )
}

/* ── Hero search box ────────────────────────────────────────── */
function HeroSearch({ query, setQuery, onSearch, suggestions, clearSuggestions, fetchSuggestions }) {
  const inputRef = useRef(null)

  const handleKey = (e) => {
    if (e.key === 'Enter') { clearSuggestions(); onSearch(query) }
    if (e.key === 'Escape') clearSuggestions()
  }
  const handleChange = (e) => {
    setQuery(e.target.value)
    fetchSuggestions(e.target.value)
  }

  return (
    <div className="hero-search">
      <div className="search-box-wrap">
        <span className="search-icon-left"><Search size={18} /></span>
        <input
          ref={inputRef}
          id="main-search-input"
          className="search-input"
          type="search"
          value={query}
          onChange={handleChange}
          onKeyDown={handleKey}
          placeholder="Search publications, authors, keywords…"
          autoComplete="off"
          spellCheck="false"
          aria-label="Search query"
          aria-autocomplete="list"
          aria-controls="suggestions-list"
        />
        <button
          id="search-btn"
          className="search-btn"
          onClick={() => { clearSuggestions(); onSearch(query) }}
        >Search</button>

        {suggestions.length > 0 && (
          <ul id="suggestions-list" className="suggestions" role="listbox">
            {suggestions.map((s, i) => (
              <li key={i} role="option"
                className="suggestion-item"
                onClick={() => { setQuery(s); clearSuggestions(); onSearch(s) }}
              >{s}</li>
            ))}
          </ul>
        )}
      </div>

      <div className="quick-terms">
        {['machine learning', 'mental health', 'healthcare', 'community', 'nursing'].map(t => (
          <button key={t} className="quick-term" onClick={() => onSearch(t)}>{t}</button>
        ))}
      </div>
    </div>
  )
}

/* ══════════════════════════════════════════════════════════════
   Main SearchPage component
   ══════════════════════════════════════════════════════════════ */
export default function SearchPage() {
  const {
    query, setQuery,
    results, total, page, pages,
    loading, error, searched,
    suggestions, setSuggestions,
    search, fetchSuggestions, goToPage, reset,
  } = useSearch()

  const [crawlStatus, setCrawlStatus] = useState(null)
  const [isCrawling, setIsCrawling] = useState(false)
  const [crawlMsg, setCrawlMsg] = useState('')

  const handleCrawl = async () => {
    setIsCrawling(true)
    setCrawlMsg('Starting crawler...')
    try {
      const res = await triggerCrawl()
      setCrawlMsg(res.message || 'Crawler started in background')
    } catch (e) {
      setCrawlMsg('Failed to start crawler')
    }
    setTimeout(() => setCrawlMsg(''), 4000)
    setIsCrawling(false)
  }

  useEffect(() => {
    fetch('/api/crawl-status')
      .then(r => r.json())
      .then(d => setCrawlStatus(d))
      .catch(() => {})
  }, [])

  return (
    <div className={`search-page ${searched ? 'has-searched' : 'is-empty'}`}>

      {/* Hero banner */}
      <header className={`search-hero ${searched ? 'compact' : ''}`}>
        <div className="hero-inner">
          {!searched && (
            <>

              <h1 className="hero-title animate-fadeUp" style={{ animationDelay: '80ms' }}>
                Vertical Search Engine
              </h1>
              <p className="hero-subtitle animate-fadeUp" style={{ animationDelay: '160ms' }}>
                Vector Space Model · Cosine Similarity · Top-K=10 ranking
              </p>
            </>
          )}
          <HeroSearch
            query={query}
            setQuery={setQuery}
            onSearch={search}
            suggestions={suggestions}
            clearSuggestions={() => setSuggestions([])}
            fetchSuggestions={fetchSuggestions}
          />

          {/* Index stats strip */}
          {crawlStatus && (
            <div className="stats-strip animate-fadeIn" style={{ animationDelay: '240ms', display: 'inline-flex', justifyContent: 'center', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                <Database size={14} /> {crawlStatus.raw_pages ?? '—'} Research Publication Index
              </span>
              <span className="strip-dot" />
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                <Users size={14} /> {crawlStatus.profiles ?? '—'} Profiles Index
              </span>
              <span className="strip-dot" />
              <span style={{ display: 'inline-flex', alignItems: 'center', gap: '6px' }}>
                <Clock size={14} /> 3-month crawl interval
              </span>
            </div>
          )}
        </div>
      </header>

      {/* Results area */}
      <main className="results-area" role="main">
        <div className="results-inner">

          {/* Loading skeletons */}
          {loading && (
            <div className="results-list">
              {[...Array(5)].map((_, i) => <SkeletonCard key={i} />)}
            </div>
          )}

          {/* Error state */}
          {error && !loading && (
            <div className="state-box state-error" role="alert">
              <span className="state-icon"><AlertTriangle size={36} /></span>
              <div>
                <strong>Search error</strong>
                <p>{error}</p>
              </div>
            </div>
          )}

          {/* Empty state */}
          {searched && !loading && !error && results.length === 0 && (
            <div className="state-box state-empty">
              <span className="state-icon"><AlertCircle size={36} /></span>
              <div>
                <strong>No results found</strong>
                <p>Try different keywords or a broader search term.</p>
              </div>
              <button className="btn-ghost" onClick={reset}>Clear search</button>
            </div>
          )}

          {/* Results list */}
          {!loading && results.length > 0 && (
            <>
              <div className="results-header">
                <span className="results-count">
                  {total} result{total !== 1 ? 's' : ''} for &ldquo;<strong>{query}</strong>&rdquo;
                </span>
                <span className="results-page-info">Page {page} of {pages}</span>
              </div>

              <div className="results-list">
                {results.map((r, i) => (
                  <ResultCard
                    key={r.url || i}
                    item={r}
                    rank={(page - 1) * 10 + i + 1}
                  />
                ))}
              </div>

              <Pagination page={page} pages={pages} onPage={goToPage} />
            </>
          )}
        </div>
      </main>
    </div>
  )
}
