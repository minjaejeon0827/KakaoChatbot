"""
* 아마존 웹서비스 람다 함수 (AWS Lambda function) 실행 진입점 (handler)
코드 리뷰 참고 URL - https://chatgpt.com/c/691e9f6e-3940-832a-afda-92c53ae4b49a

* 아마존 웹서비스 (AWS) 다중인증 (MFA는 Multi-Factor Authentication) 등록 방법 및 모바일 어플 Google Authenticator 설치 및 사용 방법
참고 URL - https://happy-jjang-a.tistory.com/223

* lambda_function.py 파이썬 스크립트 파일 소스 코드 리팩토링 (2025.09.30 minjae)
참고 URL - https://claude.ai/chat/786c45b9-f744-4fcf-950a-bcc178417e1c
"""

# 1. 공통 모듈 먼저 import
from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트

# 2. singleton 모듈을 log 모듈 보다 먼저 import
from modules.singleton import MasterEntity   # 싱글톤 (singleton) 패턴
from modules.chatbot_enum import EnumValidator   # 데이터 유효성 검사

# 3. singleton 모듈이 먼저 초기화된 후 log 모듈 import 
from utils.log import logger   # 챗봇 전역 로그 객체 (logger)

# 4. Type Hints class Any import
from typing import Any

# 5. 나머지 모듈 import
from modules.kakao import KakaoResponseFormatter   # 카카오 스킬 응답 템플릿 json 포맷
# 아래처럼 LambdaContext 클래스 import 처리하기 위해 비쥬얼스튜디오코드 (VSCode) cmd 터미널창 열고 -> 파이썬 패키지 설치 명령어 "pip install aws-lambda-powertools" 입력 및 엔터 (2025.11.20 minjae)
# 참고 URL - https://claude.ai/chat/27384cf9-7899-4dd6-9bde-12f1245c7da0
from aws_lambda_powertools.utilities.typing import LambdaContext

import json         # json 데이터 처리
import threading    # 멀티스레드 패키지
import time         # 챗봇 답변 시간 계산
import queue as q   # 자료구조 queue (deque 기반)
import os           # 답변 결과 임시 로그 텍스트 파일 ('/tmp/botlog.txt') 저장

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

prev_userRequest_msg = None   # 이전 사용자 입력 채팅 메세지 (챗봇 응답 시간 5초 초과시 응답 재요청 할 때 사용)

def handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:
    """
    Description: 아마존 웹서비스 람다 함수(AWS Lambda function) 실행 진입점
                 람다(Lambda)가 사용자로 부터 실행명령을 받았을 때, 실행되는 메인 함수(handler)이다.
                 파이썬 또는 C/C++ 프로그래밍 언어에서 main 함수와 같은 역할이다.

    Parameters: event - 카카오톡 채팅방에 사용자가 입력한 채팅 정보 (event['body']: 카카오톡 채팅방 실제 채팅 정보 저장된 변수)
                context - 아마존 웹서비스 람다 함수 (AWS Lambda function)에 속한 메타데이터 (metadata) 객체
        
    Returns: 카카오톡 서버로 전송할 json format 형식 데이터
    """

    res_queue = None    # 챗봇 답변 내용 담을 큐(queue) 객체 .put(), .get() 메서드 사용 가능 
    run_flag = False    # 챗봇 응답 시간 5초 초과 여부
    start_time = time.time()    # 챗봇 응답 시간 계산하기 위해 메인 함수 (handler) 시작하는 시간을 변수 start_time에 저장 
    
    try:
        # logger.info(f"[테스트] event 클래스 타입 - {type(event)}")
        # logger.info(f"[테스트] context 클래스 타입 - {type(context)}")

        # 키(key) 누락 체크 - event['body']가 존재하지 않는 경우
        # 콜드 스타트 (ColdStart)인 경우 제외 
        # 참고 URL - https://chatgpt.com/c/687a0180-e2bc-8010-9a19-90695a1bf477
        if chatbot_helper._body not in event: 
            raise KeyError(f"카카오톡 채팅방 실제 채팅 정보 저장된 변수 event['body'] - '{chatbot_helper._body}' 키 값 존재 안 함.")
        
        # logger.info("[테스트] 사용자 입력 채팅 정보 - %s" %event['body'])
        logger.info(f"[테스트] 사용자 입력 채팅 정보 - {event[chatbot_helper._body]}")

        # 아래와 같은 오류 메시지 출력으로 인해 메서드 json.loads 사용해서 json 문자열 -> dict 객체 변환 처리 (2025.07.21 minjae)
        # 오류 메시지 - string indices must be integers, not 'str'
        # 참고 URL - https://docs.python.org/ko/3.13/library/json.html
        # 참고 2 URL - https://0pen3r.tistory.com/200
        # 참고 3 URL - https://kim-jong-hyun.tistory.com/148
        # 참고 4 URL - https://chatgpt.com/c/687d89d3-ab18-8010-a0ea-03039b64c94e
        # 참고 5 URL - https://wikidocs.net/126088
        event_body = json.loads(event[chatbot_helper._body])
        logger.info(f"[테스트] event_body['action'] - {event_body[chatbot_helper._action]}")
          
        if chatbot_helper._warmup_request in event_body[chatbot_helper._action]:   # 콜드 스타트 (ColdStart)인 경우 - 아마존 웹서비스 람다 함수 (AWS Lambda function) 초기 응답 속도 느림 콜드 스타트 (ColdStart) 현상  
            logger.info("[ColdStart -> WarmUp] AWS Lambda Function 컨테이너 초기화 - 완료!")
            return

        kakao_request = event_body

        file_name = chatbot_helper._tmp + chatbot_helper._chatbot_file_name
        
        if False == os.path.exists(file_name): dbReset(file_name)
        else: logger.info("임시 로그 텍스트 파일('/tmp/botlog.txt') 존재 여부 - File Exists!")   

        res_queue = q.Queue()

        request_respond = threading.Thread(target=chatbot_response,
                                           args=(kakao_request, res_queue, file_name))
        
        request_respond.start()

    except (KeyError, ValueError, TypeError) as e:
        valid_error_msg = str(e)
        logger.error(f"[테스트] 데이터 유효성 오류 - {valid_error_msg}", exc_info=True)
    except Exception as e:
        sys_error_msg = str(e)   # str() 함수 사용해서 Exception 클래스 객체 e를 문자열로 변환 및 오류 메시지 변수 sys_error_msg에 할당 (문자열로 변환 안할시 챗봇에서 스킬서버 오류 출력되면서 챗봇이 답변도 안하고 장시간 멈춤 상태 발생.)
        # logger.critical('[테스트] 시스템 오류 - %s' %sys_error_msg)
        logger.critical(f"[테스트] 시스템 오류 - {sys_error_msg}", exc_info=True)
    finally:
        if None is res_queue:   # 챗봇 답변 내용 담을 큐(queue) 객체 res_queue 값이 None인 경우
            logger.info("[테스트] handler - finally 강제 종료 - [사유] 큐(queue) 객체 res_queue 생성 안 함.")
            return
             
        while(time.time() - start_time < chatbot_helper._time_limit):   # 챗봇 응답 시간 3.5초 이내인 경우
            if False == res_queue.empty():
                response = res_queue.get()  # 큐(queue) 객체 res_queue 에서 데이터 가져오기
                res_queue.task_done()   # 큐(queue) 객체 res_queue 에서 가져온 데이터에 대한 작업 완료
                logger.info(f"[테스트] 카카오 json 포맷 기반 챗봇 답변 내용 - {response}")

                run_flag = True
                break
            time.sleep(chatbot_helper._polling_interval)
 
        if False == run_flag:   # 챗봇 응답 시간 5초 초과한 경우     
            # response = kakao.timeOver_quickReplies(chatbot_helper._done_thinking)
            response = kakaoResponseFormatter.timeOver_quickReplies()

        res_msg = json.dumps(response)
        # logger.info("[테스트] 챗봇 답변 채팅 정보 - %s" %res_msg)
        logger.info(f"[테스트] 챗봇 답변 채팅 정보 - {res_msg}")

        return {   # 카카오톡 서버로 전송할 json format 형식 데이터 리턴
            'statusCode': chatbot_helper._statusCode_success,
            'body': res_msg,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            }
        }

