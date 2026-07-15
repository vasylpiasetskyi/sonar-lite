import { METRIC_LABELS, METRIC_UNITS } from '../api/types'
import type { LatestReading, MetricAnalytics, MetricType } from '../api/types'
import EmptyState from './EmptyState'

interface MetricCardProps {
  metricType: MetricType
  latest: LatestReading | null
  analytics: MetricAnalytics
}

const TREND_ARROWS: Record<'up' | 'down' | 'stable', string> = {
  up: '↑',
  down: '↓',
  stable: '→',
}

function MetricCard({ metricType, latest, analytics }: MetricCardProps) {
  const unit = METRIC_UNITS[metricType]

  return (
    <div className="rounded-lg bg-white p-4 shadow">
      <h3 className="text-sm font-medium text-slate-500">{METRIC_LABELS[metricType]}</h3>
      {latest === null ? (
        <div className="mt-3">
          <EmptyState message="No entries yet." />
        </div>
      ) : (
        <>
          <p className="mt-1 text-2xl font-semibold text-slate-900">
            {latest.value} <span className="text-base font-normal text-slate-500">{unit}</span>
          </p>
          {analytics.avg_7d !== null && (
            <p className="mt-1 text-xs text-slate-500">
              7d avg: {analytics.avg_7d.toFixed(1)} {unit}
            </p>
          )}
          {analytics.trend !== null && (
            <p className="mt-1 text-xs text-slate-500">
              {TREND_ARROWS[analytics.trend.direction]} {analytics.trend.pct_change}%
            </p>
          )}
        </>
      )}
    </div>
  )
}

export default MetricCard
