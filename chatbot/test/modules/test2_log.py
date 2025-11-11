"""
* 챗봇 전역 로그 모듈
참고 URL - https://chatgpt.com/c/69118414-a588-8323-be5b-b0362b312cfa

파이썬 logging 라이브러리 사용해서 전역 로그 객체(logger) 및 로그 기록 기능 구현 (2025.09.18 minjae)
참고 URL - https://claude.ai/chat/8fc1ceeb-fe95-4d1b-8517-ecec83beb3f2

파이썬 패키지, 모듈 
참고 URL - https://docs.python.org/ko/3.13/tutorial/modules.html
참고 2 URL - https://wikidocs.net/1418
참고 3 URL - https://dojang.io/mod/page/view.php?id=2450
"""

import sys
import logging   # 로그 기록

# 1. 공통 모듈 먼저 import 처리
from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트

# 2. singleton 모듈 import 처리
from modules.singleton import KSTFormatter   # 싱글톤(singleton) 패턴

# 1. 전역 로그 객체(logger) 설정 - logger의 이름(__name__)을 명시해서 전역 로그 객체(logger) 설정하기
# logger = logging.getLogger()   # 최상위 로그 객체(root) 가져오기
logger = logging.getLogger('chatbot_logger')   # 최상위 로그 객체(root) 대신 특별한 이름('chatbot_logger')의 전역 로그 객체(logger) 생성
logger.setLevel(logging.INFO)

# 2. 기존 핸들러들 모두 제거
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# 3. 아마존 웹서비스 람다 함수(AWS Lambda function)의 최상위 로그 객체(root)와 분리하기 위해 propagate 속성(property) 값을 False로 설정 (False일 경우, chatbot_logger의 로깅 메시지가 최상위 로그 객체(root)의 처리기로 전달되지 않는다.)
logger.propagate = False

# 4. formatter 생성 (로그 기록/출력/저장에 사용할 날짜 + 로그 메시지)
# 원하는 출력 형태 예시: [INFO] [2025-09-18 10:49:19] [kakao.py | get_response - L282]: [테스트] 카카오 json 포맷 가져오기 - 시작!
# formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] [%(filename)s | %(funcName)s - L%(lineno)d]: %(message)s', datefmt=chatbot_helper._datefmt)
formatter = KSTFormatter('[%(levelname)s] [%(asctime)s] [%(filename)s | %(funcName)s - L%(lineno)d]: %(message)s', datefmt=chatbot_helper._datefmt)

# 5. handler 생성 (streamHandler: 콘솔 출력용 // fileHandler: 파일 기록용)
# streamHandler = logging.StreamHandler()
streamHandler = logging.StreamHandler(sys.stdout)

# fileHandler 생성 및 전역 로그 객체(logger)에 handler 추가 후 OpenAI 기능 함수 openAI.getMessageFromGPT(prompt) 실행시
# 카카오톡 채팅방에 아래와 같은 메시지가 추가로 출력되어 나오므로 fileHandler 생성 및 전역 로그 객체(logger)에 handler 추가하는 로직 주석 처리 + OpenAI 기능 모듈(openAI.py) 삭제 처리 진행 (2025.09.19 minjae)
# * 주의사항: 기술지원 챗봇은 실수를 할 수 있습니다. 응답을 반드시 다시 확인해 주세요.
# [INFO] [2025-09-19 16:11:44] [lambda_function.py | handler - L157]: [테스트] 챗봇 답변 채팅 정보 - {"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "\uc694\uccad\uc0ac\ud56d \ud655\uc778 \uc911\uc774\uc5d0\uc694.\n\uc7a0\uc2dc\ud6c4 \uc544\ub798 \ub9d0\ud48d\uc120\uc744 \ub20c\ub7ec\uc8fc\uc138\uc694."}}], "quickReplies": [{"action": "message", "label": "\uc0dd\uac01 \ub2e4 \ub05d\ub0ac\ub098\uc694?", "messageText": "\uc0dd\uac01 \ub2e4 \ub05d\ub0ac\ub098\uc694?"}]}}
# [INFO] [2025-09-19 16:11:46] [lambda_function.py | handler - L93]: [테스트] 사용자 입력 채팅 정보 - {"bot":{"id":"67a961ce1e098a447d574fe7","name":"TestImbuChatBot"},"intent":{"id":"67a961ce1e098a447d574feb","name":"폴백 블록","extra":{"reason":{"code":1,"message":"OK"}}},"action":{"id":"67a99c2e92df7f65390d32f5","name":"kakaobot","params":{},"detailParams":{},"clientExtra":{}},"userRequest":{"block":{"id":"67a961ce1e098a447d574feb","name":"폴백 블록"},"user":{"id":"1b2bfc8caf85a5dff8fadd1bf4cc70125b533fea7b665d0cdb0fb493a135e94b4d","type":"botUserKey","properties":{"botUserKey":"1b2bfc8caf85a5dff8fadd1bf4cc70125b533fea7b665d0cdb0fb493a135e94b4d","isFriend":true,"plusfriendUserKey":"OL1xAnN6qN4s","bot_user_key":"1b2bfc8caf85a5dff8fadd1bf4cc70125b533fea7b665d0cdb0fb493a135e94b4d","plusfriend_user_key":"OL1xAnN6qN4s"}},"utterance":"생각 다 끝났나요?","params":{"surface":"Kakaotalk.plusfriend"},"lang":"ko","timezone":"Asia/Seoul"},"contexts":[],"flow":{"lastBlock":{"id":"67a961ce1e098a447d574feb","name":"폴백 블록"},"trigger":{"type":"QUICKREPLY_BUTTON_MESSAGE","referrerBlock":{"id":"67a961ce1e098a447d574feb","name":"폴백 블록"}}}}
# [INFO] [2025-09-19 16:11:46] [lambda_function.py | handler - L102]: [테스트] event_body['action'] - {'id': '67a99c2e92df7f65390d32f5', 'name': 'kakaobot', 'params': {}, 'detailParams': {}, 'clientExtra': {}}
# [INFO] [2025-09-19 16:11:46] [lambda_function.py | handler - L122]: 파일 존재 여부 - File Exists!
# fileHandler = logging.FileHandler(chatbot_helper._botlog_file_path)    # 아마존 웹서비스 람다 함수(AWS Lambda function)에 로그 기록할 파일 이름(경로) "/tmp/botlog.txt" 지정 (파일 이름은 다른 것으로 변경해도 된다.)