def chatbot_response(kakao_request: dict[str, Any], res_queue: q.Queue, file_name: str) -> None:
    """
    Description: 챗봇 답변 요청 및 큐 (queue) 객체 res_queue 답변 내용 추가

    Parameters: kakao_request - 카카오톡 채팅방 실제 채팅 정보
                res_queue - 챗봇 답변 내용 담을 큐(queue) 객체
                file_name - 아마존 웹서비스 람다 함수(AWS Lambda function) -> 임시 로그 텍스트 파일('/tmp/botlog.txt') 상대 경로

                *** 참고 ***
                /tmp 임시 디렉터리(스토리지) - 아마존 웹서비스 람다 함수(AWS Lambda function)에서 파일을 저장할 수 있는 임시 로컬 스토리지 영역
                실행 결과(Execution results)는 람다 함수(Lambda Function) 콘솔 "테스트" 탭에서 함수 실행 성공 여부, 실행 결과, 임시 로그 확인 가능
                참고 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/configuration-ephemeral-storage.html#configuration-ephemeral-storage-use-cases
                참고 2 URL - https://inpa.tistory.com/entry/AWS-%F0%9F%93%9A-%EB%9E%8C%EB%8B%A4-tmp-%EC%9E%84%EC%8B%9C-%EC%8A%A4%ED%86%A0%EB%A6%AC%EC%A7%80-%EC%82%AC%EC%9A%A9-%EB%B0%A9%EB%B2%95

    Returns: 없음.
    """

    # global masterEntity   # 챗봇 마스터 데이터 싱글톤 객체
    masterEntity   # 챗봇 마스터 데이터 싱글톤 객체 - 변수(masterEntity)에 저장된 값을 변경하거나 새로운 값을 대입하지 않고 단순히 값을 가져다가 쓰기(참조)만 하는 경우 global 키워드 사용할 필요 없음.

    # 함수 chatbot_response 안에서 전역 변수(prev_userRequest_msg)에 저장된 값을 변경하거나 새로운 값을 대입 하기 위해 파이썬 전역변수 키워드 global 사용. (global prev_userRequest_msg) (2025.09.30 minjae)
    # 참고 URL - https://docs.python.org/ko/3/reference/simple_stmts.html#the-global-statement
    # 참고 2 URL - https://dojang.io/mod/page/view.php?id=2364
    # 참고 3 URL - https://wikidocs.net/62
    # 참고 4 URL - https://youtu.be/M_wLOmNRBN8?si=ZOg8cPmmaSdqyyL2
    global prev_userRequest_msg   # 이전 사용자 입력 채팅 메세지 (챗봇 응답 시간 5초 초과시 응답 재요청 할 때 사용)
 
    text = None         # 챗봇 답변 내용
    response_data = None  # 카카오 json format 형식 기반 챗봇 답변 내용 + 특정 마스터 데이터
    # response = None       # 카카오 json format 형식 기반 챗봇 답변 내용
    # master_data = None    # 특정 마스터 데이터
    userRequest_msg = kakao_request[chatbot_helper._userRequest][chatbot_helper._utterance]   # 사용자 입력 채팅 메세지 가져오기 
    
    try:
        # logger.info(f"[테스트] kakao_request 클래스 타입 - {type(kakao_request)}")
        # logger.info(f"[테스트] res_queue 클래스 타입 - {type(res_queue)}")
        # logger.info(f"[테스트] file_name 클래스 타입 - {type(file_name)}")

        # 챗봇 응답 시간 5초 초과시 응답 재요청 기능 구현 
        # 참고 URL - https://claude.ai/chat/d550ac84-5c0c-4805-a600-9fdfd1236714
        if chatbot_helper._done_thinking in userRequest_msg:   # 시간 5초 초과시 응답 재요청
            logger.info(f"[테스트] userRequest_msg - {userRequest_msg}")
            with open(file_name) as f:
                last_update = f.read()
                logger.info(f"[테스트] last_update - {last_update}")

            text = prev_userRequest_msg
            logger.info(f"[테스트] 응답 재요청 채팅 메세지 - {text}")
            # res_queue.put(kakao.simple_text(text))
            res_queue.put(kakaoResponseFormatter.simple_text(text))
            dbReset(file_name)

            # TODO: 추후 필요시 아래 주석친 코드 참고 (2025.09.12 minjae)
            # if len(last_update.split()) >= chatbot_helper._multiWord:   # 변수 last_update에 저장된 문자열을 공백('')단위로 분리한 단어들의 개수가 1개보다 많은 경우 (여러 단어로 구성)
            #     kind = last_update.split()[chatbot_helper._firstWord_Idx]    # 변수 last_update에 저장된 문자열을 공백('')단위로 분리한 첫 번째 단어 변수 kind에 저장 (예) ask, img 등등...

            #     if kind == "img":   # 변수 kind에 저장된 문자열이 'img'인 경우 
            #         text, prompt = last_update.split()[chatbot_helper._secondWord_Idx], last_update.split()[chatbot_helper._thirdWord_Idx]   # 변수 last_update에 저장된 문자열 중 공백('')단위로 분리한 두 번째와 세 번째 단어 각각 text와 prompt에 저장
            #         logger.info(f"[테스트] /img - text (last_update.split()[chatbot_helper._secondWord_Idx]) - {text}")
            #         logger.info(f"[테스트] /img - prompt (last_update.split()[chatbot_helper._thirdWord_Idx]) - {prompt}")
            #         res_queue.put(kakao.simple_image(text,prompt))
            #         res_queue.put(kakaoResponseFormatter.simple_image(text,prompt))

            #     else:    # 변수 kind에 저장된 문자열이 'img' 아닌 경우 
            #         text = last_update[chatbot_helper._askPrefix_Len:]   # 변수 last_update에 저장된 문자열 중 다섯 번째 문자(last_update[chatbot_helper._askPrefix_Length:]) 부터 끝까지 변수 text에 저장 (숫자 4 의미 - "ask "(공백 '' 포함) 문자열 제거하고 나머지 텍스트 가져옴)
            #         logger.info(f"[테스트] /ask - text (last_update[4:]) - {text}")
            #         res_queue.put(kakao.simple_text(text))
            #         res_queue.put(kakaoResponseFormatter.simple_text(text))

            #     dbReset(file_name)

        # elif '/error'== userRequest_msg:   # 오류 테스트
        #     raise Exception("사유: 오류 테스트!")
        
        # 참고 - masterEntity.get_isValid.name - Enum 열거형 구조체 EnumValidator 멤버변수 이름
        elif EnumValidator.VALIDATION_ERROR == masterEntity.get_isValid:   # 데이터 유효성 검사 결과 오류인 경우
            raise ValueError("데이터 유효성 검사 오류.")
        
        elif EnumValidator.NOT_EXISTENCE == masterEntity.get_isValid:   # 마스터 데이터 유효성 검사 결과 실패한 경우
            raise ValueError("마스터 데이터 존재 안 함.")

        # elif True == masterEntity.get_isValid:   # 마스터 데이터 유효성 검사 결과 성공한 경우
        elif EnumValidator.EXISTENCE == masterEntity.get_isValid:   # 마스터 데이터 유효성 검사 결과 성공한 경우
            # response, master_data = kakao.get_response(userRequest_msg, masterEntity)
            # response_data = kakao.get_response(userRequest_msg, masterEntity)
            # TODO: 아래 코드 실행시 오류 메시지 "KakaoResponseFormatter.get_response() takes 2 positional arguments but 3 were given" 출력되어 코드 변경 처리 (2025.11.07 minjae)
            # (기존) response_data = kakaoResponseFormatter.get_response(userRequest_msg, masterEntity) -> (변경) response_data = kakaoResponseFormatter.get_response(userRequest_msg)
            # response_data = kakaoResponseFormatter.get_response(userRequest_msg, masterEntity)
            response_data = kakaoResponseFormatter.get_response(userRequest_msg)
            prev_userRequest_msg = userRequest_msg

            saveLog(file_name, f"({response_data[chatbot_helper._meta_data][chatbot_helper._levelNo]}: {response_data[chatbot_helper._meta_data][chatbot_helper._displayName]} - 사용자 입력 채팅 정보: '{userRequest_msg}')")

            # TODO: 추후 필요시 아래 주석친 코드 참고 (2025.09.12 minjae)
            # if response_data[chatbot_helper._meta_data] is not None:   # 특정 마스터 데이터 값이 존재하는 경우 (예) 아이템 카드 (basicCard, carousel) or 바로가기 그룹 (quickReplies) 
            #     saveLog(file_name, f"({response_data[chatbot_helper._meta_data][chatbot_helper._levelNo]}: {response_data[chatbot_helper._meta_data][chatbot_helper._displayName]} - 사용자 입력 채팅 정보: '{userRequest_msg}')")
            # else:   # 특정 마스터 데이터 값이 존재하지 않는 경우 (예) 아이템 카드 (basicCard, carousel) or 바로가기 그룹 (quickReplies) 
            #     saveLog(file_name, f"(etc: [기술지원 문의 제외 일반 문의] - 사용자 입력 채팅 정보: '{userRequest_msg}')")

            time.sleep(5)   # 테스트 - 5초 대기
            res_queue.put(response_data[chatbot_helper._format])

            # if master_data is not None:   # 특정 마스터 데이터 값이 존재하는 경우 (예) 아이템 카드 (basicCard, carousel) or 바로가기 그룹 (quickReplies) 
            #     saveLog(file_name, f"({master_data[chatbot_helper._levelNo]}: {master_data[chatbot_helper._displayName]} - 사용자 입력 채팅 정보: '{userRequest_msg}')")
            # else:   # 특정 마스터 데이터 값이 존재하지 않는 경우 (예) 아이템 카드 (basicCard, carousel) or 바로가기 그룹 (quickReplies) 
            #     saveLog(file_name, f"(etc: [기술지원 문의 제외 일반 문의] - 사용자 입력 채팅 정보: '{userRequest_msg}')")

            # # time.sleep(5)   # 테스트 - 5초 대기
            # res_queue.put(response)

        else: raise Exception("시스템 오류!")

        # TODO: 추후 필요시 아래 주석친 코드 참고 (2025.09.12 minjae)
        # else:
        #     empty_res = kakao.empty_response()
        #     empty_res = kakaoResponseFormatter.__empty_response()
        #     res_queue.put(empty_res)

    except (KeyError, ValueError, TypeError) as e:
        valid_error_msg = str(e)
        logger.error(f"[테스트] 데이터 유효성 오류 - {valid_error_msg}", exc_info=True)
        # res_queue.put(kakao.error_text(valid_error_msg))
        res_queue.put(kakaoResponseFormatter.error_text(f"{chatbot_helper._error_title}\n{valid_error_msg}\n{chatbot_helper._error_techSupport}"))        
        raise    # raise로 함수 chatbot_response의 현재 예외를 다시 발생시켜서 함수 chatbot_response 호출한 상위 코드 블록으로 넘김
    except Exception as e:
        sys_error_msg = str(e)
        logger.critical(f"[테스트] 시스템 오류 - {sys_error_msg}", exc_info=True)
        # res_queue.put(kakao.error_text(sys_error_msg))
        res_queue.put(kakaoResponseFormatter.error_text(f"{chatbot_helper._error_title}\n{sys_error_msg}\n{chatbot_helper._error_techSupport}"))
        raise    # raise로 함수 chatbot_response의 현재 예외를 다시 발생시켜서 함수 chatbot_response 호출한 상위 코드 블록으로 넘김

