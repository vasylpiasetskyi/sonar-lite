from app.models.metric import MetricType
from app.schemas.dashboard import MetricAnalytics
from app.schemas.recommendation import Recommendation

SUMMARY_PROMPT_TEMPLATE = """You are a health data assistant. Based on the user's recent metrics \
and the rule-based flags already raised, write a short, encouraging, non-alarmist summary.

Recent metrics (7-day averages and trend vs. the prior 7 days):
{metrics_section}

Rule-based flags already raised (do not contradict these; build on them):
{recommendations_section}

Respond with ONLY a JSON object with exactly these keys: "summary" (string), \
"positive_observations" (array of strings), "risks" (array of strings), \
"recommendations" (array of strings), "next_week_focus" (string). \
Do not include a medical disclaimer - that is added separately."""


def build_summary_prompt(
    metrics: dict[MetricType, MetricAnalytics], recommendations: list[Recommendation]
) -> str:
    metrics_lines = []
    for metric_type, analytics in metrics.items():
        trend_text = (
            f"{analytics.trend.direction} ({analytics.trend.pct_change}%)"
            if analytics.trend is not None
            else "no trend data"
        )
        metrics_lines.append(
            f"- {metric_type.value}: avg_7d={analytics.avg_7d}, "
            f"avg_30d={analytics.avg_30d}, trend={trend_text}"
        )
    metrics_section = "\n".join(metrics_lines) if metrics_lines else "No data recorded yet."

    if recommendations:
        recommendations_section = "\n".join(
            f"- {rec.metric_type.value}: {rec.message}" for rec in recommendations
        )
    else:
        recommendations_section = "None."

    return SUMMARY_PROMPT_TEMPLATE.format(
        metrics_section=metrics_section, recommendations_section=recommendations_section
    )
