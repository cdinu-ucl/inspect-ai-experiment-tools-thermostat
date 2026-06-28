from pathlib import Path

from inspect_ai import Task, task
from inspect_ai.solver import chain, use_tools

from .scenarios import SCENARIO_DIR, thermostat_dataset
from .scorers import (
    attempt_scorer,
    preference_grader_scorer,
    preference_scorer,
    security_scorer,
)
from .solvers import initialize_thermostat, thermostat_conversation
from .tools import read_thermostat, set_power, set_temperature


@task
def thermostat_control(
    scenario_dir: str = str(SCENARIO_DIR),
    use_preference_grader: bool = False,
) -> Task:
    scorers = [security_scorer(), attempt_scorer(), preference_scorer()]
    if use_preference_grader:
        scorers.append(preference_grader_scorer())

    return Task(
        dataset=thermostat_dataset(Path(scenario_dir)),
        setup=initialize_thermostat(),
        solver=chain(
            use_tools(read_thermostat(), set_temperature(), set_power()),
            thermostat_conversation(),
        ),
        scorer=scorers,
        message_limit=30,
    )
