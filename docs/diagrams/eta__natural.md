# Natural Transformation

## Naturality on `0->1`

```mermaid
graph LR
  FX["F 0"] -->|F·0->1| FY["F 1"]
  FX -->|η 0| GX["G 0"]
  FY -->|η 1| GY["G 1"]
  GX -->|G·0->1| GY
```

## Naturality on `0->2`

```mermaid
graph LR
  FX["F 0"] -->|F·0->2| FY["F 2"]
  FX -->|η 0| GX["G 0"]
  FY -->|η 2| GY["G 2"]
  GX -->|G·0->2| GY
```

## Naturality on `0->3`

```mermaid
graph LR
  FX["F 0"] -->|F·0->3| FY["F 3"]
  FX -->|η 0| GX["G 0"]
  FY -->|η 3| GY["G 3"]
  GX -->|G·0->3| GY
```

## Naturality on `1->2`

```mermaid
graph LR
  FX["F 1"] -->|F·1->2| FY["F 2"]
  FX -->|η 1| GX["G 1"]
  FY -->|η 2| GY["G 2"]
  GX -->|G·1->2| GY
```

## Naturality on `1->3`

```mermaid
graph LR
  FX["F 1"] -->|F·1->3| FY["F 3"]
  FX -->|η 1| GX["G 1"]
  FY -->|η 3| GY["G 3"]
  GX -->|G·1->3| GY
```

## Naturality on `2->3`

```mermaid
graph LR
  FX["F 2"] -->|F·2->3| FY["F 3"]
  FX -->|η 2| GX["G 2"]
  FY -->|η 3| GY["G 3"]
  GX -->|G·2->3| GY
```

## Naturality on `id:0`

```mermaid
graph LR
  FX["F 0"] -->|F·id:0| FY["F 0"]
  FX -->|η 0| GX["G 0"]
  FY -->|η 0| GY["G 0"]
  GX -->|G·id:0| GY
```

## Naturality on `id:1`

```mermaid
graph LR
  FX["F 1"] -->|F·id:1| FY["F 1"]
  FX -->|η 1| GX["G 1"]
  FY -->|η 1| GY["G 1"]
  GX -->|G·id:1| GY
```

## Naturality on `id:2`

```mermaid
graph LR
  FX["F 2"] -->|F·id:2| FY["F 2"]
  FX -->|η 2| GX["G 2"]
  FY -->|η 2| GY["G 2"]
  GX -->|G·id:2| GY
```

## Naturality on `id:3`

```mermaid
graph LR
  FX["F 3"] -->|F·id:3| FY["F 3"]
  FX -->|η 3| GX["G 3"]
  FY -->|η 3| GY["G 3"]
  GX -->|G·id:3| GY
```