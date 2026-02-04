"""Entry point for running the UI with `python -m ui`."""

import sys
import subprocess
from pathlib import Path


def main():
    """Run the Streamlit app."""
    app_path = Path(__file__).parent / "app.py"

    # Run streamlit with dark theme
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_path),
        "--theme.base=dark",
        "--server.headless=true",
    ]

    subprocess.run(cmd)


if __name__ == "__main__":
    main()
