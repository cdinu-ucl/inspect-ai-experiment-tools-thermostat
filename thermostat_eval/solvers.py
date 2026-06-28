from inspect_ai.model import ChatMessageUser
from inspect_ai.solver import Generate, Solver, TaskState, solver

from .schema import Scenario
from .state import ThermostatState


@solver
def initialize_thermostat() -> Solver:
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        scenario = state.metadata_as(Scenario)
        thermostat = state.store_as(ThermostatState)
        thermostat.power_on = scenario.initial_state.power_on
        thermostat.mode = scenario.initial_state.mode
        thermostat.target_c = scenario.initial_state.target_c
        thermostat.ambient_c = scenario.initial_state.ambient_c
        thermostat.actions.clear()
        return state

    return solve


@solver
def thermostat_conversation() -> Solver:
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        scenario = state.metadata_as(Scenario)

        for index, turn in enumerate(scenario.rendered_turns):
            if index > 0:
                state.messages.append(ChatMessageUser(content=turn))
            state = await generate(state, tool_calls="loop")

        return state

    return solve
