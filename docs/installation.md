# Installation

## Requirements

- Python 3.7 or higher
- pip (Python package installer)

## Development Installation

For development or contributing to the project:

```bash
# Clone the repository
git clone https://github.com/dineshchhantyal/chart_gizmo
cd chart_gizmo

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies and development version
pip install --upgrade pip setuptools build
pip install -e .
```

## Verifying Installation

After installation, you should be able to run the command-line tools:

```bash
histogram-gizmo --help
csv-bar-gizmo --help
csv-line-gizmo --help
csv-bubble-gizmo --help
```
