"""
* 아마존 웹서비스 람다 함수(AWS Lambda Function) 실행 진입점 (handler)
코드 리뷰 참고 URL - https://chatgpt.com/c/691e9f6e-3940-832a-afda-92c53ae4b49a

* 아마존 웹서비스 (AWS) 다중인증 (MFA는 Multi-Factor Authentication) 등록 방법 및 모바일 어플 Google Authenticator 설치 및 사용 방법
참고 URL - https://happy-jjang-a.tistory.com/223

* lambda_function.py 파이썬 스크립트 파일 소스 코드 리팩토링 (2025.09.30 minjae)
참고 URL - https://claude.ai/chat/786c45b9-f744-4fcf-950a-bcc178417e1c

* Race Condition
참고 URL - https://en.wikipedia.org/wiki/Race_condition
참고 2 URL - https://namu.wiki/w/%EA%B2%BD%EC%9F%81%20%EC%83%81%ED%83%9C
참고 3 URL - https://lake0989.tistory.com/121
"""

# 1. 공통 모듈 먼저 import
from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트

# 2. singleton 모듈을 log 모듈 보다 먼저 import
from modules.singleton import MasterEntity   # 싱글톤 (singleton) 패턴
from modules.chatbot_enum import EnumValidator   # 데이터 유효성 검사

# 3. singleton 모듈이 먼저 초기화된 후 log 모듈 import
from utils.log import logger   # 챗봇 전역 로그 객체 (logger)
from utils import aws

# 4. Type Hints class Any, Callable import
from typing import Any, Callable   # Callable - 함수 자체 타입 지정

# 5. 나머지 모듈 import
from modules.kakao import KakaoResponseFormatter   # 카카오 스킬 응답 템플릿 json 포맷
# 아래처럼 LambdaContext 클래스 import 처리하기 위해 비쥬얼스튜디오코드 (VSCode) cmd 터미널창 열고 -> 파이썬 패키지 설치 명령어 "pip install aws-lambda-powertools" 입력 및 엔터 (2025.11.20 minjae)
# 참고 URL - https://claude.ai/chat/27384cf9-7899-4dd6-9bde-12f1245c7da0
from aws_lambda_powertools.utilities.typing import LambdaContext
from queue import Queue, Empty   # 자료구조 queue (deque 기반)

import json         # json 데이터 처리
import threading    # 멀티스레드 패키지
import time         # 챗봇 답변 시간 계산

# 마스터 데이터 유효성 검사 대상 리스트
valid_targets = [ chatbot_helper._buttons,
                  chatbot_helper._itemList,
                  chatbot_helper._autoCADInfos,
                  chatbot_helper._revitInfos,
                  chatbot_helper._navisworksManageInfos,
                  chatbot_helper._infraWorksInfos,
                  chatbot_helper._civil3DInfos,
                  chatbot_helper._revitBoxInfos,
                  chatbot_helper._cadBoxInfos,
                  chatbot_helper._energyBoxInfos,
                  chatbot_helper._accountInfos,
                  chatbot_helper._etcInfos ]

masterEntity = MasterEntity(valid_targets)   # 마스터 데이터 싱글톤(singleton) 클래스 객체
kakaoResponseFormatter = KakaoResponseFormatter(masterEntity.get_master_datas)   # 스킬 응답 템플릿 json 포맷 클래스 객체

# thread_local = threading.local()   # 스레드마다 독립적으로 보관할 값 저장소

# --------------------- 메인 핸들러 (handler) ---------------------

def handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:
    """
    Description: 아마존 웹서비스 람다 함수(AWS Lambda Function) 실행 진입점
                 람다(Lambda)가 사용자로 부터 실행명령을 받았을 때, 실행되는 메인 핸들러 (handler)
                 파이썬 또는 C/C++ 프로그래밍 언어에서 main 함수와 같은 역할.

    Parameters: event - 카카오톡 채팅방에 사용자가 입력한 채팅 정보 (event['body']: 카카오톡 채팅방 실제 채팅 정보 저장된 변수)
                context - 아마존 웹서비스 람다 함수(AWS Lambda Function)에 속한 메타데이터 객체 (metadata)
        
    Returns: 카카오톡 서버로 전송할 json format 형식 데이터
    """

    kakao_request = None   # 카카오톡 채팅방 실제 채팅 정보
    user_id = None         # 카카오톡 채팅 입력 사용자 아이디
    file_path = None       # 사용자별 (user_id) 임시 로그 파일 상대 경로

    res_queue = None    # 챗봇 답변 내용 포함된 큐 객체
    err_queue = None    # 챗봇 오류 내용 포함된 큐 객체

    response = None     # 챗봇 답변 내용
    
    start_time = time.time()    # 메인 핸들러 (handler) 시작 시간 - 챗봇 응답 시간 계산 용도
    
    try:
        # logger.info(f"[테스트] event 클래스 타입 - {type(event)}")
        # logger.info(f"[테스트] context 클래스 타입 - {type(context)}")

        kakao_request = parse_event(event)   # 1) event[chatbot_helper._body] 저장된 데이터 json 파싱 (parsing)
        logger.info("[테스트] event['body'] 저장된 데이터 json 파싱 (parsing) 완료!")

        if True == is_warmup_request(kakao_request):   # 2) AWS Lambda Function 가상 컨테이너 warmup 요청 시 빠르게 응답 후 종료
            logger.info("[테스트] [coldstart -> warmup] AWS Lambda Function 가상 컨테이너 warmup 요청 - 완료!")
            return lambda_response_format({"message": "container-warmup OK!"})

        user_id = kakao_request[chatbot_helper._userRequest][chatbot_helper._user][chatbot_helper._id]   # 3) 카카오톡 채팅 입력 사용자 아이디 추출
        logger.info(f"[테스트] 채팅 입력 사용자 아이디: {user_id}")

        # 4) /tmp 폴더 하단 사용자별 (user_id) 임시 로그 파일 상대 경로
        file_path = f"{chatbot_helper._tmp}{chatbot_helper._user}_{chatbot_helper._id}{user_id}_{chatbot_helper._chatbot_file_name}"
        aws.create_tmp_file(file_path)

        # 5) 스레드 간 데이터 전달할 큐 생성
        res_queue = Queue()
        err_queue = Queue()

        start_response_thread(kakao_request, res_queue, err_queue, file_path)   # 6) 응답 생성 작업 스레드 시작

        response = wait_for_response(start_time, res_queue, err_queue)   # 7) 응답 대기 (챗봇 응답 제한 시간 초과 포함)

        if None is response:   # 8) 챗봇 응답 제한 시간 초과한 경우
            logger.warning("[테스트] 챗봇 응답 제한 시간 5초 초과 발생 - 재요청 응답 메세지 반환")
            return lambda_response_format(
                kakaoResponseFormatter.timeover_quickReplies(),
                status_code=chatbot_helper._statusCode_success,   # 카카오톡 서버로 재요청 응답 메세지 전송하기 위해 HTTP 응답 상태 코드 200 전송
            )

        logger.info("[테스트] 챗봇 응답 생성 완료 - 정상 응답 메세지 반환")
        return lambda_response_format(response)   # 9) 챗봇 정상 응답 메세지 반환

    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"[테스트] 데이터 유효성 오류 - {str(e)}", exc_info=True)
        return lambda_response_format(error_payload_format(str(e)))
    except Exception as e:
        # logger.critical("[테스트] 시스템 오류 - %s" %str(e))   # str(e) - Exception 클래스 객체 e 문자열 변환 (문자열로 변환 안할시 챗봇에서 스킬서버 오류 출력되면서 챗봇이 답변도 안하고 장시간 멈춤 상태 발생.)
        logger.critical(f"[테스트] 시스템 오류 - {str(e)}", exc_info=True)
        return lambda_response_format(error_payload_format(str(e)))
    
# --------------------- 실제 챗봇 응답 처리 (스레드 내부) ---------------------