def dbReset(file_name: str) -> None:
    """
    Description: 임시 로그 초기화

    Parameters: file_name - 아마존 웹서비스 람다 함수 (AWS Lambda function) -> 임시 로그 텍스트 파일 ('/tmp/botlog.txt') 상대 경로

    Returns: 없음.
    """

    with open(file_name, 'w') as f:
        f.write("")

def dbSave(file_name: str, msg: str) -> None:
    """
    Description: 임시 로그 기록

    Parameters: file_name - 아마존 웹서비스 람다 함수 (AWS Lambda function) -> 임시 로그 텍스트 파일 ('/tmp/botlog.txt') 상대 경로
                msg - 로그 메시지

    Returns: 없음.
    """

    with open(file_name, 'w') as f:
        f.write(msg)

def saveLog(file_name: str, msg: str) -> None:
    """
    Description: 임시 로그 초기화 및 기록

    Parameters: file_name - 아마존 웹서비스 람다 함수 (AWS Lambda function) -> 임시 로그 텍스트 파일 ('/tmp/botlog.txt') 상대 경로
                msg - 로그 메시지

    Returns: 없음.
    """

    dbReset(file_name)   
    logger.info(f"[테스트] 임시 로그 텍스트 파일({file_name}) 로그 메시지 - {msg}")
    dbSave(file_name, msg)

