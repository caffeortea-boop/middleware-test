import sys
import json
import subprocess
import time

# ChatGPTの代わり（ここは後でAPI化する）
def fake_chatgpt(prompt):
    # 仮：とりあえずechoに変換
    return {
        "task_id": str(int(time.time())),
        "command": f"echo {prompt}"
    }


def main():
    if len(sys.argv) < 2:
        print('使い方: python3 prompt_to_task.py "やりたいこと"')
        return

    prompt = sys.argv[1]

    task = fake_chatgpt(prompt)

    print("生成タスク:", task)

    # そのままtask.jsonに追加
    try:
        with open("task.json", "r") as f:
            data = json.load(f)
    except:
        data = {"tasks": []}

    data["tasks"].append(task)

    with open("task.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("task.jsonに追加しました")


if __name__ == "__main__":
    main()

