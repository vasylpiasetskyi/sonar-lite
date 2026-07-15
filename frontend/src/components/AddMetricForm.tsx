import { useForm } from 'react-hook-form'

import { useCreateMetric } from '../api/metrics'
import { METRIC_LABELS, METRIC_TYPES } from '../api/types'
import type { MetricCreateInput } from '../api/types'
import ErrorState from './ErrorState'

function toDatetimeLocalNow(): string {
  const now = new Date()
  now.setSeconds(0, 0)
  return now.toISOString().slice(0, 16)
}

function AddMetricForm() {
  const { register, handleSubmit, reset, formState } = useForm<MetricCreateInput>({
    defaultValues: {
      metric_type: 'weight',
      value: 0,
      recorded_at: toDatetimeLocalNow(),
    },
  })
  const createMetric = useCreateMetric()

  const onSubmit = handleSubmit((values) => {
    createMetric.mutate(
      { ...values, recorded_at: new Date(values.recorded_at).toISOString() },
      { onSuccess: () => reset({ ...values, value: 0 }) },
    )
  })

  return (
    <form onSubmit={onSubmit} className="rounded-lg bg-white p-4 shadow">
      <h3 className="mb-3 text-sm font-medium text-slate-500">Add metric</h3>
      <div className="flex flex-wrap items-end gap-3">
        <label className="flex flex-col text-xs text-slate-500">
          Type
          <select
            className="mt-1 rounded border border-slate-300 p-2 text-sm"
            {...register('metric_type', { required: true })}
          >
            {METRIC_TYPES.map((type) => (
              <option key={type} value={type}>
                {METRIC_LABELS[type]}
              </option>
            ))}
          </select>
        </label>
        <label className="flex flex-col text-xs text-slate-500">
          Value
          <input
            type="number"
            step="any"
            className="mt-1 rounded border border-slate-300 p-2 text-sm"
            {...register('value', { required: true, valueAsNumber: true, min: 0.01 })}
          />
        </label>
        <label className="flex flex-col text-xs text-slate-500">
          Recorded at
          <input
            type="datetime-local"
            className="mt-1 rounded border border-slate-300 p-2 text-sm"
            {...register('recorded_at', { required: true })}
          />
        </label>
        <button
          type="submit"
          disabled={formState.isSubmitting}
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
        >
          Add
        </button>
      </div>
      {createMetric.isError && (
        <div className="mt-3">
          <ErrorState message="Could not save this metric. Please try again." />
        </div>
      )}
    </form>
  )
}

export default AddMetricForm
