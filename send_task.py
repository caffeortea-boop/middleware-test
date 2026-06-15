import json
import sys
import os

TASK_FILE = "task.json"


def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []

    with open(TASK_FILE, "r") as f:
        return json.load(f).get("tasks", [])


def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump({"tasks": tasks}, f, ensure_ascii=False, indent=2)


def main():
    if len(sys.argv) < 3:
        print('使い方: python3 send_task.py <task_id> "<command>"')
        return

    task_id = sys.argv[1]
    command = sys.argv[2]

    tasks = load_tasks()

    tasks.append({
        "task_id": task_id,
        "command": command
    })

    save_tasks(tasks)

    print("送信完了:", task_id, command)


if __name__ == "__main__":
    main()
