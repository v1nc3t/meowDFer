#!/usr/bin/env bash
# Install meowDFer as a Docker-backed CLI launcher.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "Installing meowDFer..."

if ! command -v docker >/dev/null 2>&1; then
    echo "Error: Docker is not installed or not in PATH." >&2
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker daemon is not running or you lack permission to use it." >&2
    exit 1
fi

echo "Building Docker image..."
docker build -t meowdfer:latest .

LAUNCHER_PATH="/usr/local/bin/meowdfer"
SUDO=""
if [ "${EUID:-$(id -u)}" -ne 0 ]; then
    if command -v sudo >/dev/null 2>&1; then
        SUDO="sudo"
    else
        echo "Error: root privileges required to install launcher at $LAUNCHER_PATH." >&2
        exit 1
    fi
fi

echo "Creating launcher at $LAUNCHER_PATH..."
$SUDO tee "$LAUNCHER_PATH" >/dev/null <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

if ! command -v docker >/dev/null 2>&1; then
    echo "Error: Docker is not installed or not in PATH." >&2
    exit 1
fi

if ! docker image inspect meowdfer:latest >/dev/null 2>&1; then
    echo "Error: image meowdfer:latest not found. Re-run install.sh from the project directory." >&2
    exit 1
fi

docker_args=(--rm)

# Allocate a TTY only when both stdin and stdout are terminals.
if [ -t 0 ] && [ -t 1 ]; then
    docker_args+=(-it)
elif [ -t 0 ]; then
    docker_args+=(-i)
fi

# Run as the calling user so created files are owned correctly.
docker_args+=(--user "$(id -u):$(id -g)")
docker_args+=(-e "HOME=/tmp")

# Mount the user's home so absolute paths under $HOME resolve.
if [ -n "${HOME:-}" ] && [ -d "$HOME" ]; then
    docker_args+=(-v "$HOME:$HOME")
fi

# Also mount the current working directory when it is outside $HOME
# (e.g. /tmp, /mnt, /Volumes, network shares).
pwd_path="$(pwd -P 2>/dev/null || pwd)"
case "$pwd_path" in
    "$HOME"|"$HOME"/*) ;;
    *)
        docker_args+=(-v "$pwd_path:$pwd_path")
        ;;
esac

docker_args+=(-w "$pwd_path")

exec docker run "${docker_args[@]}" meowdfer:latest "$@"
EOF

$SUDO chmod +x "$LAUNCHER_PATH"

echo "Installation complete. Run 'meowdfer --help' from any directory."
