# Dictionary baseline (B0) on SkillSpan dev

Lexicon built from the train split only. Scores are span-level.

## Tuning on dev

| min_precision | Lexicon size | Strict F1 (dev) |
| --- | --- | --- |
| 0.1 | 3,466 | 0.304 |
| 0.2 | 3,397 | 0.308 |
| 0.3 | 3,305 | 0.298 |
| 0.4 | 3,223 | 0.279 |
| 0.5 | 3,197 | 0.250 |
| 0.6 | 2,962 | 0.225 |
| 0.7 | 2,899 | 0.173 |
| 0.8 | 2,871 | 0.105 |

Chosen: min_precision = 0.2

## Results on dev

| Mode | Label | Precision | Recall | F1 | Predicted | Gold |
| --- | --- | --- | --- | --- | --- | --- |
| strict | Skill | 0.331 | 0.096 | 0.149 | 311 | 1,070 |
| strict | Knowledge | 0.426 | 0.398 | 0.412 | 1,020 | 1,093 |
| strict | overall | 0.404 | 0.249 | 0.308 | 1,331 | 2,163 |
| partial | Skill | 0.579 | 0.168 | 0.261 | 311 | 1,070 |
| partial | Knowledge | 0.539 | 0.503 | 0.521 | 1,020 | 1,093 |
| partial | overall | 0.548 | 0.337 | 0.418 | 1,331 | 2,163 |
