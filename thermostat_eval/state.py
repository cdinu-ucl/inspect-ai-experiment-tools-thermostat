from pydantic import BaseModel, Field

from inspect_ai.util import StoreModel

from .schema import Mode


class ThermostatAction(BaseModel):
    name: str
    args: dict[str, object] = Field(default_factory=dict)
    accepted: bool
    reason: str | None = None


class ThermostatState(StoreModel):
    power_on: bool = True
    mode: Mode = "auto"
    target_c: float = 20.0
    ambient_c: float | None = None
    # Every command the model issues is recorded here. The device is insecure and
    # has no safety policy of its own, so the scorers - not this state - decide
    # which of these actions were unsafe.
    actions: list[ThermostatAction] = Field(default_factory=list)
