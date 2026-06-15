import json
import subprocess
from datetime import datetime
import os

TASK_FILE = "task.json"
LOG_FILE = "logs/run.jsonl"


def load_tasks():
    with open(TASK_FILE, "r") as f:
        data = json.load(f)
        return data.get("tasks", [])


def run(task):
    result = subprocess.run(
        task["command"],
        shell=True,
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

    # logsフォルダがなければ作る
    os.makedirs("logs", exist_ok=True)

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log, ensure_ascii=False) + "\n")

    print("実行：", log)


def main():
    tasks = load_tasks()

    if not tasks:
        print("タスクがありません")
        return

    for task in tasks:
        run(task)


if __name__ == "__main__":
    main()
