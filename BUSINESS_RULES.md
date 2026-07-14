# Sonar Lite — Business Rules

## Metrics tracked

- Weight (kg)
- Sleep duration (hours)
- Resting heart rate (bpm)
- Daily steps
- Water intake (liters)

Future/optional: Mood (1-5), Stress level, Blood pressure.

## Threshold rules

Ranges are continuous — every value falls into exactly one bucket.

**Sleep (hours/night)**
| Range | Status |
|---|---|
| `< 6` | warning (too little) |
| `6 – 9` | good |
| `> 9` | notice (possible oversleep) |

**Resting heart rate (bpm)**
| Range | Status |
|---|---|
| `< 45` | critical |
| `45 – 59` | low |
| `60 – 100` | normal |
| `> 100` | warning |

**Water intake (liters/day)**
| Range | Status |
|---|---|
| `< 1.5` | low |
| `1.5 – 3` | normal |
| `> 3` | notice |

**Daily steps**
| Range | Status |
|---|---|
| `< 5000` | low activity |
| `5000 – 10000` | normal |
| `> 10000` | high activity |

**Weight**

No fixed threshold. Evaluated as a trend over 7-day and 30-day windows. A change greater than 3% within a week is flagged for review.

## Health Score

A single 0–100 score, weighted sum of sub-scores:

| Component | Weight |
|---|---|
| Sleep quality | 30% |
| Activity (steps) | 25% |
| Heart rate | 20% |
| Weight trend stability | 15% |
| Water intake | 10% |

Weights sum to 100%. Exact sub-score formulas are an implementation detail decided during Sprint 2/3 — this document fixes only the weights and inputs.

## Rule-based recommendations

Evaluated before any AI call. AI enhances these — it never replaces them.

| Condition | Recommendation |
|---|---|
| Sleep < 6h | Improve sleep hygiene / schedule |
| Resting heart rate > 100 | Recommend consulting a healthcare professional |
| Water intake < 1.5L | Increase hydration |
| Daily steps < 5000 | Increase daily activity |
| Weight change > 3% in a week | Monitor nutrition, flag for attention |

## AI Summary

On demand ("Generate AI Summary"), the backend aggregates structured stats (7d/30d averages, trends) and asks the LLM for: short summary, positive observations, possible risks, personalized recommendations, next week's focus.

The response is always structured JSON and always carries this disclaimer: **recommendations are informational only, not medical advice.**
