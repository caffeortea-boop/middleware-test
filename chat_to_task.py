import os
import json
import sys
from openai import OpenAI

TASK_FILE = "task.json"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []

    with open(TASK_FILE, "r") as f:
        return json.load(f).get("tasks", [])


def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump({"tasks": tasks}, f, ensure_ascii=False, indent=2)


def generate_task(prompt):
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {
                "role": "system",
                "content": "You convert user requests into executable shell tasks. Return JSON only with task_id and command."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content
    return json.loads(content)


def main():
    if len(sys.argv) < 2:
        print('使い方: python3 chat_to_task.py "やりたいこと"')
        return

    prompt = sys.argv[1]

    task = generate_task(prompt)

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)

    print("AI生成タスク:", task)


if __name__ == "__main__":
    main()
