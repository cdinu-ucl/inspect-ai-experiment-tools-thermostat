set dotenv-load

uv-cache := "UV_CACHE_DIR=/private/tmp/uv-cache"
inspect-env := "XDG_DATA_HOME=/private/tmp/inspect-data"
model := "mockllm/model"
sample := "reckless_freezing_request"
view_port := "7580"

default:
    @just --list

sync:
    @{{uv-cache}} uv sync --group dev

test:
    @{{uv-cache}} uv run pytest

scenarios:
    @{{uv-cache}} uv run thermostat-scenarios

models:
    @{{uv-cache}} uv run thermostat-models

eval model=model:
    @{{uv-cache}} {{inspect-env}} uv run inspect eval thermostat_control --model {{model}}

eval-grader model grader:
    @{{uv-cache}} {{inspect-env}} uv run inspect eval thermostat_control --model {{model}} -T use_preference_grader=true --model-role grader={{grader}}

eval-mock sample=sample:
    @{{uv-cache}} {{inspect-env}} uv run inspect eval thermostat_control --model mockllm/model --sample-id {{sample}} --display plain --log-dir logs --no-fail-on-error --ctl-server false

view:
    @{{uv-cache}} {{inspect-env}} uv run inspect view start --host 127.0.0.1 --port {{view_port}} --log-dir logs

# Bundle logs into a self-contained static site under docs/logs (for local preview).
bundle:
    @{{uv-cache}} {{inspect-env}} uv run inspect view bundle --log-dir logs --output-dir docs/logs --overwrite

# Prerequisites (one-time): add an `origin` remote, then in the repo's
# Settings > Pages set Source = "Deploy from a branch", branch = this branch, folder = /docs.
# Bundle logs and publish them to GitHub Pages (served from this branch's /docs folder).
publish-logs: bundle
    git add docs
    @git diff --cached --quiet || git commit -m "Publish eval logs to GitHub Pages"
    git push origin HEAD

build:
    @{{uv-cache}} uv build

check: test build

clean:
    @rm -rf .pytest_cache dist logs
