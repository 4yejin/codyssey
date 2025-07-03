# 단계 1(project) - 과정 1(Project 1) - 문제 1
# -> mission_computer_main.log 이용, log_analysis.md 생성

# 조건
# 로그 분석을 위해 Python으로 소프트웨어를 개발해야 한다. 이를 위해서 먼저 Python을 설치해야 한다.
# 빠른 개발을 위해 Python 개발 도구들을 알아보고 비교해서 하나의 도구를 선정해서 설치한다.
# 설치가 잘 되었는지 확인 하기 위해서 ‘Hello Mars’를 출력해 본다.
# 본격적으로 로그를 분석하기 위해서 mission_computer_main.log 파일을 열고 전체 내용을 화면에 출력해 본다. 이때 코드는 main.py 파일로 저장한다.
# (로그 데이터는 별도 제공)
# 파일을 처리 할 때에 발생할 수 있는 예외를 처리한다.
# mission_computer_main.log의 내용을 통해서 사고의 원인을 분석하고 정리해서 보고서(log_analysis.md)를 Markdown 형태로 를 작성해 놓는다.
	
# Python 버전은 3.x 버전으로 한다.
# Python에서 기본 제공되는 명령어만 사용해야 하며 별도의 라이브러리나 패키지를 사용해서는 안된다.
# Python의 coding style guide를 확인하고 가이드를 준수해서 코딩한다.
# (PEP 8 – 파이썬 코드 스타일 가이드 | peps.python.org)
# 문자열을 표현 할 때에는 ‘ ’을 기본으로 사용한다. 다만 문자열 내에서 ‘을 사용할 경우와 같이 부득이한 경우에는 “ “를 사용한다.
# foo = (0,) 와 같이 대입문의 = 앞 뒤로는 공백을 준다.
# 들여 쓰기는 공백을 기본으로 사용합니다.

# 제약사항
# 보고서는 UTF8 형태의 encoding을 사용해서 저장한다.
# 수행 과제에 지시된 파일 이름을 준수한다.

# 보너스 과제
# 출력 결과를 시간의 역순으로 정렬해서 출력한다.
# 출력 결과 중 문제가 되는 부분만 따로 파일로 저장한다.

#--------------------------------------------------------------------------

import os # 파일 경로 확인
from collections import Counter # 이벤트 횟수 계산
import datetime # 시간 정보 얻기 위함
# 어디에 적용되는지 궁금하면 주석처리 해보기

print("Hello Mars")

# log 파일 경로 지정
log_file_path = "./Project 1/mission_computer_main.log"

# 로그 파일 존재 여부 확인
if not os.path.exists(log_file_path): # 파일 존재하지 않을 때 true
    print(f"❌ 로그 파일이 존재하지 않습니다: {log_file_path}")
    exit(1) # 0 : 정상 종료, 1 : 에러로 인한 비정상 종료

# 로그 파일 열기 및 출력
try: # 예외 발생 코드 실행
    with open(log_file_path, "r", encoding="utf-8") as file: # with구문은 자동으로 닫힘
        for line in file: # 한 줄 씩 읽기
            print(line.strip()) # 양쪽 공백(특히 줄 바꿈 문자 \n) 제거 후 출력
except Exception as e: # 오류 발생 시 해당 블록 실행 _ 예외처리
    print(f"❌ 로그 파일 열기 실패: {e}") # e에 실제 오류 메세지 자동으로 삽입
    exit(1)

# 이상 로그 탐지
print("\n❗ 이상 로그 탐지:")
keywords = ["unstable", "explosion", "error", "fail"]

try:
    with open(log_file_path, "r", encoding="utf-8") as file:
        next(file)  # 첫 줄 헤더 생략
        for line in file:
            if any(k in line.lower() for k in keywords): 
                # keywords 중 하나라도 포함되어있으면 조건 만족
                #line.lower() : 소문자로 전부 교체
                print("⚠️", line.strip())
except Exception as e:
    print(f"❌ 로그 탐지 중 오류 발생: {e}")
    exit(1)

# 로그 분석
event_counter = Counter() # 항목별 개수를 자동으로 세어줌
anomalies = [] # 이상 로그를 담아줄 리스트, (시간, 메세지 형태로 추가)

try:
    with open(log_file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    for line in lines[1:]:  # 첫 줄은 header 생략, 두 번째 줄부터 반복
        parts = line.split(",", 2) # 각 줄을 쉼표 기준으로 3개로 나눔
        if len(parts) == 3: # 잘 분리된건지 확인
            timestamp, event, message = parts # 변수할당
            event_counter[event.strip()] += 1 # 해당 이벤트 이름 출현 횟수 1 증가
            if any(k in message.lower() for k in keywords):
                anomalies.append((timestamp.strip(), message.strip()))
                # 메세지에 unstable, explosion, error, fail 중 하난라도 있다면
                # anomalies 리스트에 (timestamp, message) 튜플 저장
        else:
            print(f"⚠️ 로그 형식 이상 무시됨: {line}")
            # 만약 3개의 항목이 아니면 경고 메세지 출력 후 건너뜀

except Exception as e:
    print(f"❌ 로그 분석 중 오류 발생: {e}")
    exit(1) # 전체 분석 중 문제 발생시 에러메세지 출력 후 프로그램 종료

# Markdown 저장 경로
output_path = "./Project 1/log_analysis.md"

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
