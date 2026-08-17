import { useState, useCallback } from 'react'
import { searchPublications, getSuggestions } from '../api/client'

export function useSearch() {
  const [query, setQuery]       = useState('')
  const [results, setResults]   = useState([])
  const [total, setTotal]       = useState(0)
  const [page, setPage]         = useState(1)
  const [pages, setPages]       = useState(0)
  const [loading, setLoading]   = useState(false)
  const [error, setError]       = useState(null)
  const [searched, setSearched] = useState(false)
  const [suggestions, setSuggestions] = useState([])

  const search = useCallback(async (q = query, p = 1) => {
    if (!q.trim()) return
    setLoading(true)
    setError(null)
    setSearched(true)
    setSuggestions([])
    try {
      const data = await searchPublications(q, p)
      setResults(data.results || [])
      setTotal(data.total   || 0)
      setPages(data.pages   || 0)
      setPage(data.page     || p)
      setQuery(q)
    } catch (e) {
      setError(e?.response?.data?.error || e.message || 'Search failed')
    } finally {
      setLoading(false)
    }
  }, [query])

  const fetchSuggestions = useCallback(async (q) => {
    if (!q || q.length < 2) { setSuggestions([]); return }
    try {
      const data = await getSuggestions(q)
      setSuggestions(data.suggestions || [])
    } catch { setSuggestions([]) }
  }, [])

  const goToPage = useCallback((p) => {
    search(query, p)
  }, [search, query])

  const reset = () => {
    setQuery(''); setResults([]); setTotal(0); setPage(1)
    setPages(0); setSearched(false); setSuggestions([])
  }

  return {
    query, setQuery,
    results, total, page, pages,
    loading, error, searched,
    suggestions, setSuggestions,
    search, fetchSuggestions, goToPage, reset,
  }
}
