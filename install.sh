#!/usr/bin/env bash
set -euo pipefail

echo "Installing meowDFer..."

# 1. Check dependencies
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH." >&2
    exit 1
fi

# 2. Build the Docker image
echo "Building Docker container..."
docker build -t meowdfer:latest .

# 3. Target install directory & determine privilege requirements
LAUNCHER_PATH="/usr/local/bin/meowdfer"

SUDO=""
if [ "$EUID" -ne 0 ]; then
    SUDO="sudo"
fi

echo "Creating global launcher at $LAUNCHER_PATH..."

# 4. Write the launcher script
$SUDO bash -c "cat << 'EOF' > $LAUNCHER_PATH
#!/usr/bin/env bash
set -e

# Detect if stdin/stdout are attached to a terminal (TTY)
TTY_ARGS=\"\"
if [ -t 0 ] && [ -t 1 ]; then
    TTY_ARGS=\"-it\"
fi

# Mount host storage paths into container so host paths resolve naturally
exec docker run --rm \$TTY_ARGS \\
    --user \"\$(id -u):\$(id -g)\" \\
    -v \"/home:/home\" \\
    -v \"/tmp:/tmp\" \\
    -v \"\$(pwd):\$(pwd)\" \\
    -w \"\$(pwd)\" \\
    meowdfer:latest \"\$@\"
EOF"

$SUDO chmod +x "$LAUNCHER_PATH"

echo "Installation complete! You can now run 'meowdfer' from any folder."