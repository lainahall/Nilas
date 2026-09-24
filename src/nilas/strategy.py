from __future__ import annotations
from dataclasses import dataclass
from adaptive_milling.strategy import AdaptivePolishMillingStrategy
from fibsem.microscope import FibsemMicroscope
from fibsem.structures import FibsemMillingStage


@dataclass
class NilasMillingStrategy(AdaptivePolishMillingStrategy):
    """
    Adaptive polishing with a user-specified stage tilt.

    Inherits all AdaptivePolishing behaviour (ML-driven thickness feedback,
    stopping conditions, output plots) and adds one parameter:

        stage_tilt_deg  – tilt angle in degrees applied before milling starts.
                          The original tilt is restored when milling finishes,
                          even if milling fails.
    """

    stage_tilt_deg: float = 0.0  # degrees; shown in the UI alongside other settings

    def mill(
        self,
        microscope: FibsemMicroscope,
        stage: FibsemMillingStage,
        *args,
        **kwargs,
    ):
        # Record current tilt so we can restore it afterwards
        original_tilt = microscope.get_stage_position().t

        try:
            # Move to the requested tilt before milling
            if self.stage_tilt_deg != original_tilt:
                pos = microscope.get_stage_position()
                pos.t = self.stage_tilt_deg
                microscope.move_stage_absolute(pos)

            # Run the full AdaptivePolishing loop
            super().mill(microscope, stage, *args, **kwargs)

        finally:
            # Always restore the original tilt, even on failure
            pos = microscope.get_stage_position()
            pos.t = original_tilt
            microscope.move_stage_absolute(pos)
