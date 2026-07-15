import { clearAuthToken } from '../api/client'
import { useDashboard } from '../api/metrics'
import { METRIC_TYPES } from '../api/types'
import AddMetricForm from '../components/AddMetricForm'
import AiSummaryPanel from '../components/AiSummaryPanel'
import ErrorState from '../components/ErrorState'
import HealthScoreCard from '../components/HealthScoreCard'
import LoadingState from '../components/LoadingState'
import MetricCard from '../components/MetricCard'
import MetricTrendChart from '../components/MetricTrendChart'

interface DashboardPageProps {
  onLogout: () => void
}

function DashboardPage({ onLogout }: DashboardPageProps) {
  const { data, isLoading, isError } = useDashboard()

  if (isLoading) {
    return <LoadingState label="Loading your dashboard..." />
  }

  if (isError || !data) {
    return <ErrorState message="Could not load the dashboard. Please try again." />
  }

  return (
    <div className="mx-auto max-w-5xl space-y-6 p-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-slate-900">Sonar Lite</h1>
          <p className="text-sm text-slate-500">Your health, at a glance.</p>
        </div>
        <button
          type="button"
          onClick={() => {
            clearAuthToken()
            onLogout()
          }}
          className="rounded border border-slate-300 px-3 py-1.5 text-sm text-slate-600"
        >
          Log out
        </button>
      </header>

      <HealthScoreCard healthScore={data.health_score} />

      <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
        {METRIC_TYPES.map((type) => (
          <MetricCard
            key={type}
            metricType={type}
            latest={data.latest[type]}
            analytics={data.metrics[type]}
          />
        ))}
      </section>

      <AddMetricForm />

      <section className="grid grid-cols-1 gap-4 lg:grid-cols-2">
        {METRIC_TYPES.map((type) => (
          <MetricTrendChart key={type} metricType={type} />
        ))}
      </section>

      <AiSummaryPanel />
    </div>
  )
}

export default DashboardPage
