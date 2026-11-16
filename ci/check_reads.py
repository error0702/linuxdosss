"""Measure fresh PostgreSQL snapshots on both sides of the browser visit."""
import json
import os
import subprocess
import sys
from pathlib import Path


def snapshot():
    sql = Path("ci/read_counts.sql").read_text()
    out = subprocess.check_output(
        ["docker", "exec", "-i", "-u", "postgres", "forum",
         "psql", "-X", "-qAt", "-v", "ON_ERROR_STOP=1", "-d", "discourse"],
        input=sql, text=True,
    )
    account, target, control = map(int, out.strip().split("|"))
    return dict(account=account, target=target, unread_control=control)


before = snapshot()
print(f"Database before: {before}", flush=True)
assert before["target"] == before["unread_control"] == 0, "Fixtures must start unread"
subprocess.run([sys.executable, "linux_do_headless.py"], check=True)
after = snapshot()
delta = {key: after[key] - before[key] for key in before}
evidence = json.dumps(dict(before=before, after=after, delta=delta), indent=2)
print(evidence, flush=True)
with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
    summary.write("### Discourse PostgreSQL read counts\n\n```json\n" + evidence + "\n```\n")
assert delta == dict(account=1, target=1, unread_control=0), "Unexpected server-side change"
