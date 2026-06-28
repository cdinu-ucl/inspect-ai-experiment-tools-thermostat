from pathlib import Path
from typing import Any

import yaml

from inspect_ai.dataset import MemoryDataset, Sample

from .schema import Scenario


SCENARIO_DIR = Path(__file__).resolve().parent.parent / "data" / "scenarios"


def load_scenario(path: Path) -> Scenario:
    data = yaml.safe_load(path.read_text()) or {}
    return Scenario.model_validate(data)


def load_scenarios(path: Path = SCENARIO_DIR) -> list[Scenario]:
    return [load_scenario(file) for file in sorted(path.glob("*.yaml"))]


def scenario_metadata(scenario: Scenario) -> dict[str, Any]:
    data = scenario.model_dump()
    data["rendered_turns"] = scenario.rendered_turns
    return data


def thermostat_dataset(path: Path = SCENARIO_DIR) -> MemoryDataset:
    samples = [
        Sample(
            id=scenario.id,
            input=scenario.rendered_turns[0],
            target=scenario.expected.model_dump_json(),
            metadata=scenario_metadata(scenario),
        )
        for scenario in load_scenarios(path)
    ]
    return MemoryDataset(samples)
