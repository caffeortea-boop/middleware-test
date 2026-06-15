import subprocess
import json
from datetime import datetime


def load_tasks():
    with open("task.json", "r") as f:
        data = json.load(f)

    if isinstance(data, dict):
        return [data]
    return data


def run(task):
    prompt = f"Execute command:\n\n{task['command']}"

    result = subprocess.run(
        ["bash", "-lc", task["command"]],
        capture_output=True,
        text=True
    )

    log = {
        "task_id": task["task_id"],
        "command": task["command"],
        "status": "success" if result.returncode == 0 else "failed",
        "stdout": result.stdout,
        "stderr": result.stderr,
        "timestamp": datetime.utcnow().isoformat()
    }

    with open("logs/run.jsonl", "a") as f:
        f.write(json.dumps(log) + "\n")

    return log


if __name__ == "__main__":
    tasks = load_tasks()

    for task in tasks:
        print(run(task))
