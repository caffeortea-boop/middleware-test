import json

LOG_FILE = "logs/run.jsonl"

def load_logs():
    try:
        with open(LOG_FILE, "r") as f:
            return [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        return []

def get_recent_commands(logs, n=10):
    return [log.get("command") for log in logs[-n:]]

def is_repeat(command, recent_commands):
    return command in recent_commands

# 元のgeneratorの代わりに使う簡易ロジック例
def pick_command():
    return "date"  # ←ここは既存ロジックに置き換えられる想定

def main():
    logs = load_logs()
    recent = get_recent_commands(logs)

    while True:
        cmd = pick_command()

        if is_repeat(cmd, recent):
            print("⛔ 重複なのでスキップ:", cmd)
            continue

        print("✅ 実行OK:", cmd)
        break

if __name__ == "__main__":
    main()
