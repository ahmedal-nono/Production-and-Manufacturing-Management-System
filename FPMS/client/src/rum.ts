/**
 * Lightweight real-user monitoring (RUM).
 *
 * Collects Core Web Vitals (LCP, CLS, INP) plus FCP and TTFB, then sends one
 * beacon per page load. No dependency on an external analytics service.
 */
import { adminApiUrl } from '@/api'

type Rating = 'good' | 'needs-improvement' | 'poor'

interface Sample {
  name: string
  value: number
  rating: Rating
  page_path: string
  device: string
  connection: string
}

const ENDPOINT = `${adminApiUrl}/rum/`
const ENABLED = import.meta.env.VITE_RUM !== 'false'

// [goodThreshold, poorThreshold]
const THRESHOLDS: Record<string, [number, number]> = {
  LCP: [2500, 4000],
  CLS: [0.1, 0.25],
  INP: [200, 500],
  FCP: [1800, 3000],
  TTFB: [800, 1800],
}

const values: Record<string, number> = {}
let sent = false

function rate(name: string, value: number): Rating {
  const [good, poor] = THRESHOLDS[name] ?? [0, 0]
  if (value <= good) return 'good'
  if (value <= poor) return 'needs-improvement'
  return 'poor'
}

function observe(type: string, callback: (entries: PerformanceEntry[]) => void) {
  if (typeof PerformanceObserver === 'undefined') return
  try {
    const observer = new PerformanceObserver((list) => callback(list.getEntries()))
    observer.observe({ type, buffered: true } as PerformanceObserverInit)
  } catch {
    // Unsupported entry type in this browser.
  }
}

function connectionType(): string {
  const connection = (navigator as any).connection
  return connection?.effectiveType ?? ''
}

function flush() {
  if (sent || !ENABLED) return
  sent = true

  const path = `${window.location.pathname}${window.location.search}`.slice(0, 200)
  const device = window.matchMedia('(max-width: 768px)').matches ? 'mobile' : 'desktop'
  const connection = connectionType()
  const samples: Sample[] = Object.entries(values)
    .filter(([, value]) => Number.isFinite(value) && value >= 0)
    .map(([name, value]) => ({
      name,
      value: Math.round(value * 1000) / 1000,
      rating: rate(name, value),
      page_path: path,
      device,
      connection,
    }))

  if (!samples.length) return
  const body = JSON.stringify({ metrics: samples })

  if (navigator.sendBeacon) {
    navigator.sendBeacon(ENDPOINT, new Blob([body], { type: 'application/json' }))
    return
  }
  fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body,
    keepalive: true,
  }).catch(() => {
    // Metrics are best-effort; never surface errors to the user.
  })
}

if (ENABLED) {
  // Navigation timings.
  try {
    const navigation = performance.getEntriesByType('navigation')[0] as
      | PerformanceNavigationTiming
      | undefined
    if (navigation) {
      values.TTFB = navigation.responseStart
    }
  } catch {
    // Ignore.
  }

  observe('paint', (entries) => {
    const fcp = entries.find((entry) => entry.name === 'first-contentful-paint')
    if (fcp) values.FCP = fcp.startTime
  })

  observe('largest-contentful-paint', (entries) => {
    const last = entries[entries.length - 1]
    if (last) values.LCP = last.startTime
  })

  let cls = 0
  observe('layout-shift', (entries) => {
    for (const entry of entries as any[]) {
      if (!entry.hadRecentInput) cls += entry.value
    }
    values.CLS = cls
  })

  let inp = 0
  observe('event', (entries) => {
    for (const entry of entries as any[]) {
      if (entry.duration > inp) inp = entry.duration
    }
    values.INP = inp
  })

  window.addEventListener('pagehide', flush, { once: true })
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') flush()
  })
}
