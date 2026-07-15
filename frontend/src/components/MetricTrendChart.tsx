import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

import { useMetricHistory } from '../api/metrics'
import { METRIC_LABELS } from '../api/types'
import type { MetricType } from '../api/types'
import EmptyState from './EmptyState'
import ErrorState from './ErrorState'
import LoadingState from './LoadingState'

interface MetricTrendChartProps {
  metricType: MetricType
}

function MetricTrendChart({ metricType }: MetricTrendChartProps) {
  const { data, isLoading, isError } = useMetricHistory(metricType)

  if (isLoading) {
    return <LoadingState label={`Loading ${METRIC_LABELS[metricType]} history...`} />
  }

  if (isError) {
    return <ErrorState message={`Could not load ${METRIC_LABELS[metricType]} history.`} />
  }

  if (!data || data.items.length === 0) {
    return <EmptyState message="No data yet — add your first entry to see a trend." />
  }

  const chartData = [...data.items]
    .sort((a, b) => new Date(a.recorded_at).getTime() - new Date(b.recorded_at).getTime())
    .map((item) => ({
      recorded_at: new Date(item.recorded_at).toLocaleDateString(),
      value: item.value,
    }))

  return (
    <div className="rounded-lg bg-white p-4 shadow">
      <h3 className="mb-2 text-sm font-medium text-slate-500">
        {METRIC_LABELS[metricType]} trend
      </h3>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="recorded_at" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip />
          <Line type="monotone" dataKey="value" stroke="#2563eb" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}

export default MetricTrendChart
