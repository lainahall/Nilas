# Nilas

A fibsemOS milling strategy plugin that extends [Adaptive Milling](https://github.com/rosalindfranklininstitute/adaptive_milling) with a configurable stage tilt and rotation, enabling adaptive polishing at low voltage and high tilt.

## What it does

Nilas wraps the `AdaptivePolishing` strategy and adds two parameters: a stage tilt offset and a stage rotation offset. Before each polishing run, it moves the stage by those offsets (relative to where it currently is), then restores the original stage position when milling finishes (including on failure or cancellation).

Everything else — the ML-driven thickness feedback, GIS stopping conditions, output plots — is inherited from `AdaptivePolishing` unchanged. Milling voltage is set per stage as usual.

## Installation

```bash
pip install -e .
```

Then restart AutoLamella. Nilas will appear in the Strategy dropdown alongside AdaptivePolishing.

## Usage

In the AutoLamella protocol editor, add a Polishing stage and set its strategy to **Nilas**. You will see all the usual AdaptivePolishing settings plus:

| Setting | Default | Description |
|---|---|---|
| `stage_tilt_offset` | `0.0` | Degrees to tilt the stage, relative to its current tilt, before polishing. |
| `stage_rotation_offset` | `0.0` | Degrees to rotate the stage, relative to its current rotation, before polishing. |

With both offsets at `0`, Nilas behaves exactly like AdaptivePolishing and does not move the stage.

**Note:** tilting or rotating after milling setup moves the lamella relative to the FIB patterns and alignment reference. Keep offsets small and work at eucentric height; large rotations will usually move the lamella out of the field of view.

## Requirements

- Python ≥ 3.9
- [adaptive-milling](https://github.com/rosalindfranklininstitute/adaptive_milling) ≥ 0.4.0 (which pulls in fibsem)
