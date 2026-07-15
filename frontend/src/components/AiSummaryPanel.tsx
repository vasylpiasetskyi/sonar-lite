import { useGenerateAiSummary } from '../api/aiSummary'
import { METRIC_LABELS } from '../api/types'
import ErrorState from './ErrorState'
import LoadingState from './LoadingState'

function AiSummaryPanel() {
  const generateSummary = useGenerateAiSummary()

  return (
    <div className="rounded-lg bg-white p-4 shadow">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-slate-500">AI Summary &amp; Recommendations</h3>
        <button
          type="button"
          onClick={() => generateSummary.mutate()}
          disabled={generateSummary.isPending}
          className="rounded bg-emerald-600 px-3 py-1.5 text-sm font-medium text-white disabled:opacity-50"
        >
          {generateSummary.isPending ? 'Generating...' : 'Generate AI Summary'}
        </button>
      </div>

      {generateSummary.isPending && (
        <div className="mt-3">
          <LoadingState label="Asking the AI for a summary..." />
        </div>
      )}

      {generateSummary.isError && (
        <div className="mt-3">
          <ErrorState message="Could not reach the server. Please try again." />
        </div>
      )}

      {generateSummary.data && (
        <div className="mt-4 space-y-4">
          {generateSummary.data.rule_based_recommendations.length > 0 && (
            <div>
              <h4 className="text-xs font-semibold uppercase text-slate-400">
                Rule-based recommendations
              </h4>
              <ul className="mt-1 list-inside list-disc text-sm text-slate-700">
                {generateSummary.data.rule_based_recommendations.map((rec, index) => (
                  <li key={index}>
                    <span className="font-medium">{METRIC_LABELS[rec.metric_type]}:</span>{' '}
                    {rec.message}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {generateSummary.data.ai_summary && (
            <div className="space-y-2 text-sm text-slate-700">
              <p>{generateSummary.data.ai_summary.summary}</p>
              <p className="text-xs italic text-slate-400">
                {generateSummary.data.ai_summary.disclaimer}
              </p>
            </div>
          )}

          {generateSummary.data.ai_summary_error && (
            <ErrorState message={generateSummary.data.ai_summary_error} />
          )}
        </div>
      )}
    </div>
  )
}

export default AiSummaryPanel
