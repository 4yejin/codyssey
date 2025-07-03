# 단계 1(project) - 과정 1(Project 1) - 문제 2
# mission_computer_main.log 사용, mission_computer_main.json 생성

# 조건
# mission_computer_main.log 파일을 읽어들여서 출력한다. 콤마를 기준으로 날짜 및 시간과 로그 내용을 분류해서 Python의 리스트(List) 객체로 전환한다.
# (여기서 말하는 리스트는 배열이 아니라 파이썬에서 제공하는 리스트 타입의 객체를 의미한다.)
# 전환된 리스트 객체를 화면에 출력한다.
# 리스트 객체를 시간의 역순으로 정렬(sort)한다.
# 리스트 객체를 사전(Dict) 객체로 전환한다.
# 사전 객체로 전환된 내용을 mission_computer_main.json 파일로 저장하는데 파일 포멧은 JSON(JavaScript Ontation)으로 저장한다.

# Python 버전은 3.x 버전으로 한다. 
# Python에서 기본 제공되는 명령어만 사용해야 하며 별도의 라이브러리나 패키지를 사용해서는 안된다. 
# Python의 coding style guide를 확인하고 가이드를 준수해서 코딩한다. 
# (PEP 8 – 파이썬 코드 스타일 가이드 | peps.python.org)
# 문자열을 표현 할 때에는 ‘ ’을 기본으로 사용한다. 다만 문자열 내에서 ‘을 사용할 경우와 같이 부득이한 경우에는 “ “를 사용한다. 
# foo = (0,) 와 같이 대입문의  = 앞 뒤로는 공백을 준다. 
# 들여 쓰기는 공백을 기본으로 사용합니다. 

# 제약사항
# 추가 라이브러리를 사용하지 않고 Python 기본 명령어로만 작업해야 한다.
# 파일처리 부분에는 모두 예외처리가 되어 있어야 한다.
# JSON 포멧이 완전하게 구현되어야 한다.

# 보너스 과제
# 사전 객체로 전환된 내용에서 특정 문자열 (예를 들어 Oxygen)을 입력하면 해당 내용을 출력하는 코드를 추가한다.

#--------------------------------------------------------------------------

import os
import json # dict 객체를 .json 형식으로 저장

# 로그 파일 경로 (상대 경로)
log_file_path = './mission_computer_main.log'

# 로그 존재 여부 확인
if not os.path.exists(log_file_path):
    print(f'❌ 로그 파일이 존재하지 않습니다: {log_file_path}')
    exit(1) # 에러로 인한 강제 종료

# 리스트로 전환 _ 로그 항목을 담을 빈 리스트 선언
log_entries = []

try:
    with open(log_file_path, 'r', encoding='utf-8') as file: # UTF-8 인코딩으로 파일 읽기
        next(file)  # 첫 줄 헤더 생략
        for line in file:
            parts = line.strip().split(',', 2)
            if len(parts) == 3:
                timestamp, event, message = parts # 각 줄을 콤마(,)로 최대 3개로 나눔
                log_entries.append([timestamp.strip(), event.strip(), message.strip()])
                # 각각 strip()으로 공백 제거 후, 리스트로 저장
except Exception as e: # 만약 try 블록에서 에러 났을 때 에러 메세지 출력 후 종료
    print(f'❌ 로그 읽기 실패: {e}')
    exit(1)

# 리스트 출력
print('\n✅ 리스트 형식 출력:')
for entry in log_entries:
    print(entry)

# 시간 기준 역순 정렬(sort) (timestamp는 문자열이지만 ISO 형식이라 정렬 가능)
log_entries.sort(reverse=True) # reverse=true : 최신 로그가 먼저 오도록 역순 정렬

# 사전(dict)으로 변환
log_dicts = [{'timestamp': e[0], 'event': e[1], 'message': e[2]} for e in log_entries]
# log_entries : 리스트의 각 항목을 dict 형식으로 변환

# JSON 파일로 저장
json_path = './mission_computer_main.json'

try:
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(log_dicts, f, indent=2, ensure_ascii=False) 
        # json.dump : 사전 객체(log_dicts)를 .json 형식으로 저장하는 함수
        # indent=2 : 보기 좋게 들여쓰기
        # ensure_ascii=False : 한글 깨짐 방지
    print(f'\n✅ JSON 저장 완료: {json_path}')
except Exception as e:
    print(f'❌ JSON 저장 실패: {e}')
    exit(1)

# 🔍 보너스: 특정 키워드 필터링
search_keyword = 'Oxygen' # message 필드 안에 Oxygen 이라는 단어가 포함된 로그만 출력
print(f'\n🔎 메시지에 "{search_keyword}" 포함된 로그:')
for entry in log_dicts:
    if search_keyword.lower() in entry['message'].lower(): 
        # lower() : 대소문자 구분 없이 비교 
        print(entry)


# 목적?
# 1. 자동으로 로그 읽고 python을 활용한 자동 분석 시스템 도구 제작
# 2. CSV -> List -> Dict -> JSON 변환 익히기
# CSV : 각 줄이 하나의 레코드(row), 각 쉼표로 구분된 값이 열(column)
#       사람이 보기 쉽지만 단순 문자열 모음(텍스트 기반)
# List : 각 줄을 읽고 split(',')으로 분해해 리스트에 저장 (2차원 배열)
#       행 단위 데이터 집합을 list (파이썬 기본 자료구조)로 다룰 수 있음
#       정렬, 검색, 필터링 등 기초처리 가능
# Dict : 각 리스트 항목을 이것으로 변환(구조화)
#       사전형으로 의미 부여(검색 유용)
# JSON : list of dict 구조 그대로 JSON 직렬화
#       사람, 컴퓨터 모두 읽기 쉬움(범용 데이터 포멧)