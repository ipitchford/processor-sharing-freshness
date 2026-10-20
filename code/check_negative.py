"""Verify that a semantically corrupted expected mean is rejected under -O."""
import json
from pathlib import Path
import subprocess
import sys

command = [sys.executable, "-B", "-O", str(Path(__file__).with_name("replay.py")),
           "--negative-control"]
result = subprocess.run(command, capture_output=True, text=True)
passed = result.returncode != 0 and "finite-chain mean mismatch" in result.stderr
report = {"status": "pass" if passed else "fail", "child_optimized": True,
          "mutation": "capacity-two expected exact mean increased by one",
          "returncode": result.returncode, "stderr": result.stderr}
print(json.dumps(report, indent=2))
if not passed:
    raise SystemExit("negative control was not rejected")
