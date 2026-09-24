# Nilas

A fibsemOS milling strategy plugin that extends [Adaptive Milling](https://github.com/rosalindfranklininstitute/adaptive_milling) with a configurable stage tilt, enabling adaptive polishing at low voltage and high tilt.

## What it does

Nilas wraps the `AdaptivePolishing` strategy and adds one parameter: `stage_tilt_deg`. Before each polishing run, it tilts the stage to the specified angle, then restores the original tilt when milling finishes (including on failure).

Everything else — the ML-driven thickness feedback, GIS stopping conditions, output plots — is inherited from `AdaptivePolishing` unchanged.

## Installation

```bash
pip install -e .
```

Then restart AutoLamella. Nilas will appear in the Strategy dropdown alongside AdaptivePolishing.

## Usage

In the AutoLamella protocol editor, add a Polishing stage and set its strategy to **Nilas**. You will see all the usual AdaptivePolishing settings plus:

| Setting | Default | Description |
|---|---|---|
| `stage_tilt_deg` | `0.0` | Stage tilt angle in degrees applied before milling. Original tilt is restored afterwards. |

## Requirements

- Python ≥ 3.9
- [adaptive-milling](https://github.com/rosalindfranklininstitute/adaptive_milling) ≥ 0.1.0 (which pulls in fibsem)