def chatbot_response(kakao_request: dict[str, Any], res_queue: Queue, file_path: str) -> None:
    """
    Description: 챗봇 답변 요청 및 큐 객체 res_queue 답변 내용 추가

    Parameters: kakao_request - 카카오톡 채팅방 실제 채팅 정보
                res_queue - 챗봇 답변 내용 포함된 큐 객체
                file_path - 아마존 웹서비스 람다 함수(AWS Lambda Function) -> 사용자별 (user_id) 임시 로그 텍스트 파일 상대 경로 - (예시) '/tmp/user_id-1b2bfc8caf85a5dff8fadd1bf4cc70125b533fea7b665d0cdb0fb493a135e94b4d_chatbot.txt'

                * 참고
                /tmp 임시 폴더(스토리지) - 아마존 웹서비스 람다 함수(AWS Lambda Function)에서 파일을 저장할 수 있는 임시 로컬 스토리지 영역
                실행 결과(Execution results)는 람다 함수(Lambda Function) 콘솔 "테스트" 탭에서 함수 실행 성공 여부, 실행 결과, 임시 로그 확인 가능
                참고 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/configuration-ephemeral-storage.html#configuration-ephemeral-storage-use-cases
                참고 2 URL - https://inpa.tistory.com/entry/AWS-%F0%9F%93%9A-%EB%9E%8C%EB%8B%A4-tmp-%EC%9E%84%EC%8B%9C-%EC%8A%A4%ED%86%A0%EB%A6%AC%EC%A7%80-%EC%82%AC%EC%9A%A9-%EB%B0%A9%EB%B2%95

    Returns: 없음.
    """

    # TODO: 아래 주석친 코드 필요시 참고 (2025.11.27 minjae)
    # if False == hasattr(thread_local, "prev_userRequest_msg"):
    #     logger.info(f"[테스트] thread_local - prev_userRequest_msg 속성 초기화 완료!")
    #     setattr(thread_local, "prev_userRequest_msg", None)   # 이전 사용자 입력 채팅 메세지 (챗봇 응답 제한 시간 5초 초과시 응답 재요청 할 때 사용)
    #     thread_local.prev_userRequest_msg = None
        
    prev_userRequest_msg = None   # 이전 사용자 입력 채팅 메세지 (챗봇 응답 제한 시간 5초 초과시 응답 재요청 할 때 사용)
    userRequest_msg = kakao_request[chatbot_helper._userRequest][chatbot_helper._utterance]   # 사용자 입력 채팅 메세지 가져오기
    
    try:
        # logger.info(f"[테스트] kakao_request 클래스 타입 - {type(kakao_request)}")
        # logger.info(f"[테스트] res_queue 클래스 타입 - {type(res_queue)}")
        # logger.info(f"[테스트] file_path 클래스 타입 - {type(file_path)}")

        # 챗봇 응답 제한 시간 5초 초과시 응답 재요청 기능 구현
        # 참고 URL - https://claude.ai/chat/d550ac84-5c0c-4805-a600-9fdfd1236714
        if chatbot_helper._done_thinking == userRequest_msg:   # 시간 5초 초과시 응답 재요청
            logger.info(f"[테스트] userRequest_msg - {userRequest_msg}")

            prev_userRequest_msg = aws.read_tmp_file(file_path)
            
            if len(prev_userRequest_msg.split()) >= EnumValidator.EXISTENCE.value:
                # text = getattr(thread_local, "prev_userRequest_msg")
                logger.info(f"[테스트] 응답 재요청 채팅 메세지 - {prev_userRequest_msg}")

                response_data = kakaoResponseFormatter.get_response(prev_userRequest_msg)
                res_queue.put(response_data[chatbot_helper._payload])
                # res_queue.put(kakaoResponseFormatter.simple_text(prev_userRequest_msg))
                
                aws.write_tmp_file(file_path, "")
            return

        if EnumValidator.VALIDATION_ERROR == masterEntity.get_isValid:   # 마스터 데이터 유효성 검사 결과 - 오류.
            raise ValueError("마스터 데이터 유효성 검사 결과 - 오류.")
        
        if EnumValidator.NOT_EXISTENCE == masterEntity.get_isValid:   # 마스터 데이터 유효성 검사 결과 - 데이터 존재 안 함.
            raise ValueError("마스터 데이터 유효성 검사 결과 - 데이터 존재 안 함.")
        
        if EnumValidator.EXISTENCE == masterEntity.get_isValid:   # 마스터 데이터 유효성 검사 결과 - 성공.
            response_data = kakaoResponseFormatter.get_response(userRequest_msg)
            # setattr(thread_local, "prev_userRequest_msg", userRequest_msg)

            aws.write_tmp_file(file_path, "")
            
            levelNo = response_data[chatbot_helper._meta_data][chatbot_helper._levelNo]
            displayName = response_data[chatbot_helper._meta_data][chatbot_helper._displayName]
            logger.info(f"({levelNo}: {displayName} - 사용자 입력 채팅 정보: '{userRequest_msg}')")

            aws.write_tmp_file(file_path, userRequest_msg)

            # time.sleep(5)   # 테스트 - 5초 대기
            res_queue.put(response_data[chatbot_helper._payload])
            return

        raise Exception("시스템 내부 오류!")

    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"[테스트] 데이터 유효성 오류 - {str(e)}", exc_info=True)
        res_queue.put(error_payload_format(str(e)))
        raise    # raise 사용시 함수 chatbot_response 발생한 현재 예외 다시 발생시켜서 함수 chatbot_response 호출한 상위 코드 블록 전달
    except Exception as e:
        logger.critical(f"[테스트] 시스템 오류 - {str(e)}", exc_info=True)
        res_queue.put(error_payload_format(str(e)))
        raise    # raise 사용시 함수 chatbot_response 발생한 현재 예외 다시 발생시켜서 함수 chatbot_response 호출한 상위 코드 블록 전달

