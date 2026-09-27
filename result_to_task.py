import json
import os
import time

RESULT_FILE = "result.json"
TASK_FILE = "task.json"

MAX_TASKS = 10

SAFE_COMMANDS = [
    "date",
    "echo SYSTEM OK",
    "echo AFTER DATE",
    "echo LOOP CHECK",
]


def load_recent_results(n=3):
    if not os.path.exists(RESULT_FILE):
        return []
    with open(RESULT_FILE, "r") as f:
        lines = [l for l in f if l.strip()]
    results = []
    for line in lines[-n:]:
        try:
            results.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return results


def summarize(results):
    if not results:
        return "実行結果なし"
    parts = []
    for r in results:
        parts.append(f"{r.get('task_id', '?')}={r.get('command', '?')}")
    return f"直近{len(results)}件: " + " / ".join(parts)


def pick_next_command(results):
    recent_cmds = [r.get("command") for r in results]
    for c in SAFE_COMMANDS:
        if c not in recent_cmds:
            return c
    return SAFE_COMMANDS[0]


def append_task(task):
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {"tasks": []}
    else:
        data = {"tasks": []}

    if "tasks" not in data:
        data["tasks"] = []

    data["tasks"].append(task)

    with open(TASK_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    try:
        count = sum(1 for _ in open(RESULT_FILE)) if os.path.exists(RESULT_FILE) else 0
        if count >= MAX_TASKS:
            print(f"STOP: 実行回数{count}件が上限{MAX_TASKS}に到達")
            return

        results = load_recent_results(3)
        summary = summarize(results)
        next_cmd = pick_next_command(results)

        if results and results[-1].get("command") == next_cmd:
            print(f"STOP: 直前と同じcommandのため停止 ({next_cmd})")
            return

        # ★ここだけ修正済み（重複防止）
        task_id = f"agg_{int(time.time() * 1000)}"

        task = {"task_id": task_id, "command": next_cmd}
        append_task(task)

        print(f"summary  : {summary}")
        print(f"next_task: {next_cmd}")
        print(f"task_id  : {task_id}")

    except Exception as e:
        print(f"STOP: エラー発生のため停止 - {e}")


if __name__ == "__main__":
    main()
