from __future__ import annotations

from airflow.core.constants import METERS_PER_FOOT

#
# Room
#

ROOM_LENGTH = 100.0
ROOM_WIDTH = 100.0
ROOM_HEIGHT = 8.0

#
# Fan
#

FAN_DIAMETER = 8 * METERS_PER_FOOT
FAN_RADIUS = FAN_DIAMETER / 2

FAN_RPM = 250

FAN_CENTER = (
    ROOM_LENGTH / 2,
    ROOM_WIDTH / 2,
    ROOM_HEIGHT - 0.4,
)

#
# Simulation
#

TIME_STEP = 1 / 60

PARTICLE_COUNT = 1500

PARTICLE_SIZE = 4

PARTICLE_LIFETIME = 6.0

#
# Future
#

ENABLE_TURBULENCE = False

ENABLE_PRESSURE = False

ENABLE_TEMPERATURE = False