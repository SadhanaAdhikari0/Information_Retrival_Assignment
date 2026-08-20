/* ═══════════════════════════════════════════════════════════════════
   NewsPage.jsx  —  Task 2: News Document Clustering (K-Means, K=3)
   ═══════════════════════════════════════════════════════════════════ */
import { useState, useEffect, useRef } from 'react'
import {
  getNewsStats, getCrawlStatus, classifyText, getRecentClassifications, clearRecentClassifications, getClassifySuggestions,
  triggerCollection, getNewsArticles, getNewsSuggestions, getClusterData
} from '../api/client'
import { TrendingUp, Clapperboard, Landmark, Target, LayoutDashboard, Network, Newspaper, Hourglass, RefreshCw, AlertTriangle, AlertCircle, Trash2 } from 'lucide-react'
import { Chart as ChartJS, LinearScale, PointElement, Tooltip, Legend } from 'chart.js'
import { Scatter } from 'react-chartjs-2'

ChartJS.register(LinearScale, PointElement, Tooltip, Legend)

import './NewsPage.css'

/* ── Category colours & icons ──────────────────────────────────── */
const CATS = {
  Economics: { color: '#06b6d4', icon: <TrendingUp size={16} />, hex: '#06b6d4' }, // Cyan
  Entertainment: { color: '#f59e0b', icon: <Clapperboard size={16} />, hex: '#f59e0b' }, // Orange
  Politics: { color: '#a855f7', icon: <Landmark size={16} />, hex: '#a855f7' }, // Purple
}

