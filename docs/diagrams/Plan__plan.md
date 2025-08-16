# Plan

```mermaid
graph LR
  in["⟦input⟧"]
  s1["denoise"]
  s2["edges"]
  s3["segment"]
  s4["merge"]
  out["⟦output⟧"]
  in --> s1
  s1 --> s2
  s2 --> s3
  s3 --> s4
  s4 --> out
```