"""
*** 참고 ***
*** 아마존 웹서비스 문서 ***
* LambdaContext 클래스
참고 URL - https://docs.aws.amazon.com/powertools/python/latest/utilities/typing/
참고 2 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-context.html
참고 3 URL - https://jibinary.tistory.com/551

* 콜드 스타트 (ColdStart)
아마존 웹서비스 람다 함수(AWS Lambda function) 초기 응답 속도 느림(Cold Start) 개선 (2025.07.16 minjae)
참고 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/provisioned-concurrency.html
참고 2 URL - https://jeonghwan-kim.github.io/dev/2021/04/01/aws-lambda-cold-start.html  
참고 3 URL - https://blog.naver.com/chandong83/221975639559
참고 4 URL - https://wave35.tistory.com/150
참고 5 URL - https://chatgpt.com/c/687872f0-2ad0-8010-9eb3-2b4e8dba2ba8
참고 6 URL - https://chatgpt.com/c/6878b74a-b478-8010-b277-313b21eeceee

* 아마존 웹서비스 람다 함수 (AWS Lambda function)와 EventBridge 조합으로 일정 시간마다 함수 handler 호출하여 초기 응답 속도 느림(Cold Start) 개선 (2025.07.18 minjae)
참고 URL - https://docs.aws.amazon.com/ko_kr/eventbridge/latest/userguide/eb-run-lambda-schedule.html
참고 2 URL - https://docs.aws.amazon.com/ko_kr/AmazonCloudWatch/latest/logs/example_cross_LambdaScheduledEvents_section.html
참고 3 URL - https://github.com/awsdocs/aws-doc-sdk-examples/tree/main/python/example_code/lambda#readme
참고 4 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/with-eventbridge-scheduler.html
참고 5 URL - https://jimmy-ai.tistory.com/505
참고 6 URL - https://www.freeconvert.com/ko/time/utc-to-kst
참고 7 URL - https://chatgpt.com/c/687df65c-c718-8010-802f-8f8d03c81f5f
참고 8 URL - https://chatgpt.com/c/6886e63d-c67c-8010-9056-c578b981c95e
"""