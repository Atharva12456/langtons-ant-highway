"""Regenerate the first-R cyclic-phase certificate through period 32.

The 32 length-six prefix shards are independent subprocesses.  A separate
unprefixed run covers depths zero through five. Every positive-growth
heading-resetting word has a cyclic shift beginning with R.
"""
from __future__ import annotations

import itertools
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPO_SOURCE = ROOT.parent / "code/python/langton_research.py"
ARCHIVE_SOURCE = ROOT / "python/langton_research.py"
if REPO_SOURCE.is_file():
    SOURCE = REPO_SOURCE
    OUTPUT = ROOT.parent.parent / "work/p32_current_shards"
elif ARCHIVE_SOURCE.is_file():
    SOURCE = ARCHIVE_SOURCE
    OUTPUT = ROOT / "p32_rerun_shards"
else:
    raise FileNotFoundError("cannot locate code/python/langton_research.py")


def run(prefix: str, max_period: int, filename: str) -> tuple[str, str]:
    output = OUTPUT / filename
    command = [
        sys.executable,
        str(SOURCE),
        "search-highway-words",
        "--max-period",
        str(max_period),
        "--node-cap",
        "100000000",
    ]
    if prefix:
        command += ["--prefix", prefix]
    command += ["--output", str(output)]
    completed = subprocess.run(command, capture_output=True, text=True, check=True)
    return filename, completed.stdout.strip()


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    jobs = [
        ("R" + "".join(bits), 32, f"highway_words_p32_R{''.join(bits)}.json")
        for bits in itertools.product("RL", repeat=5)
    ]
    jobs.append(("", 5, "highway_words_p5_all.json"))
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(run, *job): job[2] for job in jobs}
        for future in as_completed(futures):
            filename, _ = future.result()
            print(f"completed {filename}")
    print(f"wrote {len(jobs)} records to {OUTPUT}")


if __name__ == "__main__":
    main()
