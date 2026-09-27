#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

mkdir -p logs

# watcher.py がまだ動いていなければバックグラウンド起動（多重起動防止）
if pgrep -f "python3 watcher.py" > /dev/null; then
    echo "[INFO] watcher.py は既に動作中"
else
    echo "[INFO] watcher.py をバックグラウンド起動"
    nohup python3 watcher.py > logs/watcher.out 2>&1 &
    sleep 1
fi

# result_to_task.py を1回だけ実行（内部のMAX_TASKS=10で暴走防止）
echo "[INFO] result_to_task.py を実行"
python3 result_to_task.py
