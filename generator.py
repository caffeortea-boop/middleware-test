import json
import random

LOG_FILE = "logs/run.jsonl"
TASK_FILE = "task.json"

COMMANDS = [
    "date",
    "echo SYSTEM OK",
    "echo AFTER DATE",
    "echo LOOP CHECK"
]

def load_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        return []

def get_recent_commands(logs, n=10):
    return [log.get("command") for log in logs[-n:]]

def pick_command(recent):
    # 直近3回と被るものは避ける
    recent3 = recent[-3:]

    candidates = [c for c in COMMANDS if c not in recent3]

    if not candidates:
        return random.choice(COMMANDS)

    return random.choice(candidates)

def save_task(cmd):
    task_id = f"auto_{random.randint(100,999)}"
    with open(TASK_FILE, "w") as f:
        f.write(f'{{"tasks":[{{"task_id":"{task_id}","command":"{cmd}"}}]}}')

def main():
    logs = load_logs()
    recent = get_recent_commands(logs)

    cmd = pick_command(recent)

    save_task(cmd)

    print("task updated:", cmd)

if __name__ == "__main__":
    main()