/* ── Mini donut chart ─────────────────────────────────────────── */
function DonutChart({ distribution, total }) {
  const cats = Object.keys(CATS)
  const vals = cats.map(c => distribution[c] || 0)
  const sum = vals.reduce((a, b) => a + b, 0) || 1

  let offset = 0
  const R = 48, C = 60
  const circumference = 2 * Math.PI * R

  const slices = cats.map((c, i) => {
    const frac = vals[i] / sum
    const dash = frac * circumference
    const gap = circumference - dash
    const rotate = offset * 360
    offset += frac
    return { c, frac, dash, gap, rotate }
  })

  return (
    <div className="donut-chart-wrap">
      <svg viewBox="0 0 120 120" width="160" height="160">
        {slices.map(({ c, dash, gap, rotate }) => (
          <circle
            key={c}
            cx={C} cy={C} r={R}
            fill="none"
            stroke={CATS[c].hex}
            strokeWidth="14"
            strokeDasharray={`${dash} ${gap}`}
            strokeDashoffset={0}
            transform={`rotate(${rotate * 360 - 90} ${C} ${C})`}
            style={{ transition: 'stroke-dasharray 0.6s ease' }}
          />
        ))}
        <text x={C} y={C - 4} textAnchor="middle" fill="var(--text-primary)" fontSize="16" fontWeight="700">{total}</text>
        <text x={C} y={C + 13} textAnchor="middle" fill="var(--text-secondary)" fontSize="8">documents</text>
      </svg>
      <div className="donut-legend">
        {cats.map(c => (
          <div key={c} className="legend-row">
            <span className="legend-dot" style={{ background: CATS[c].hex }} />
            <span>{CATS[c].icon} {c}</span>
            <span className="legend-count">{distribution[c] || 0}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

/* ── PCA Scatter plot (2D) ──────────────────────────────────────────── */
function ScatterPlot({ points }) {
  if (!points || points.length === 0) return (
    <div className="scatter-empty">No cluster data available yet. Run data collection first.</div>
  )

  const datasets = Object.keys(CATS).map(cat => {
    const catPoints = points.filter(p => (p.category || 'Economics') === cat)
    return {
      label: cat,
      data: catPoints.map(p => ({ x: p.pca_x, y: p.pca_y, title: p.title || cat })),
      backgroundColor: CATS[cat].hex,
      borderColor: CATS[cat].hex,
      pointRadius: 4,
      pointHoverRadius: 6,
    }
  })

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'bottom', labels: { color: 'var(--text-secondary)' } },
      tooltip: {
        callbacks: {
          label: (ctx) => ctx.raw.title
        }
      }
    },
    scales: {
      x: { title: { display: true, text: 'PCA Component 1', color: 'var(--text-secondary)' }, grid: { color: 'rgba(128,128,128,0.1)' } },
      y: { title: { display: true, text: 'PCA Component 2', color: 'var(--text-secondary)' }, grid: { color: 'rgba(128,128,128,0.1)' } }
    }
  }

  return (
    <div className="scatter-wrap" style={{ width: '100%', height: '450px' }}>
      <Scatter data={{ datasets }} options={options} />
      <p className="scatter-caption" style={{ marginTop: '1rem' }}>
        PCA 2D projection of {points.length} news articles into three K-Means clusters (K=3).
        Each point represents one article. The interactive 2D view allows better analysis of cluster separation.
      </p>
    </div>
  )
}

/* ── Classifier panel ──────────────────────────────────────────── */
function ClassifierPanel() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [suggestions, setSuggestions] = useState([])

  const fetchSuggestions = async (val) => {
    if (!val || val.trim().length === 0) {
      setSuggestions([])
      return
    }
    try {
      const data = await getClassifySuggestions(val)
      setSuggestions(data.suggestions || [])
    } catch (e) {
      setSuggestions([])
    }
  }

  const handleTextChange = (e) => {
    const val = e.target.value
    setText(val)
    fetchSuggestions(val)
  }

  const fetchHistory = async () => {
    setIsRefreshing(true)
    try {
      const [data] = await Promise.all([
        getRecentClassifications(),
        new Promise(res => setTimeout(res, 600)) // Force delay so spin is visible
      ])
      setHistory(data.history || [])
    } catch (e) {
      console.error("Failed to load history", e)
    } finally {
      setIsRefreshing(false)
    }
  }

  const clearHistory = async () => {
    try {
      await clearRecentClassifications()
      setHistory([])
    } catch (e) {
      console.error("Failed to clear history", e)
    }
  }

  useEffect(() => {
    fetchHistory()
  }, [])

  const classify = async () => {
    if (!text.trim()) return
    setLoading(true); setError(null); setResult(null)
    try {
      const data = await classifyText(text)
      setResult(data)
      await fetchHistory()
    } catch (e) {
      setError(e?.response?.data?.error || e.message || 'Classification failed')
    } finally {
      setLoading(false)
    }
  }

  const cat = result?.category
  return (
    <div className="classifier-panel">
      <h3 className="panel-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Target size={20} style={{ color: 'var(--accent)' }} /> Classify a Document
      </h3>
      <p className="panel-desc">
        Enter any text — the K-Means model will classify it into Economics, Entertainment, or Politics.
      </p>
      <div style={{ position: 'relative' }}>
        <textarea
          id="classify-textarea"
          className="classify-input"
          value={text}
          onChange={handleTextChange}
          placeholder="Paste a sentence, paragraph, or news article…"
          rows={5}
          aria-label="Text to classify"
        />
        {suggestions.length > 0 && (
          <div className="suggest-popup" style={{ position: 'absolute', top: '100%', left: 0, right: 0, background: 'var(--bg-surface)', border: '1px solid var(--border)', borderRadius: '6px', marginTop: '4px', zIndex: 9999, boxShadow: '0 8px 24px rgba(0,0,0,0.12)' }}>
            {suggestions.map((s, idx) => (
              <div key={idx} style={{ padding: '10px 12px', borderBottom: idx === suggestions.length - 1 ? 'none' : '1px solid var(--border)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '8px' }}>
                <div
                  style={{ flex: 1, cursor: 'pointer', fontSize: '13px', color: 'var(--text-secondary)' }}
                  onClick={() => { setText(s); setSuggestions([]) }}
                >
                  {s.length > 60 ? s.slice(0, 60) + '...' : s}
                </div>
                <div style={{ display: 'flex', gap: '6px' }}>
                  <button
                    className="btn-ghost"
                    style={{ fontSize: '11px', padding: '4px 8px', background: 'var(--bg-inset)' }}
                    onClick={() => { setText(s); setSuggestions([]) }}
                  >
                    Select
                  </button>
                  <button
                    className="btn-ghost"
                    style={{ fontSize: '11px', padding: '4px 8px', color: 'var(--c-ent)', background: 'var(--bg-inset)' }}
                    onClick={() => setSuggestions(suggestions.filter(sg => sg !== s))}
                  >
                    Reject
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', marginTop: '12px', flexWrap: 'wrap' }}>
        <button
          id="classify-btn"
          className="classify-btn"
          style={{ flex: 1, minWidth: '140px', maxWidth: '200px', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px' }}
          onClick={classify}
          disabled={loading || !text.trim()}
        >
          {loading ? <Hourglass size={16} /> : <Target size={16} />}
          {loading ? 'Classifying…' : 'Classify Text'}
        </button>
        <button
          className="clear-btn"
          onClick={() => { setText(''); setResult(null); setError(null) }}
          style={{ flex: 1, minWidth: '140px', maxWidth: '200px', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px' }}
        >
          <Trash2 size={16} /> Clear
        </button>
      </div>

      {error && (
        <div className="classify-error" role="alert" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <AlertTriangle size={16} /> {error}
        </div>
      )}

      {result && (
        <div className="classify-result animate-fadeUp" style={{ borderColor: CATS[cat]?.hex }}>
          <div className="result-cat" style={{ color: CATS[cat]?.hex }}>
            <span className="cat-icon">{CATS[cat]?.icon}</span>
            {cat}
          </div>
          <div className="result-meta">
            <span>Confidence: <strong>{(result.confidence * 100).toFixed(1)}%</strong></span>
            <span>Method: <code>{result.method}</code></span>
          </div>
          <div className="conf-bar-wrap">
            <div className="conf-bar" style={{
              width: `${result.confidence * 100}%`,
              background: CATS[cat]?.hex,
            }} />
          </div>
        </div>
      )}

      {history.length > 0 && (
        <div className="classify-history animate-fadeIn">
          <div className="history-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
            <h4 className="history-title" style={{ margin: 0 }}>Recent Classifications (Last 10)</h4>
            <div style={{ display: 'flex', gap: '8px' }}>
              <button
                onClick={fetchHistory}
                className="btn-ghost"
                style={{ padding: '4px 8px', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '4px' }}
                title="Refresh history"
                disabled={isRefreshing}
              >
                <RefreshCw size={14} style={{ animation: isRefreshing ? 'spin 1s linear infinite' : 'none', transformOrigin: 'center' }} /> Refresh
              </button>
              <button
                onClick={clearHistory}
                className="btn-ghost"
                style={{ padding: '4px 8px', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--c-ent)' }}
                title="Clear all history"
              >
                <Trash2 size={14} /> Clear
              </button>
            </div>
          </div>
          <ul className="history-list">
            {history.map((h, i) => (
              <li key={i} className="history-item" onClick={() => { setText(h.text); setResult(h.result) }}>
                <div className="history-text">"{h.text.length > 60 ? h.text.slice(0, 60) + '...' : h.text}"</div>
                <div className="history-cat" style={{ color: CATS[h.result.category]?.hex, background: CATS[h.result.category]?.hex + '1a' }}>
                  {CATS[h.result.category]?.icon} {h.result.category}
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

/* ── Articles table ────────────────────────────────────────────── */
function ArticlesTable({ category, searchQuery }) {
  const [articles, setArticles] = useState([])
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    getNewsArticles(category, page, searchQuery)
      .then(d => { setArticles(d.articles || []); setPages(d.pages || 1) })
      .catch(() => { })
      .finally(() => setLoading(false))
  }, [category, page, searchQuery])

  if (loading) return <div className="articles-loading">Loading…</div>
  if (!articles.length) return <div className="articles-empty">No articles found in this category.</div>

  return (
    <div className="articles-wrap">
      <div style={{ overflowX: 'auto' }}>
        <table className="articles-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Title</th>
              <th>Source</th>
              <th>Category</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {articles.map((a, i) => {
              const cat = a.category || category
              return (
                <tr key={i}>
                  <td className="art-num">{(page - 1) * 10 + i + 1}</td>
                  <td>
                    <a href={a.url} target="_blank" rel="noopener noreferrer" className="art-link">
                      {a.title}
                    </a>
                  </td>
                  <td className="art-src">{a.source || '—'}</td>
                  <td>
                    <span className="cat-badge" style={{ background: CATS[cat]?.hex + '22', color: CATS[cat]?.hex }}>
                      {CATS[cat]?.icon} {cat}
                    </span>
                  </td>
                  <td className="art-date">{a.published ? a.published.slice(0, 10) : '—'}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      {pages > 1 && (
        <div className="art-pager">
          <button className="page-btn" disabled={page <= 1} onClick={() => setPage(p => p - 1)}>‹</button>
          <span>{page} / {pages}</span>
          <button className="page-btn" disabled={page >= pages} onClick={() => setPage(p => p + 1)}>›</button>
        </div>
      )}
    </div>
  )
}

/* ── News Search Bar with Suggestions ────────────────────────────── */
function NewsSearchBar({ onSearch }) {
  const [input, setInput] = useState('')
  const [suggestions, setSuggestions] = useState([])

  const fetchSuggestions = async (q) => {
    setInput(q)
    if (!q || q.length < 2) {
      setSuggestions([])
      return
    }
    try {
      const data = await getNewsSuggestions(q)
      setSuggestions(data.suggestions || [])
    } catch (e) {
      setSuggestions([])
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      setSuggestions([])
      onSearch(input)
    }
    if (e.key === 'Escape') setSuggestions([])
  }

  return (
    <div className="news-search-wrap">
      <input
        type="text"
        className="news-search-input"
        placeholder="Search clustered articles..."
        value={input}
        onChange={e => fetchSuggestions(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      {suggestions.length > 0 && (
        <ul className="news-suggestions" role="listbox">
          {suggestions.map((s, i) => (
            <li key={i} role="option" onClick={() => { setInput(s); setSuggestions([]); onSearch(s) }}>
              {s}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

/* ══════════════════════════════════════════════════════════════
   Main NewsPage component
   ══════════════════════════════════════════════════════════════ */
export default function NewsPage() {
  const [stats, setStats] = useState(null)
  const [clusterPoints, setClusterPoints] = useState([])
  const [activeTab, setActiveTab] = useState('overview')
  const [collecting, setCollecting] = useState(false)
  const [collectMsg, setCollectMsg] = useState('')
  const [filterCat, setFilterCat] = useState('')
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    getNewsStats().then(d => setStats(d)).catch(() => { })
    getCrawlStatus().then(() => { }).catch(() => { })
  }, [])

  useEffect(() => {
    if (activeTab === 'clusters') {
      getClusterData().then(d => setClusterPoints(d.points || [])).catch(() => { })
    }
  }, [activeTab])

  const handleCollect = async () => {
    setCollecting(true)
    setCollectMsg('Running collection & K-Means training…')
    try {
      const res = await triggerCollection()
      setCollectMsg(`Done! ${res.summary?.new_stored ?? 0} new articles stored.`)
      getNewsStats().then(d => setStats(d)).catch(() => { })
    } catch (e) {
      setCollectMsg(`Error: ${e?.response?.data?.message || e.message}`)
    } finally {
      setCollecting(false)
    }
  }

  const dist = stats?.distribution || {}
  const total = stats?.total || 0
  const model = stats?.model || {}

  return (
    <div className="news-page">
      {/* Page header */}
      <header className="news-hero">
        <div className="news-hero-inner">

          <h1 className="news-title animate-fadeUp" style={{ animationDelay: '60ms' }}>
            News Document Clustering
          </h1>
          <p className="news-subtitle animate-fadeUp" style={{ animationDelay: '120ms' }}>
            Automatic classification into Economics · Entertainment · Politics
          </p>

          {/* Cluster stat chips */}
          <div className="cat-chips animate-fadeUp" style={{ animationDelay: '180ms' }}>
            {Object.entries(CATS).map(([cat, info]) => (
              <div key={cat} className="cat-chip" style={{ borderColor: info.hex + '44' }}>
                <span>{info.icon}</span>
                <span>{cat}</span>
                <strong style={{ color: info.hex }}>{dist[cat] ?? '—'}</strong>
              </div>
            ))}
          </div>
        </div>
      </header>

      <div className="news-subnav-wrap" style={{ display: 'flex', justifyContent: 'center', padding: '24px' }}>
        <div className="news-subnav">
          {[
            { key: 'overview', label: <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><LayoutDashboard size={16} /> Overview</span> },
            { key: 'classify', label: <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><Target size={16} /> Classify</span> },
            { key: 'clusters', label: <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><Network size={16} /> Clusters</span> },
            { key: 'articles', label: <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><Newspaper size={16} /> Articles</span> },
          ].map(({ key, label }) => (
            <button
              key={key}
              id={`news-tab-${key}`}
              className={`subnav-btn ${activeTab === key ? 'active' : ''}`}
              onClick={() => setActiveTab(key)}
            >{label}</button>
          ))}
        </div>
      </div>

      <main className="news-main">

          {/* ── OVERVIEW ── */}
          {activeTab === 'overview' && (
            <div className="overview-grid animate-fadeIn">
              {/* Donut chart */}
              <div className="news-card">
                <h3>Cluster Distribution</h3>
                <DonutChart distribution={dist} total={total} />
              </div>

              {/* Model info */}
              <div className="news-card">
                <h3>Model Information</h3>
                {model.method ? (
                  <dl className="model-dl">
                    <dt>Algorithm</dt><dd>{model.method}</dd>
                    <dt>Clusters (K)</dt><dd>3</dd>
                    <dt>Total documents</dt><dd>{model.total_docs ?? '—'}</dd>
                    <dt>Silhouette score</dt>
                    <dd>{model.silhouette != null ? model.silhouette.toFixed(4) : '—'}</dd>
                    <dt>Accuracy</dt>
                    <dd>{model.accuracy != null ? (model.accuracy * 100).toFixed(1) + '%' : '—'}</dd>
                    <dt>Trained at</dt>
                    <dd>{model.trained_at ? model.trained_at.slice(0, 19).replace('T', ' ') : '—'}</dd>
                  </dl>
                ) : (
                  <p className="no-model">No model trained yet. Collect RSS data to train.</p>
                )}

              </div>


            </div>
          )}

          {/* ── CLUSTERS ── */}
          {activeTab === 'clusters' && (
            <div className="animate-fadeIn" style={{ maxWidth: '700px', margin: '0 auto' }}>
              <div className="news-card">
                <h3>K-Means Cluster Visualisation (PCA 2D Projection)</h3>
                <ScatterPlot points={clusterPoints} />
              </div>
            </div>
          )}

          {/* ── ARTICLES ── */}
          {activeTab === 'articles' && (
            <div className="animate-fadeIn">
              <div className="news-card">
                <div className="articles-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
                    <h3>News Articles</h3>
                    <NewsSearchBar onSearch={setSearchQuery} />
                  </div>
                  <div className="filter-row">
                    {['', ...Object.keys(CATS)].map(c => (
                      <button
                        key={c || 'all'}
                        className={`filter-btn ${filterCat === c ? 'active' : ''}`}
                        style={filterCat === c && c ? { borderColor: CATS[c]?.hex, color: CATS[c]?.hex } : {}}
                        onClick={() => setFilterCat(c)}
                      >{c || 'All'}</button>
                    ))}
                  </div>
                </div>
                <ArticlesTable category={filterCat} searchQuery={searchQuery} />
              </div>
            </div>
          )}

          {/* ── CLASSIFY ── */}
          {activeTab === 'classify' && (
            <div className="animate-fadeIn">
              <ClassifierPanel />
            </div>
          )}
      </main>
    </div>
  )
}
