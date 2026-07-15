import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'

import { apiGet, apiPost } from './client'
import type { DashboardResponse, Metric, MetricCreateInput, MetricList, MetricType } from './types'

export function useDashboard() {
  return useQuery({
    queryKey: ['dashboard'],
    queryFn: () => apiGet<DashboardResponse>('/dashboard'),
  })
}

export function useMetricHistory(metricType: MetricType, limit = 30) {
  return useQuery({
    queryKey: ['metric-history', metricType, limit],
    queryFn: () => apiGet<MetricList>(`/metrics?metric_type=${metricType}&limit=${limit}`),
  })
}

export function useCreateMetric() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (input: MetricCreateInput) => apiPost<Metric>('/metrics', input),
    onSuccess: (metric) => {
      queryClient.invalidateQueries({ queryKey: ['dashboard'] })
      queryClient.invalidateQueries({ queryKey: ['metric-history', metric.metric_type] })
    },
  })
}
