# Cross-model matrix comparison
Matrix: {Groq, OpenAI} × {baseline, stem agent} × {sample_advanced_clean.py, sample.cpp} — 5 runs each (40 total)

## Per-combination results

### Groq (llama-3.3-70b-versatile) / baseline / sample_advanced_clean.py

```
Run  Comments   High   Med    Low
---------------------------------
1    6          3      2      0
2    6          3      2      0
3    6          3      2      0
4    6          3      2      0
5    6          3      2      0
```

### Groq (llama-3.3-70b-versatile) / baseline / sample.cpp

```
Run  Comments   High   Med    Low
---------------------------------
1    6          4      2      0
2    6          4      2      0
3    6          4      2      0
4    6          4      1      1
5    6          4      2      0
```

### Groq (llama-3.3-70b-versatile) / stem agent / sample_advanced_clean.py

```
Run  Comments   High   Med    Low    Score   Refines
----------------------------------------------------
1    10         4      4      2      9.0     0
2    7          3      3      1      9.0     0
3    8          4      2      2      9.0     0
4    10         3      4      3      9.0     0
5    9          4      3      1      9.0     0
```

### Groq (llama-3.3-70b-versatile) / stem agent / sample.cpp

```
Run  Comments   High   Med    Low    Score   Refines
----------------------------------------------------
1    6          5      1      0      9.5     0
2    9          6      2      1      9.0     0
3    10         7      3      0      9.0     0
4    8          6      2      0      9.0     0
5    9          5      3      1      9.0     0
```

### OpenAI (gpt-4o-mini) / baseline / sample_advanced_clean.py

```
Run  Comments   High   Med    Low
---------------------------------
1    5          3      2      0
2    4          3      1      0
3    4          3      1      0
4    4          3      1      0
5    5          3      2      0
```

### OpenAI (gpt-4o-mini) / baseline / sample.cpp

```
Run  Comments   High   Med    Low
---------------------------------
1    6          5      1      0
2    6          5      0      0
3    6          5      1      0
4    6          5      1      0
5    6          5      1      1
```

### OpenAI (gpt-4o-mini) / stem agent / sample_advanced_clean.py

```
Run  Comments   High   Med    Low    Score   Refines
----------------------------------------------------
1    3          3      0      0      9.0     0
2    4          4      0      0      9.0     0
3    4          3      1      0      9.0     0
4    4          3      1      0      9.0     0
5    4          3      1      0      9.0     0
```

### OpenAI (gpt-4o-mini) / stem agent / sample.cpp

```
Run  Comments   High   Med    Low    Score   Refines
----------------------------------------------------
1    6          5      1      1      9.0     0
2    6          5      1      0      9.0     0
3    6          5      1      0      9.0     0
4    5          4      2      0      9.0     0
5    5          3      2      0      9.0     0
```

## Summary matrix — mean ± stdev comments

```
                                                 sample_advanced_clean.py               sample.cpp          
------------------------------------------------------------------------------------------------------------
Groq (llama-3.3-70b-versatile) / baseline               6.0 ± 0.00                      6.0 ± 0.00          
Groq (llama-3.3-70b-versatile) / stem agent             8.8 ± 1.30                      8.4 ± 1.52          
OpenAI (gpt-4o-mini) / baseline                         4.4 ± 0.55                      6.0 ± 0.00          
OpenAI (gpt-4o-mini) / stem agent                       3.8 ± 0.45                      5.6 ± 0.55          
```

## Baseline → stem agent delta (mean comments)

### Groq (llama-3.3-70b-versatile) / sample_advanced_clean.py

```
Baseline:    6.0 ± 0.00 comments
Stem agent:  8.8 ± 1.30 comments
Delta:       +2.8
```

### Groq (llama-3.3-70b-versatile) / sample.cpp

```
Baseline:    6.0 ± 0.00 comments
Stem agent:  8.4 ± 1.52 comments
Delta:       +2.4
```

### OpenAI (gpt-4o-mini) / sample_advanced_clean.py

```
Baseline:    4.4 ± 0.55 comments
Stem agent:  3.8 ± 0.45 comments
Delta:       -0.6
```

### OpenAI (gpt-4o-mini) / sample.cpp

```
Baseline:    6.0 ± 0.00 comments
Stem agent:  5.6 ± 0.55 comments
Delta:       -0.4
```
