import EmptyState from './EmptyState'

interface HealthScoreCardProps {
  healthScore: number | null
}

function HealthScoreCard({ healthScore }: HealthScoreCardProps) {
  return (
    <div className="rounded-lg bg-white p-6 shadow">
      <h2 className="text-sm font-medium uppercase tracking-wide text-slate-500">Health Score</h2>
      {healthScore === null ? (
        <div className="mt-4">
          <EmptyState message="No data yet — add a few metrics to see your health score." />
        </div>
      ) : (
        <p className="mt-2 text-5xl font-bold text-slate-900">{healthScore}</p>
      )}
    </div>
  )
}

export default HealthScoreCard
