#!/usr/bin/env bash
set -e

echo "Installing meowDFer..."

# 1. Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed or not in PATH."
    exit 1
fi

# 2. Build the Docker container image
echo "Building Docker container..."
docker build -t meowdfer:latest .

# 3. Create the launcher script
LAUNCHER_PATH="/usr/local/bin/meowdfer"
echo "Creating global launcher at $LAUNCHER_PATH..."

# Safely check if we need sudo or if we are already root
SUDO=""
if [ "$EUID" -ne 0 ]; then
    SUDO="sudo"
fi

$SUDO bash -c "cat << 'EOF' > $LAUNCHER_PATH
#!/usr/bin/env bash
# Quoting \"\$(pwd)\" ensures paths with spaces don't break execution
docker run --rm -it \\
    --user \"\$(id -u):\$(id -g)\" \\
    -v \"\$(pwd):\$(pwd)\" \\
    -w \"\$(pwd)\" \\
    meowdfer:latest \"\$@\"
EOF"

# 4. Make launcher executable
$SUDO chmod +x $LAUNCHER_PATH

echo "Installation complete! You can now run 'meowdfer' from any folder."