# --------------------- 이벤트 파싱 ---------------------

def parse_event(event: dict[str, Any]) -> dict[str, Any]:
    """
    Description: 카카오톡 채팅방 실제 채팅 정보 (event[chatbot_helper._body]) 저장된 데이터 json 파싱 (parsing)
                 json 파싱 (parsing) 의미: json 문자열 -> dict 객체 변환 처리

    Parameters: event - 카카오톡 채팅방에 사용자가 입력한 채팅 정보 (event['body']: 카카오톡 채팅방 실제 채팅 정보 저장된 변수)

    Returns: json 파싱 (parsing) 완료된 카카오톡 채팅방 실제 채팅 정보
    """

    try:
        # 키(key) 누락 체크 - event['body']가 존재하지 않는 경우
        # 콜드 스타트(coldstart)인 경우 제외 
        # 참고 URL - https://chatgpt.com/c/687a0180-e2bc-8010-9a19-90695a1bf477
        if chatbot_helper._body not in event: 
            raise KeyError(f"카카오톡 채팅방 실제 채팅 정보 저장된 변수 event['body'] - '{chatbot_helper._body}' 키 값 존재 안 함.")

        event_body_obj = event[chatbot_helper._body]

        # logger.info("[테스트] 사용자 입력 채팅 정보 - %s" %event['body'])
        logger.info(f"[테스트] 사용자 입력 채팅 정보 - {event_body_obj}")

        # 아래와 같은 오류 메시지 출력으로 인해 메서드 json.loads 사용해서 json 문자열 -> dict 객체 변환 처리 (2025.07.21 minjae)
        # 오류 메시지 - string indices must be integers, not 'str'
        # 참고 URL - https://docs.python.org/ko/3.13/library/json.html
        # 참고 2 URL - https://0pen3r.tistory.com/200
        # 참고 3 URL - https://kim-jong-hyun.tistory.com/148
        # 참고 4 URL - https://chatgpt.com/c/687d89d3-ab18-8010-a0ea-03039b64c94e
        # 참고 5 URL - https://wikidocs.net/126088
        # 참고 6 URL - https://chasuyeon.tistory.com/entry/AWS-Lambda%EC%97%90%EC%84%9C-event%EC%99%80-body-%EA%B0%9D%EC%B2%B4-%EA%B0%9C%EB%85%90#1%EF%B8%8F%E2%83%A3_event_%EA%B0%9D%EC%B2%B4%EB%9E%80_%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80?
        # event_body = json.loads(event[chatbot_helper._body])

        if True == isinstance(event_body_obj, str): return json.loads(event_body_obj)   # 인스턴스 event_body_obj 데이터 타입 str인 경우
        # elif True == isinstance(event_body_obj, dict): return event_body_obj   # 인스턴스 event_body_obj 데이터 타입 dict인 경우
        raise TypeError("event['body'] 데이터 타입 오류")

    except json.JSONDecodeError as e:
        logger.error(f"[테스트] event['body'] json 파싱 오류 - {str(e)}", exc_info=True)
        raise
    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"[테스트] 데이터 유효성 오류 - {str(e)}", exc_info=True)
        raise
    except Exception as e:
        logger.critical(f"[테스트] 시스템 오류 - {str(e)}", exc_info=True)
        raise

