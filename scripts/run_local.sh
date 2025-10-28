set -euo pipefail
export PYTHONUNBUFFERED=1

python -m sqlmap_agent.run "$@"
