import shutil
from pathlib import Path

# copies all necessary Python files from the tutorial/ directory and places them in the ~/.ryven/nodes/tutorial_nodes/ directory
files = Path("../tutorial").glob("*.py")
dst_dir = Path.home() / ".ryven" / "nodes" / "tutorial_nodes/"
dst_dir.mkdir(parents=True, exist_ok=True)

for f in files:
    shutil.copy2(f, dst_dir / f.name)