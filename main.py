import os
from collections import Counter
import datetime

print("Hellow Mars")

# log 파일 경로 지정
log_file_path = "C:/Users/Han/Downloads/python_study/25_06_30/mission_computer_main.log"

# 로그 파일 존재 여부 확인
if not os.path.exists(log_file_path):
    print(f"❌ 로그 파일이 존재하지 않습니다: {log_file_path}")
    exit(1)

# 파일 열기 및 출력
try:
    with open(log_file_path, "r", encoding="utf-8") as file:
        for line in file:
            print(line.strip())
except Exception as e:
    print(f"❌ 로그 파일 열기 실패: {e}")
    exit(1)

# 이상 로그 탐지
print("\n❗ 이상 로그 탐지:")
keywords = ["unstable", "explosion", "error", "fail"]

try:
    with open(log_file_path, "r", encoding="utf-8") as file:
        next(file)  # 헤더 생략
        for line in file:
            if any(k in line.lower() for k in keywords):
                print("⚠️", line.strip())
except Exception as e:
    print(f"❌ 로그 탐지 중 오류 발생: {e}")
    exit(1)

# 로그 분석
event_counter = Counter()
anomalies = []

try:
    with open(log_file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    for line in lines[1:]:  # 첫 줄은 header 생략
        parts = line.split(",", 2)
        if len(parts) == 3:
            timestamp, event, message = parts
            event_counter[event.strip()] += 1
            if any(k in message.lower() for k in keywords):
                anomalies.append((timestamp.strip(), message.strip()))
        else:
            print(f"⚠️ 로그 형식 이상 무시됨: {line}")

except Exception as e:
    print(f"❌ 로그 분석 중 오류 발생: {e}")
    exit(1)

# Markdown 저장 경로
output_path = "C:/Users/Han/Documents/log_analysis.md"

# Markdown 저장
try:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 📄 로그 분석 보고서\n\n")
        f.write(f"**파일 경로**: `{log_file_path}`\n")
        f.write(f"**생성 시각**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("## 📊 이벤트 통계\n\n")
        f.write("| 이벤트 | 횟수 |\n")
        f.write("|---------|------|\n")
        for evt, count in event_counter.items():
            f.write(f"| {evt} | {count} |\n")

        f.write("\n---\n\n")
        f.write("## ❗ 이상 로그 메시지\n\n")
        if anomalies:
            for ts, msg in anomalies:
                f.write(f"- `{ts}` → ⚠️ {msg}\n")
        else:
            f.write("_이상 로그 없음_\n")

        f.write("\n---\n\n")
        f.write("## 📌 해석 및 사고 원인 정리 (수동 입력)\n\n")
        f.write("> ⚠️ 이 섹션은 사용자가 직접 입력해야 합니다.\n")
        f.write("> 예: '산소 탱크 이상 감지 후 폭발이 발생함. 착륙 이후 시스템 문제로 추정됨.'\n")

    if os.path.exists(output_path):
        print("✅ 보고서 저장 성공:", os.path.abspath(output_path))
    else:
        print("❌ 보고서 파일이 생성되지 않았습니다.")

except Exception as e:
    print(f"❌ Markdown 저장 중 오류 발생: {e}")
    exit(1)
