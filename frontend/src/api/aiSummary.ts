import { useMutation } from '@tanstack/react-query'

import { apiPost } from './client'
import type { AISummaryResponse } from './types'

export function useGenerateAiSummary() {
  return useMutation({
    mutationFn: () => apiPost<AISummaryResponse>('/ai/summary'),
  })
}
