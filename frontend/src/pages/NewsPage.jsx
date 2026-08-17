/* ═══════════════════════════════════════════════════════════════════
   NewsPage.jsx  —  Task 2: News Document Clustering (K-Means, K=3)
   ═══════════════════════════════════════════════════════════════════ */
import { useState, useEffect, useRef } from 'react'
import {
  getNewsStats, getCrawlStatus, classifyText,
  triggerCollection, getNewsArticles
} from '../api/client'
import { TrendingUp, Clapperboard, Landmark, Target, LayoutDashboard, Network, Newspaper } from 'lucide-react'
import './NewsPage.css'

/* ── Category colours & icons ──────────────────────────────────── */
const CATS = {
  Economics:     { color: 'var(--c-econ)',  icon: <TrendingUp size={16} />, hex: '#3b82f6' },
  Entertainment: { color: 'var(--c-ent)',   icon: <Clapperboard size={16} />, hex: '#a855f7' },
  Politics:      { color: 'var(--c-pol)',   icon: <Landmark size={16} />, hex: '#10b981' },
}

/* ── Mini donut chart ─────────────────────────────────────────── */
function DonutChart({ distribution, total }) {
  const cats = Object.keys(CATS)
  const vals = cats.map(c => distribution[c] || 0)
  const sum  = vals.reduce((a,b) => a+b, 0) || 1

  let offset = 0
  const R = 48, C = 60
  const circumference = 2 * Math.PI * R

  const slices = cats.map((c, i) => {
    const frac  = vals[i] / sum
    const dash  = frac * circumference
    const gap   = circumference - dash
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
        <text x={C} y={C - 4} textAnchor="middle" fill="#f0f0ff" fontSize="16" fontWeight="700">{total}</text>
        <text x={C} y={C + 13} textAnchor="middle" fill="#8888bb" fontSize="8">documents</text>
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

/* ── PCA Scatter plot ──────────────────────────────────────────── */
function ScatterPlot({ points }) {
  const svgRef = useRef(null)
  if (!points || points.length === 0) return (
    <div className="scatter-empty">No cluster data available yet. Run data collection first.</div>
  )

  const xs = points.map(p => p.pca_x)
  const ys = points.map(p => p.pca_y)
  const xMin = Math.min(...xs), xMax = Math.max(...xs)
  const yMin = Math.min(...ys), yMax = Math.max(...ys)
  const xRange = xMax - xMin || 1
  const yRange = yMax - yMin || 1

  const W = 520, H = 340, PAD = 30
  const toSx = x => PAD + ((x - xMin) / xRange) * (W - 2 * PAD)
  const toSy = y => (H - PAD) - ((y - yMin) / yRange) * (H - 2 * PAD)

  return (
    <div className="scatter-wrap">
      <svg ref={svgRef} viewBox={`0 0 ${W} ${H}`} className="scatter-svg" role="img" aria-label="K-Means cluster scatter plot">
        {/* Grid lines */}
        {[0.25, 0.5, 0.75].map(f => (
          <g key={f}>
            <line x1={PAD + f*(W-2*PAD)} y1={PAD} x2={PAD + f*(W-2*PAD)} y2={H-PAD}
              stroke="rgba(255,255,255,0.04)" strokeWidth="1" />
            <line x1={PAD} y1={PAD + f*(H-2*PAD)} x2={W-PAD} y2={PAD + f*(H-2*PAD)}
              stroke="rgba(255,255,255,0.04)" strokeWidth="1" />
          </g>
        ))}
        {/* Points */}
        {points.map((p, i) => {
          const cat  = p.category || 'Economics'
          const info = CATS[cat] || CATS['Economics']
          return (
            <circle
              key={i}
              cx={toSx(p.pca_x)}
              cy={toSy(p.pca_y)}
              r={3.5}
              fill={info.hex}
              fillOpacity={0.75}
              stroke={info.hex}
              strokeOpacity={0.3}
              strokeWidth={1}
            >
              <title>{p.title || cat}</title>
            </circle>
          )
        })}
        {/* Axis labels */}
        <text x={W/2} y={H-4} textAnchor="middle" fill="#4a4a6a" fontSize="9">PCA Component 1</text>
        <text x={8} y={H/2} textAnchor="middle" fill="#4a4a6a" fontSize="9"
          transform={`rotate(-90 8 ${H/2})`}>PCA Component 2</text>
      </svg>
      <div className="scatter-legend">
        {Object.entries(CATS).map(([c, info]) => (
          <span key={c} className="sc-leg-item">
            <span className="sc-dot" style={{ background: info.hex }} />
            {info.icon} {c}
          </span>
        ))}
      </div>
      <p className="scatter-caption">
        Figure 1. PCA 2D projection of {points.length} news articles into three K-Means clusters (K=3).
        Each point represents one article. Cluster separation indicates category distinctiveness.
      </p>
    </div>
  )
}

/* ── Classifier panel ──────────────────────────────────────────── */
function ClassifierPanel() {
  const [text, setText]         = useState('')
  const [result, setResult]     = useState(null)
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState(null)

  const classify = async () => {
    if (!text.trim()) return
    setLoading(true); setError(null); setResult(null)
    try {
      const data = await classifyText(text)
      setResult(data)
    } catch (e) {
      setError(e?.response?.data?.error || e.message || 'Classification failed')
    } finally {
      setLoading(false)
    }
  }

  const cat = result?.category
  return (
    <div className="classifier-panel">
      <h3 className="panel-title">🔮 Classify a Document</h3>
      <p className="panel-desc">
        Enter any text — the K-Means model will classify it into Economics, Entertainment, or Politics.
      </p>
      <textarea
        id="classify-textarea"
        className="classify-input"
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Paste a sentence, paragraph, or news article…"
        rows={5}
        aria-label="Text to classify"
      />
      <button
        id="classify-btn"
        className="classify-btn"
        onClick={classify}
        disabled={loading || !text.trim()}
      >
        {loading ? 'Classifying…' : 'Classify Text'}
      </button>

      {error && (
        <div className="classify-error" role="alert">⚠️ {error}</div>
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
    </div>
  )
}

/* ── Articles table ────────────────────────────────────────────── */
function ArticlesTable({ category }) {
  const [articles, setArticles] = useState([])
  const [page, setPage]         = useState(1)
  const [pages, setPages]       = useState(1)
  const [loading, setLoading]   = useState(false)

  useEffect(() => {
    setLoading(true)
    getNewsArticles(category, page)
      .then(d => { setArticles(d.articles || []); setPages(d.pages || 1) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [category, page])

  if (loading) return <div className="articles-loading">Loading…</div>
  if (!articles.length) return <div className="articles-empty">No articles found in this category.</div>

  return (
    <div className="articles-wrap">
      <table className="articles-table" role="table" aria-label="News articles">
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
                <td className="art-num">{(page-1)*10 + i + 1}</td>
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
                <td className="art-date">{a.published ? a.published.slice(0,10) : '—'}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
      {pages > 1 && (
        <div className="art-pager">
          <button className="page-btn" disabled={page <= 1} onClick={() => setPage(p => p-1)}>‹</button>
          <span>{page} / {pages}</span>
          <button className="page-btn" disabled={page >= pages} onClick={() => setPage(p => p+1)}>›</button>
        </div>
      )}
    </div>
  )
}

/* ══════════════════════════════════════════════════════════════
   Main NewsPage component
   ══════════════════════════════════════════════════════════════ */
export default function NewsPage() {
  const [stats, setStats]       = useState(null)
  const [points, setPoints]     = useState([])
  const [activeTab, setActiveTab] = useState('overview')
  const [collecting, setCollecting] = useState(false)
  const [collectMsg, setCollectMsg] = useState('')
  const [filterCat, setFilterCat] = useState('')

  useEffect(() => {
    getNewsStats().then(d => setStats(d)).catch(() => {})
    getCrawlStatus().then(() => {}).catch(() => {})
  }, [])

  useEffect(() => {
    if (activeTab === 'clusters') {
      import('../api/client').then(({ getCrawlStatus, getClusterData }) => {
        getClusterData().then(d => setPoints(d.points || [])).catch(() => {})
      })
    }
  }, [activeTab])

  const handleCollect = async () => {
    setCollecting(true)
    setCollectMsg('Running collection & K-Means training…')
    try {
      const res = await triggerCollection()
      setCollectMsg(`✅ Done! ${res.summary?.new_stored ?? 0} new articles stored.`)
      getNewsStats().then(d => setStats(d)).catch(() => {})
    } catch (e) {
      setCollectMsg(`⚠️ Error: ${e?.response?.data?.message || e.message}`)
    } finally {
      setCollecting(false)
    }
  }

  const dist  = stats?.distribution || {}
  const total = stats?.total        || 0
  const model = stats?.model        || {}

  return (
    <div className="news-page">
      {/* Page header */}
      <header className="news-hero">
        <div className="news-hero-inner">
          <div className="hero-badge animate-fadeUp">📰 K-Means Clustering · K = 3</div>
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

      {/* Sub-navigation */}
      <div className="news-subnav">
        {[
          { key: 'overview',  label: <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><LayoutDashboard size={16} /> Overview</span>   },
          { key: 'classify',  label: <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><Target size={16} /> Classify</span>   },
          { key: 'clusters',  label: <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><Network size={16} /> Clusters</span>   },
          { key: 'articles',  label: <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}><Newspaper size={16} /> Articles</span>   },
        ].map(({ key, label }) => (
          <button
            key={key}
            id={`news-tab-${key}`}
            className={`subnav-btn ${activeTab === key ? 'active' : ''}`}
            onClick={() => setActiveTab(key)}
          >{label}</button>
        ))}
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
                  <dt>Trained at</dt>
                  <dd>{model.trained_at ? model.trained_at.slice(0,19).replace('T',' ') : '—'}</dd>
                </dl>
              ) : (
                <p className="no-model">No model trained yet. Collect RSS data to train.</p>
              )}

              <div className="collect-section">
                <button
                  id="collect-btn"
                  className="collect-btn"
                  onClick={handleCollect}
                  disabled={collecting}
                >
                  {collecting ? '⏳ Running…' : '🔄 Collect & Retrain'}
                </button>
                {collectMsg && <p className="collect-msg">{collectMsg}</p>}
                <p className="collect-note">
                  Fetches RSS feeds, stores ≥150 articles per category, re-trains K-Means.
                </p>
              </div>
            </div>

            {/* Category distribution bars */}
            <div className="news-card span-2">
              <h3>Category Distribution</h3>
              <div className="dist-bars">
                {Object.entries(CATS).map(([cat, info]) => {
                  const count = dist[cat] || 0
                  const pct   = total > 0 ? (count / total) * 100 : 0
                  return (
                    <div key={cat} className="dist-row">
                      <span className="dist-label">{info.icon} {cat}</span>
                      <div className="dist-track">
                        <div className="dist-fill"
                          style={{ width: `${pct}%`, background: info.hex }} />
                      </div>
                      <span className="dist-count">{count}</span>
                      <span className="dist-pct">({pct.toFixed(1)}%)</span>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        )}

        {/* ── CLUSTERS ── */}
        {activeTab === 'clusters' && (
          <div className="animate-fadeIn">
            <div className="news-card">
              <h3>K-Means Cluster Visualisation (PCA 2D Projection)</h3>
              <ScatterPlot points={points} />
            </div>
          </div>
        )}

        {/* ── ARTICLES ── */}
        {activeTab === 'articles' && (
          <div className="animate-fadeIn">
            <div className="news-card">
              <div className="articles-header">
                <h3>News Articles</h3>
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
              <ArticlesTable category={filterCat} />
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
