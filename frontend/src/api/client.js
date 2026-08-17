import axios from 'axios'

const api = axios.create({ baseURL: '/api', timeout: 120000 })

export const searchPublications = (query, page = 1) =>
  api.get('/search', { params: { q: query, page } }).then(r => r.data)

export const getSuggestions = (q) =>
  api.get('/suggestions', { params: { q } }).then(r => r.data)

export const getCrawlStatus = () =>
  api.get('/crawl-status').then(r => r.data)

export const triggerCrawl = () =>
  api.post('/crawler/run').then(r => r.data)

export const getNewsStats = () =>
  api.get('/news/stats').then(r => r.data)

export const getClusterData = () =>
  api.get('/news/clusters').then(r => r.data)

export const classifyText = (text) =>
  api.post('/news/classify', { text }).then(r => r.data)

export const triggerCollection = () =>
  api.post('/news/collect').then(r => r.data)

export const getNewsArticles = (category, page = 1) =>
  api.get('/news/articles', { params: { category, page } }).then(r => r.data)
