export type MetricType = 'weight' | 'sleep' | 'heart_rate' | 'steps' | 'water'

export interface Metric {
  id: string
  user_id: string
  metric_type: MetricType
  value: number
  recorded_at: string
  created_at: string
  updated_at: string
}

export interface MetricList {
  items: Metric[]
  total: number
}

export interface MetricCreateInput {
  metric_type: MetricType
  value: number
  recorded_at: string
}

export interface Trend {
  direction: 'up' | 'down' | 'stable'
  pct_change: number
}

export interface MetricAnalytics {
  avg_7d: number | null
  avg_30d: number | null
  trend: Trend | null
}

export interface LatestReading {
  value: number
  recorded_at: string
}

export interface DashboardResponse {
  latest: Record<MetricType, LatestReading | null>
  metrics: Record<MetricType, MetricAnalytics>
  health_score: number | null
  ai_summary: null
}

export interface Recommendation {
  metric_type: MetricType
  message: string
}

export interface AISummary {
  summary: string
  positive_observations: string[]
  risks: string[]
  recommendations: string[]
  next_week_focus: string
  disclaimer: string
}

export interface AISummaryResponse {
  rule_based_recommendations: Recommendation[]
  ai_summary: AISummary | null
  ai_summary_error: string | null
}

export const METRIC_TYPES: MetricType[] = ['weight', 'sleep', 'heart_rate', 'steps', 'water']

export const METRIC_LABELS: Record<MetricType, string> = {
  weight: 'Weight',
  sleep: 'Sleep',
  heart_rate: 'Heart Rate',
  steps: 'Steps',
  water: 'Water',
}

export const METRIC_UNITS: Record<MetricType, string> = {
  weight: 'kg',
  sleep: 'h',
  heart_rate: 'bpm',
  steps: 'steps',
  water: 'L',
}

export interface UserRead {
  id: string
  email: string
  created_at: string
}

export interface AuthResponse {
  user: UserRead
  access_token: string
  token_type: string
}
