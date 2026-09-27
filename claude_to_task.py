import json
import sys
import time

def add_task(command: str):
    task = {
        "task_id": f"auto_{int(time.time())}",
        "command": command
    }

    try:
        with open("task.json", "r") as f:
            data = json.load(f)
    except:
        data = {"tasks": []}

    data["tasks"].append(task)

    with open("task.json", "w") as f:
        json.dump(data, f, ensure_ascii=False)

    print("task added:", task)

if __name__ == "__main__":
    cmd = " ".join(sys.argv[1:])
    add_task(cmd)