def is_warmup_request(event_body: dict[str, Any]) -> bool:
    """
    Description: 아마존 웹서비스 람다 함수(AWS Lambda Function) 가상 컨테이너 웜업 (warmup) 요청 여부 확인

    Parameters: event_body - json 파싱 (parsing) 완료된 카카오톡 채팅방 실제 채팅 정보

    Returns: 가상 컨테이너 웜업 (warmup) 요청 여부 [True - 웜업 (warmup) / False - 콜드 스타트(coldstart)]
    """

    try:
        # 키(key) 누락 체크 - event_body['action']가 존재하지 않는 경우
        # 참고 URL - https://chatgpt.com/c/687a0180-e2bc-8010-9a19-90695a1bf477
        if chatbot_helper._action not in event_body:
            raise KeyError(f"가상 컨테이너 웜업 (warmup) 요청 여부 확인 event_body['action'] - '{chatbot_helper._action}' 키 값 존재 안 함.")
        return chatbot_helper._warmup_request in event_body[chatbot_helper._action]   # 콜드 스타트(coldstart)인 경우 - 아마존 웹서비스 람다 함수(AWS Lambda Function) 초기 응답 속도 느림 콜드 스타트(coldstart) 현상

    except (KeyError, ValueError, TypeError) as e:
        logger.error(f"[테스트] 데이터 유효성 오류 - {str(e)}", exc_info=True)
        return False
    except Exception as e:
        logger.critical(f"[테스트] 시스템 오류 - {str(e)}", exc_info=True)
        return False

# --------------------- 스레드 실행 래퍼 ---------------------

def thread_wrapper(target: Callable[..., Any], args: tuple[Any, ...], err_queue: Queue) -> None:
    """
    Description: 작업 스레드 내부 발생 예외 -> err_queue 전달

    Parameters: target - 작업 스레드 실행 대상 함수 (chatbot_response)
                args - 작업 스레드 실행 대상 함수 (chatbot_response) 동작하기 위해 필요한 인자값 - kakao_request: dict[str, Any], res_queue: Queue, file_path: str
                res_queue - 챗봇 답변 내용 포함된 큐 객체
                err_queue - 챗봇 오류 내용 포함된 큐 객체

                thread_wrapper 함수의 경우 예외만 err_queue 전달 (err_queue.put(str(e)))

    Returns: 없음.
    """

    try:
        target(*args)   # chatbot_response(kakao_request, res_queue, file_path) 함수 호출과 같은 의미

    except Exception as e:
        logger.critical(f"[테스트] 작업 스레드 오류 - {str(e)}", exc_info=True)
        err_queue.put(str(e))
    
# --------------------- 주요 로직 함수 ---------------------

def start_response_thread(kakao_request: dict[str, Any], res_queue: Queue, err_queue: Queue, file_path: str) -> threading.Thread:
    """
    Description: 챗봇 답변 전용 작업 스레드 시작

    Parameters: kakao_request - 카카오톡 채팅방 실제 채팅 정보
                res_queue - 챗봇 답변 내용 포함된 큐 객체
                err_queue - 챗봇 오류 내용 포함된 큐 객체
                file_path - 아마존 웹서비스 람다 함수(AWS Lambda Function) -> 사용자별 (user_id) 임시 로그 텍스트 파일 상대 경로 - (예시) '/tmp/user_id-1b2bfc8caf85a5dff8fadd1bf4cc70125b533fea7b665d0cdb0fb493a135e94b4d_chatbot.txt'

    Returns: 챗봇 답변 전용 작업 스레드 객체
    """

    worker = threading.Thread(target=thread_wrapper,
                              args=(
                                chatbot_response,   # 작업 스레드 실행 대상 함수
                                (kakao_request, res_queue, file_path),   # chatbot_response 함수 실행시 필요 인자
                                err_queue   # 챗봇 오류 전달 전용 큐
                              ),
                              daemon=True)   # 작업 스레드 함수 연결 (daemon=True - 데몬 스레드 생성)
    worker.start()
    return worker

