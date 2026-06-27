"""Airflow simulation components for AirFlowSim."""

__all__ = ["CeilingFan", "ParticleSystem"]


def __getattr__(name: str):
    if name == "CeilingFan":
        from .fan import CeilingFan

        return CeilingFan
    if name == "ParticleSystem":
        from .particle_system import ParticleSystem

        return ParticleSystem
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
