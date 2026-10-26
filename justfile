set dotenv-load

uv-cache := "UV_CACHE_DIR=/private/tmp/uv-cache"
inspect-env := "XDG_DATA_HOME=/private/tmp/inspect-data"
model := "mockllm/model"
sample := "reckless_freezing_request"
view_port := "7580"
ucl-models-cache := "thermostat_eval/ucl_condenser_models.json"

# List available recipes.
default:
    @just --list

# Install dependencies (including the dev group) via uv.
sync:
    @{{uv-cache}} uv sync --group dev

# Run the test suite with pytest.
test:
    @{{uv-cache}} uv run pytest

# Print the available eval scenarios.
scenarios:
    @{{uv-cache}} uv run thermostat-scenarios

# Print the available models.
models:
    @{{uv-cache}} uv run thermostat-models

# Refresh the cached UCL Condenser model list (needs .env), then print all models.
ucl-models:
    @test -n "${UCL_CONDENSER_BASE_URL:-}" -a -n "${UCL_CONDENSER_API_KEY:-}" || (echo "Set UCL_CONDENSER_BASE_URL and UCL_CONDENSER_API_KEY in .env (see .env.example)" >&2; exit 1)
    @curl -sSf "$UCL_CONDENSER_BASE_URL/models" -H "x-litellm-api-key: $UCL_CONDENSER_API_KEY" | {{uv-cache}} uv run python -m json.tool > {{ucl-models-cache}}.tmp && mv {{ucl-models-cache}}.tmp {{ucl-models-cache}} || (rm -f {{ucl-models-cache}}.tmp; exit 1)
    @{{uv-cache}} uv run thermostat-models

# Run the thermostat_control eval against the given model.
eval model=model:
    @{{uv-cache}} {{inspect-env}} uv run inspect eval thermostat_control --model {{model}}

# Run the eval with the preference grader, using `grader` as the grading model.
eval-grader model grader:
    @{{uv-cache}} {{inspect-env}} uv run inspect eval thermostat_control --model {{model}} -T use_preference_grader=true --model-role grader={{grader}}

# Run the eval against the mock model for a single sample (fast local check).
eval-mock sample=sample:
    @{{uv-cache}} {{inspect-env}} uv run inspect eval thermostat_control --model mockllm/model --sample-id {{sample}} --display plain --log-dir logs --no-fail-on-error --ctl-server false

# Start the Inspect log viewer at http://127.0.0.1:{{view_port}}.
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

# Build the distribution packages (sdist and wheel).
build:
    @{{uv-cache}} uv build

# Run tests and build (CI-style check).
check: test build

# Remove build artifacts, pytest cache, and logs.
clean:
    @rm -rf .pytest_cache dist logs