def wait_for_response(start_time: float, res_queue: Queue, err_queue: Queue) -> dict[str, Any] | None:
    """
    Description: 챗봇 답변 또는 오류 대기 (응답 제한 시간 3.5초 이내)

    Parameters: start_time - 메인 핸들러 (handler) 시작 시간 (챗봇 응답 시간 계산 용도)
                res_queue - 챗봇 답변 내용 포함된 큐 객체
                err_queue - 챗봇 오류 내용 포함된 큐 객체

                Blocking - 호출된 함수가 자신이 할 일을 모두 마칠 때까지 제어권을 계속 가지고서 호출한 함수에게 바로 돌려주지 않는 것.
                Non-Blocking - 호출된 함수가 자신이 할 일을 채 마치지 않았더라도 바로 제어권을 건네주어 (return) 호출한 함수가 다른 일을 진행할 수 있도록 해주는 것.

    Returns: response - 챗봇 답변 내용
    """

    while(time.time() - start_time < chatbot_helper._time_limit):   # 챗봇 응답 시간 3.5초 이내인 경우

        try:   # 오류 큐 우선 확인 (err_queue)
            err_response = err_queue.get_nowait()   # get(block=False) 함수와 비슷한 기능 수행 - 오류 큐 객체 아이템 없을 때 Non-Blocking 처리 (아이템 즉시 반환 또는 아이템 없을 시 즉시 Empty 예외 처리) 및 즉시 오류 큐 객체 아이템 가져오기 (오류 큐 객체 아이템 없이 비어있는지 확인하고, 비어있는 경우 즉시 다른 작업 수행해야 할 때 사용.)
            err_queue.task_done()   # 오류 큐 작업 완료
            raise Exception(f"작업 스레드 오류: {err_response}")
        except Empty:   # 오류 큐 객체 err_queue 아이템 없는 경우 즉시 Empty 예외 처리
            pass

        try:   # 응답 큐 확인 (res_queue)
            response = res_queue.get(timeout=chatbot_helper._polling_interval)   # (block=True) - 응답 큐 객체 아이템 없을 때 최대 0.01초 동안 Blocking 처리 (현재 작업 스레드 멈추고, 아이템 추가될 때까지 대기) 및 응답 큐 객체 아이템 가져오기 (응답 큐 객체 아이템 들어올 때까지 안정적으로 처리하고 싶을 때 사용.)
            res_queue.task_done()   # 응답 큐 작업 완료
            return response
        except Empty:   # 최대 0.01초 초과 후 응답 큐 객체 res_queue 아이템 없는 경우 Empty 예외 처리
            continue

    return None

def lambda_response_format(payload: dict[str, Any], status_code: int = chatbot_helper._statusCode_success) -> dict[str, Any]:
    """
    Description: 카카오톡 서버로 전송할 API Gateway 규격에 맞는 json format 형식 데이터 리턴

    Parameters: payload - 카카오 json 포맷 기반 챗봇 답변 내용 (페이로드)
                status_code - HTTP 응답 상태 코드 값 (예) 2XX - 성공 / 4XX - 클라이언트 오류 / 5XX - 서버 오류 (default value parameter)

    Returns: 카카오톡 서버로 전송할 json format 형식 데이터
    """

    return {
        "statusCode": status_code,
        "body": json.dumps(payload, ensure_ascii=False),
        "headers": { "Access-Control-Allow-Origin": "*" },
    }

def error_payload_format(msg: str) -> dict[str, Any]:
    """
    Description: 챗봇 오류 내용 리턴

    Parameters: msg - 오류 내용

    Returns: 오류 메세지 json 포맷
    """

    return kakaoResponseFormatter.error_text(f"{chatbot_helper._error_title}\n{msg}\n{chatbot_helper._error_techSupport}")

