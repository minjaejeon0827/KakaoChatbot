# TODO: 파이썬 logging 라이브러리 사용해서 전역 로그 객체 및 로그 기록 기능 구현하기 (2025.09.18 minjae)
# 참고 URL - https://claude.ai/chat/8fc1ceeb-fe95-4d1b-8517-ecec83beb3f2
import sys
import logging   # 로그 작성 라이브러리

# 1. 공통 모듈 먼저 import 처리
from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트

# 2. singleton 모듈 import 처리 
from modules.singleton import KSTFormatter   # 싱글톤(singleton) 패턴 전용 모듈
# from datetime import datetime 
# from zoneinfo import ZoneInfo  # 로그 출력시 대한민국 표준시로 출력하기 위해 패키지 "zoneinfo" 불러오기 


# 1. logger instance 설정 - logger의 이름(__name__)을 명시해서 logger instance 설정하기
# logger = logging.getLogger()
logger = logging.getLogger(chatbot_helper._chatbot_logger)   # root logger 대신 특별한 이름('chatbot_logger')의 전역 로그 객체(logger) 생성
logger.setLevel(logging.INFO)

# 2. 기존 핸들러들 모두 제거
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Lambda의 기본 로그(root logger)와 분리하기 위해 propagate를 False로 설정 (False일 경우, chatbot_logger의 로깅 메시지가 조상(root) 로거의 처리기로 전달되지 않는다.)
# 참고 URL - https://docs.python.org/ko/3/library/logging.html
logger.propagate = False


# 3. formatter 생성 (로그 작성/출력/저장에 사용할 날짜 + 로그 메시지)
# 원하는 출력 형태: [INFO] [2025-09-18 10:49:19] [kakao.py | get_response - L282]: [테스트] 카카오 json 포맷 가져오기 - Start!
# formatter = logging.Formatter('[%(levelname)s] [%(asctime)s] [%(filename)s | %(funcName)s - L%(lineno)d]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
formatter = KSTFormatter('[%(levelname)s] [%(asctime)s] [%(filename)s | %(funcName)s - L%(lineno)d]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# 4. handler 생성(설정) (streamHandler : 콘솔 출력용 // fileHandler : 파일 기록용)
# streamHandler = logging.StreamHandler()
streamHandler = logging.StreamHandler(sys.stdout)
# TODO: fileHandler 생성 및 logger instance(logger)에 handler 추가 후 OpenAI 기능 함수 openAI.getMessageFromGPT(prompt) 실행시 
#       카카오톡 채팅방에 아래와 같은 메시지가 추가로 출력되어 나오므로 fileHandler 생성 및 logger instance(logger)에 handler 추가하는 로직 주석 처리 진행 (2025.09.19 minjae)
# * 주의사항: 기술지원 챗봇은 실수를 할 수 있습니다. 응답을 반드시 다시 확인해 주세요.[INFO] [2025-09-19 16:11:44] [lambda_function.py | handler - L157]: [테스트] 챗봇 답변 채팅 정보 - {"version": "2.0", "template": {"outputs": [{"simpleText": {"text": "\uc694\uccad\uc0ac\ud56d \ud655\uc778 \uc911\uc774\uc5d0\uc694.\n\uc7a0\uc2dc\ud6c4 \uc544\ub798 \ub9d0\ud48d\uc120\uc744 \ub20c\ub7ec\uc8fc\uc138\uc694."}}], "quickReplies": [{"action": "message", "label": "\uc0dd\uac01 \ub2e4 \ub05d\ub0ac\ub098\uc694?", "messageText": "\uc0dd\uac01 \ub2e4 \ub05d\ub0ac\ub098\uc694?"}]}}
# [INFO] [2025-09-19 16:11:46] [lambda_function.py | handler - L93]: [테스트] 사용자 입력 채팅 정보 - {"bot":{"id":"67a961ce1e098a447d574fe7","name":"TestImbuChatBot"},"intent":{"id":"67a961ce1e098a447d574feb","name":"폴백 블록","extra":{"reason":{"code":1,"message":"OK"}}},"action":{"id":"67a99c2e92df7f65390d32f5","name":"kakaobot","params":{},"detailParams":{},"clientExtra":{}},"userRequest":{"block":{"id":"67a961ce1e098a447d574feb","name":"폴백 블록"},"user":{"id":"1b2bfc8caf85a5dff8fadd1bf4cc70125b533fea7b665d0cdb0fb493a135e94b4d","type":"botUserKey","properties":{"botUserKey":"1b2bfc8caf85a5dff8fadd1bf4cc70125b533fea7b665d0cdb0fb493a135e94b4d","isFriend":true,"plusfriendUserKey":"OL1xAnN6qN4s","bot_user_key":"1b2bfc8caf85a5dff8fadd1bf4cc70125b533fea7b665d0cdb0fb493a135e94b4d","plusfriend_user_key":"OL1xAnN6qN4s"}},"utterance":"생각 다 끝났나요?","params":{"surface":"Kakaotalk.plusfriend"},"lang":"ko","timezone":"Asia/Seoul"},"contexts":[],"flow":{"lastBlock":{"id":"67a961ce1e098a447d574feb","name":"폴백 블록"},"trigger":{"type":"QUICKREPLY_BUTTON_MESSAGE","referrerBlock":{"id":"67a961ce1e098a447d574feb","name":"폴백 블록"}}}}
# [INFO] [2025-09-19 16:11:46] [lambda_function.py | handler - L102]: [테스트] event_body['action'] - {'id': '67a99c2e92df7f65390d32f5', 'name': 'kakaobot', 'params': {}, 'detailParams': {}, 'clientExtra': {}}
# [INFO] [2025-09-19 16:11:46] [lambda_function.py | handler - L122]: 파일 존재 여부 - File Exists!
# fileHandler = logging.FileHandler(chatbot_helper._botlog_file_path)    # 로그를 기록할 파일 이름(경로) "/tmp/botlog.txt" 지정 (파일 이름은 다른 것으로 변경해도 된다.)

# 5. logger instance에 formatter 설정(할당) (각각의 Handler에 formatter 설정 적용)
streamHandler.setFormatter(formatter)
# fileHandler.setFormatter(formatter)


# 6. logger instance(logger)에 handler 추가 (addHandler) (입력받는 log에 handler 사용)
logger.addHandler(streamHandler)
# logger.addHandler(fileHandler)

# 참고 
# * 파이썬 logging 모듈 사용하여 로그 기록하기 
# 참고 URL - https://docs.python.org/ko/3/library/logging.html
# 참고 2 URL - https://docs.python.org/ko/3/howto/logging.html#basic-logging-tutorial
# 참고 3 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-logging.html
# 참고 4 URL - https://wikidocs.net/84432
# 참고 5 URL - https://wikidocs.net/123324
# 참고 6 URL - https://velog.io/@jeongpar/Python-Logging-%EC%82%AC%EC%9A%A9%EB%B2%95
# 참고 7 URL - https://aoc55.tistory.com/10

# * 파이썬 logging 모듈 사용하여 전역 로그 기능 구현하기 
# 참고 URL - https://chuun92.tistory.com/7
# 참고 2 URL - https://malwareanalysis.tistory.com/527
# 참고 3 URL - https://github.com/sungwook-practice/python_logging_logger.git
# 참고 4 URL - https://velog.io/@qlgks1/python-python-logging-%ED%95%B4%EB%B6%80