# 6. 각각의 Handler에 formatter 설정(할당) 적용
streamHandler.setFormatter(formatter)
# fileHandler.setFormatter(formatter)

# 7. 전역 로그 객체(logger)에 handler 추가 (로그 기록시 해당 handler 적용)
logger.addHandler(streamHandler)
# logger.addHandler(fileHandler)

"""
* 참고 
파이썬 logging 모듈 사용하여 로그 기록하기 
참고 URL - https://docs.python.org/ko/3/library/logging.html
참고 2 URL - https://docs.python.org/ko/3/howto/logging.html#basic-logging-tutorial
참고 3 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-logging.html
참고 4 URL - https://wikidocs.net/84432
참고 5 URL - https://wikidocs.net/123324
참고 6 URL - https://velog.io/@jeongpar/Python-Logging-%EC%82%AC%EC%9A%A9%EB%B2%95
참고 7 URL - https://aoc55.tistory.com/10

파이썬 logging 모듈 사용하여 전역 로그 기능 구현하기 
참고 URL - https://chuun92.tistory.com/7
참고 2 URL - https://malwareanalysis.tistory.com/527
참고 3 URL - https://github.com/sungwook-practice/python_logging_logger.git
참고 4 URL - https://velog.io/@qlgks1/python-python-logging-%ED%95%B4%EB%B6%80

* 챗봇 전역 로그 모듈 구현 순서 및 로그 기록 방법 
​1. instance 설정 - log(로그) instance 설정
2. 기록할 log level 지정 - 로그 레벨 지정 (DEBUG, INFO, WARNING, ERROR, CRICTICAL)
3. formatter 생성 - log(로그)를 저장(기록)할 포맷(format) 지정 
4. handler 생성 - log(로그)를 담을 수 있는 핸들러(handler) 생성 (log(로그)를 콘솔창에 출력 할건지? 아니면 파일에 저장 할건지? 이런 저장하는 핸들러(handler) 생성하기)
5. handler에 formatter 지정 - 2번에서 지정한 포맷(format)을 핸들러(handler)에 지정
6. 입력받는 instance에 handler 추가 - 4번에서 지정한 포맷(format)을 핸들러(handler)에 지정한 이후 해당 핸들러(handler)를 log(로그) instance에 추가하여 "입력받는 값"을 핸들러(콘솔 또는 파일)로 가져올 수 있도록 또 설정하기 
7. 다른 파이썬 스크립트 파일에서 챗봇 전역 로그 모듈 import 처리 - from modules.log import logger   # 챗봇 전역 로그 객체(logger)  
8. 원하는 지점에 로그 기록하기 (예) logger.info("[테스트] ~~~"), logger.error(f"[테스트] 오류 - {error_msg}") 등등...

* 로그 포맷(format) formatter
|     이름    |   포멧           |   설명   |
| asctime     | %(asctime)s     | 날짜 시간, ex) 2021.04.10 11:21:48,162
| created     | %(created)f     | 생성 시간 출력
| filename    | %(filename)s    | 파일명
| funcName    | %(funcName)s    | 함수명
| levelname   | %(levelname)s   | 로그 레벨(DEBUG, INFO, WARNING, ERROR, CRITICAL)
| levelno     | %(levelno)s     | 로그 레벨 수치화해서 출력(10, 20, 30, …)
| lineno      | %(lineno)d      | 소스의 라인 넘버
| module      | %(module)s      | 모듈 이름
| msecs       | %(msecs)d       | 로그 생성 시간에서 밀리세컨드 시간 부분만 출력
| message     | %(message)s     | 로그 메시지
| name        | %(name)s        | 로그 이름
| pathname    | %(pathname)s    | 소스 경로
| process     | %(process)d     | 프로세스(Process) ID
| processName | %(processName)s | 프로세스 이름
| thread      | %(thread)d      | Thread ID
| threadName  | %(threadName)s  | Thread Name

* 로그 레벨 종류 
|   Level   |   Value   |   When to use
|   DEBUG   |     10    | (주로 문제 해결을 할때 필요한) 자세한 정보. - 개발 과정에서 오류 원인 파악하고자 할 때 사용
|   INFO    |     20    | 작업이 정상적으로 작동하고 있다는 메시지. 
|  WARNING  |     30    | 예상하지 못한 일이 발생하거나, 발생 가능한 문제점을 명시. (e.g 'disk space low') 작업은 정상적으로 진행.
|   ERROR   |     40    | 프로그램이 함수를 실행하지 못 할 정도의 심각한 문제.
| CRICTICAL |     50    | 프로그램이 동작할 수 없을 정도의 심각한 문제. 
"""