"""
*** 참고 ***
*** 아마존 웹서비스 문서 ***
* LambdaContext 클래스
참고 URL - https://docs.aws.amazon.com/powertools/python/latest/utilities/typing/
참고 2 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-context.html
참고 3 URL - https://jibinary.tistory.com/551

* 콜드 스타트(coldstart)
아마존 웹서비스 람다 함수(AWS Lambda Function) 초기 응답 속도 느림(coldstart) 개선 (2025.07.16 minjae)
참고 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/provisioned-concurrency.html
참고 2 URL - https://jeonghwan-kim.github.io/dev/2021/04/01/aws-lambda-cold-start.html  
참고 3 URL - https://blog.naver.com/chandong83/221975639559
참고 4 URL - https://wave35.tistory.com/150
참고 5 URL - https://chatgpt.com/c/687872f0-2ad0-8010-9eb3-2b4e8dba2ba8
참고 6 URL - https://chatgpt.com/c/6878b74a-b478-8010-b277-313b21eeceee

* 아마존 웹서비스 람다 함수(AWS Lambda Function)와 EventBridge 조합으로 일정 시간마다 함수 handler 호출하여 초기 응답 속도 느림(coldstart) 개선 (2025.07.18 minjae)
참고 URL - https://docs.aws.amazon.com/ko_kr/eventbridge/latest/userguide/eb-run-lambda-schedule.html
참고 2 URL - https://docs.aws.amazon.com/ko_kr/AmazonCloudWatch/latest/logs/example_cross_LambdaScheduledEvents_section.html
참고 3 URL - https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/lambda#readme
참고 4 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/with-eventbridge-scheduler.html
참고 5 URL - https://jimmy-ai.tistory.com/505
참고 6 URL - https://www.freeconvert.com/ko/time/utc-to-kst
참고 7 URL - https://chatgpt.com/c/687df65c-c718-8010-802f-8f8d03c81f5f
참고 8 URL - https://chatgpt.com/c/6886e63d-c67c-8010-9056-c578b981c95e
참고 9 URL - https://zamezzz.tistory.com/entry/Serverless-%EC%84%9C%EB%B9%84%EC%8A%A4-%EA%B0%9C%EB%B0%9C-6-Lambda-%EC%84%B1%EB%8A%A5-%EC%98%AC%EB%A6%AC%EA%B8%B0

* 아마존 웹서비스 람다 함수(AWS Lambda Function) API Gateway 오류 처리
참고 URL - https://docs.aws.amazon.com/ko_kr/apigateway/latest/developerguide/handle-errors-in-lambda-integration.html

* 페이로드 (payload)
참고 URL - https://ssue95.tistory.com/30

*** 파이썬 문서 ***
* threading.Thread
참고 URL - https://docs.python.org/ko/3/library/threading.html#thread-objects
참고 2 URL - https://mechacave.tistory.com/2
참고 3 URL - https://pybi.tistory.com/19

* 데몬 스레드 (daemon=True)
참고 URL - https://wikidocs.net/82581

* threading.local()
참고 URL - https://docs.python.org/ko/3.13/library/threading.html#thread-local-data
참고 2 URL - https://soundprovider.tistory.com/entry/python-Thread-Local-Data

* hasattr
참고 URL - https://docs.python.org/ko/3.10/library/functions.html#hasattr

* setattr
참고 URL - https://docs.python.org/ko/3.10/library/functions.html#setattr

* getattr
참고 URL - https://docs.python.org/ko/3.10/library/functions.html#getattr

* split
참고 URL - https://docs.python.org/3.6/library/stdtypes.html#string-methods

* isinstance
참고 URL - https://docs.python.org/ko/3.9/library/functions.html#isinstance
참고 2 URL - https://everywhere-data.tistory.com/entry/Python-isinstance-%ED%95%A8%EC%88%98-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%9E%90%EB%A3%8C%ED%98%95-%ED%99%95%EC%9D%B8%ED%95%98%EB%8A%94-%ED%95%A8%EC%88%98

* non-default value parameter, default value parameter
참고 URL - https://docs.python.org/ko/3/glossary.html#term-parameter
참고 2 URL - https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects

* Blocking vs Non-Blocking
Blocking - 호출된 함수가 자신이 할 일을 모두 마칠 때까지 제어권을 계속 가지고서 호출한 함수에게 바로 돌려주지 않는 것.
Non-Blocking - 호출된 함수가 자신이 할 일을 채 마치지 않았더라도 바로 제어권을 건네주어(return) 호출한 함수가 다른 일을 진행할 수 있도록 해주는 것.
참고 URL - https://exmemory.tistory.com/78

* 큐 (queue) except Empty:
참고 URL - https://docs.python.org/ko/dev/library/queue.html#queue.Empty

* json.loads - json 파싱 (parsing)
json 파싱 (parsing)은 json 형식의 문자열 (str)을 프로그래밍 언어에서 사용할 수 있는 객체 (dict 등등...)로 변환하는 과정이다.
참고 URL - https://docs.python.org/ko/3/library/json.html
참고 2 URL - https://kyeong-hoon.tistory.com/226

*** 기타 문서 ***
* HTTP 응답 상태 코드
참고 URL - https://developer.mozilla.org/ko/docs/Web/HTTP/Reference/Status
참고 2 URL - https://namu.wiki/w/HTTP/%EC%9D%91%EB%8B%B5%20%EC%BD%94%EB%93%9C
"""