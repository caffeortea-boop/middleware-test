import json
import subprocess

# task.jsonを読み込み
with open("task.json") as f:
    data = json.load(f)

tasks = data["tasks"]

print(f"TOTAL TASKS: {len(tasks)}")

# 全タスクを順番に実行
for task in tasks:
    print("\nRUN TASK:", task)

    command = task["command"]

    # ★ここが重要：Claudeを使わずにPCが直接実行する
    result = subprocess.run(
        ["bash", "-c", command],
        capture_output=True,
        text=True
    )

    print("STDOUT:")
    print(result.stdout)

    print("STDERR:")
    print(result.stderr)

    # タスクごとにファイル保存
    output_file = f"result_{task['task_id']}.txt"

    with open(output_file, "w") as f:
        f.write(result.stdout)

print("\nDONE ALL TASKS")

# まとめ表示
print("\n=== SUMMARY ===")

for task in tasks:
    output_file = f"result_{task['task_id']}.txt"
    try:
        with open(output_file) as f:
            content = f.read()
        print(task["task_id"], "→", content.strip())
    except:
        print(task["task_id"], "→ NO RESULT")
