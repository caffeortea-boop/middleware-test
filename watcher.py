import time
import json
import subprocess
from datetime import datetime

DONE = set()

def load_tasks():
    try:
        with open("task.json", "r") as f:
            return json.load(f).get("tasks", [])
    except:
        return []

# ★ここが重要（修正ポイント）
def run_claude(command):
    result = subprocess.run(
        ["claude", "-p", command],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def save_result(task_id, command, output):
    data = {
        "task_id": task_id,
        "command": command,
        "output": output,
        "timestamp": datetime.now().isoformat()
    }

    with open("result.json", "a") as f:
        json.dump(data, f)
        f.write("\n")

def main():
    print("watcher started...")

    while True:
        tasks = load_tasks()

        for task in tasks:
            task_id = task.get("task_id")
            command = task.get("command")

            if task_id in DONE:
                continue

            DONE.add(task_id)

            print(f"run: {task_id} {command}")

            output = run_claude(command)

            print(output)

            save_result(task_id, command, output)

        time.sleep(1)

if __name__ == "__main__":
    main()
