from __future__ import annotations

import logging
import threading
import typing
from dataclasses import dataclass, field
from typing import Optional

import numpy as np
from adaptive_milling.config import AdaptivePolishMillingConfig
from adaptive_milling.strategy import AdaptivePolishMillingStrategy
from fibsem.milling.properties import DEFAULT_ANGLE_METADATA
from fibsem.structures import FibsemStagePosition, field_meta

if typing.TYPE_CHECKING:
    from fibsem.microscope import FibsemMicroscope
    from fibsem.milling import FibsemMillingStage

_logger = logging.getLogger(__name__)


@dataclass
class NilasMillingConfig(AdaptivePolishMillingConfig):
    stage_tilt_offset: float = field(
        default=0.0,
        metadata=field_meta(
            DEFAULT_ANGLE_METADATA,
            label="Stage tilt offset",
            minimum=-60.0,
            maximum=60.0,
            step=0.5,
            tooltip="Tilt the stage by this many degrees (relative to the current "
            "tilt) before polishing. The original position is restored afterwards.",
        ),
    )
    stage_rotation_offset: float = field(
        default=0.0,
        metadata=field_meta(
            DEFAULT_ANGLE_METADATA,
            label="Stage rotation offset",
            minimum=-180.0,
            maximum=180.0,
            step=1.0,
            tooltip="Rotate the stage by this many degrees (relative to the current "
            "rotation) before polishing. The original position is restored afterwards.",
        ),
    )


class NilasMillingStrategy(AdaptivePolishMillingStrategy):
    """Adaptive polishing with a relative stage tilt and/or rotation.

    Inherits all AdaptivePolishing behaviour (ML-driven thickness feedback,
    stopping conditions, output plots). Before polishing, the stage is moved
    by the configured tilt/rotation offsets; the original stage position is
    restored when polishing finishes, even if it fails or is cancelled.
    """

    name: str = "Nilas"
    fullname: str = "Adaptive polishing at a stage tilt/rotation offset"
    config_class: type[NilasMillingConfig] = NilasMillingConfig

    def run(
        self,
        microscope: FibsemMicroscope,
        stage: FibsemMillingStage,
        asynch: bool = False,
        parent_ui=None,
        stop_event: Optional[threading.Event] = None,
    ) -> None:
        tilt_deg = self.config.stage_tilt_offset
        rotation_deg = self.config.stage_rotation_offset

        if not tilt_deg and not rotation_deg:
            super().run(
                microscope,
                stage,
                asynch=asynch,
                parent_ui=parent_ui,
                stop_event=stop_event,
            )
            return

        initial_position = microscope.get_stage_position()
        try:
            _logger.info(
                "%s: offsetting stage by tilt %.2f°, rotation %.2f°",
                self.name,
                tilt_deg,
                rotation_deg,
            )
            microscope.move_stage_relative(
                FibsemStagePosition(
                    t=np.deg2rad(tilt_deg) if tilt_deg else None,
                    r=np.deg2rad(rotation_deg) if rotation_deg else None,
                )
            )
            super().run(
                microscope,
                stage,
                asynch=asynch,
                parent_ui=parent_ui,
                stop_event=stop_event,
            )
        finally:
            _logger.info("%s: restoring stage position %s", self.name, initial_position)
            microscope.move_stage_absolute(initial_position)
