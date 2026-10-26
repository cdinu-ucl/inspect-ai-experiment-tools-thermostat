import json
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.table import Table


@dataclass(frozen=True)
class ModelGroup:
    name: str
    description: str
    models: tuple[str, ...]


# Cached `/v1/models` response from the UCL Condenser; refresh with `just ucl-models`.
UCL_CONDENSER_MODELS_CACHE = Path(__file__).with_name("ucl_condenser_models.json")


def ucl_condenser_models(cache: Path = UCL_CONDENSER_MODELS_CACHE) -> tuple[str, ...]:
    try:
        data = json.loads(cache.read_text())["data"]
    except (OSError, ValueError, KeyError):
        return ()
    return tuple(f"openai-api/ucl_condenser/{model['id']}" for model in data)


MODEL_GROUPS = (
    ModelGroup(
        name="Direct providers",
        description="Provider-native Inspect model identifiers.",
        models=(
            "anthropic/claude-sonnet-4-5",
            "mistral/mistral-medium-3-5",
        ),
    ),
    ModelGroup(
        name="OpenRouter",
        description="Models routed through the OpenRouter provider.",
        models=(
            "openrouter/free",
            "openrouter/deepseek/deepseek-v4-flash",
            "openrouter/xiaomi/mimo-v2.5",
            "openrouter/tencent/hy3-preview",
            "openrouter/x-ai/grok-4.3",
        ),
    ),
    ModelGroup(
        name="UCL Condenser",
        description="OpenAI-compatible UCL ARC endpoint; set UCL_CONDENSER_* in .env. "
        "Run `just ucl-models` to refresh this list.",
        models=ucl_condenser_models() or ("openai-api/ucl_condenser/<model-name>",),
    ),
    ModelGroup(
        name="Local smoke test",
        description="No API credentials required; useful for plumbing checks.",
        models=("mockllm/model",),
    ),
)


def main() -> None:
    table = Table(title="Thermostat Eval Starting Models")
    table.add_column("Group", style="cyan", no_wrap=True)
    table.add_column("Model", style="bold", overflow="fold")
    table.add_column("Notes", style="dim")

    for group in MODEL_GROUPS:
        for index, model in enumerate(group.models):
            table.add_row(
                group.name if index == 0 else "",
                model,
                group.description if index == 0 else "",
            )

    Console().print(table)
