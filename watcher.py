import json
import subprocess
import time
import os
from datetime import datetime

TASK_FILE = "task.json"
LOG_FILE = "logs/run.jsonl"
DONE_FILE = "done_tasks.json"


def load_tasks():
    with open(TASK_FILE, "r") as f:
        data = json.load(f)
        return data.get("tasks", [])


def load_done():
    if not os.path.exists(DONE_FILE):
        return set()

    with open(DONE_FILE, "r") as f:
        return set(json.load(f))


def save_done(done_tasks):
    with open(DONE_FILE, "w") as f:
        json.dump(list(done_tasks), f)


def run(task):
    result = subprocess.run(
        task["command"],
        shell=True,
        capture_output=True,
        text=True
    )

    os.makedirs("logs", exist_ok=True)

    log = {
        "task_id": task["task_id"],
        "command": task["command"],
        "status": "success" if result.returncode == 0 else "failed",
        "stdout": result.stdout,
        "stderr": result.stderr,
        "timestamp": datetime.utcnow().isoformat()
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")

    print("実行完了:", log)


def main():
    done_tasks = load_done()

    while True:
        tasks = load_tasks()

        for task in tasks:
            if task["task_id"] in done_tasks:
                continue

            run(task)
            done_tasks.add(task["task_id"])
            save_done(done_tasks)

        time.sleep(1)


if __name__ == "__main__":
    main()
