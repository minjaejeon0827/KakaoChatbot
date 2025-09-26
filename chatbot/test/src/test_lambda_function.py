# 아마존 웹서비스(AWS) 다중인증(MFA는 Multi-Factor Authentication) 등록 방법 및 모바일 어플 Google Authenticator 설치 및 사용 방법 
# 참고 URL - https://happy-jjang-a.tistory.com/223

###### 기본 정보 설정 단계 #######
# 참고사항
# 아마존 웹서비스(AWS) 활용할 때에는 FastAPI 개발자 로컬 웹서버를 따로 생성할 필요가 없으니까
# 패키지 "from fastapi import Request, FastAPI"를 불러올 필요가 없다.

import json         # 카카오톡 서버로 부터 받은 json 데이터 처리 패키지 json  
import threading    # 프로그램 안에서 동시에 작업하는 멀티스레드 패키지 "threading" 
import time         # ChatGPT 답변 시간 계산 패키지 "time" 
import queue as q   # 자료구조 queue(deque 기반) 패키지 "queue" 
import os           # 답변 결과를 테스트 파일로 저장할 때 경로 생성 패키지 "os" 
 
from commons import chatbot_helper   # 폴더 "commons" -> 챗봇 전용 도움말 텍스트  

# 폴더 "modules" 
from modules import kakao            # 카카오 API 전용 모듈    
from modules import openAI           # OpenAI 전용 모듈   
from modules import chatbot_logger           # 챗봇 로그 작성 모듈  
from modules import singleton        # 싱글톤(singleton) 패턴 전용 모듈   

# --------------------------------------------------------------------------------------------------------------------------------------

# 마스터 데이터 유효성 검사 대상 리스트 
valid_targets = [ chatbot_helper._buttons, 
                  chatbot_helper._items, 
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

masterEntity = singleton.MasterEntity(valid_targets)   # 챗봇 마스터 데이터 싱글톤 객체   

# --------------------------------------------------------------------------------------------------------------------------------------

# TODO: 필요시 아래 코드 가독성이 높은 함수 sum_of_even_numbers 참고해서 챗봇 프로그램 고도화 작업 진행 예정 (2025.08.08 minjae)
# def sum_of_even_numbers(numbers_list):
#   """
#   Calculate the sum of all even numbers in a given list.

#   Parameters:
#   numbers_list (list): A list of integers.

#   Returns:
#   int: The sum of all even numbers in the list.
#   """
#   even_numbers = [number for number in numbers_list if number % 2 == 0]
#   total_sum = sum(even_numbers)
#   return total_sum

# --------------------------------------------------------------------------------------------------------------------------------------

###### 메인 함수 단계 #######

# 람다(lambda)가 실행명령을 받았을 때, 실행되는 메인함수 handler
# 파이썬 또는 C/C++ 프로그래밍 언어에서 main 함수와 같은 역할을 한다.
# 또한 해당 함수는 event, context 라는 파라미터를 매개변수로 전달 받는다.
# 메인 함수
def handler(event, context):
    res_queue = None   # 챗봇 답변 내용 담을 큐 객체 .put(), .get() 메서드 사용 가능 
    run_flag = False   # 챗봇 응답 시간 5초 초과 여부 
    start_time = time.time()   # 답변/그림 응답 시간 계산하기 위해 답변/그림을 시작하는 시간을 변수 start_time에 저장 
    
    try: 
        # 카카오 정보 저장
        # json.loads 함수 호출 하여 JSON 문자열 -> Dictionary 객체 변환 처리 및
        # Dictionary 객체를 변수 kakao_request에 저장 
        # JSON 문자열 (예) '{"name": "홍길동", "birth": "0525", "age": 30}'
        # Dictionary 객체 (예) {'name': '홍길동', 'birth': '0525', 'age': 30}
        # 참고 URL - https://wikidocs.net/126088 
        # 카카오톡 채팅방 채팅 정보가 event 파라미터를 통해서 람다(lambda) 함수 handler 로 넘어온다.
        # event['body'] - 카카오톡 채팅방 채팅 정보가 들어있는 변수이다.

        # event['body']가 존재하지 않는 경우 - ColdStart(콜드 스타트)인 경우 제외 
        # 참고 URL - https://chatgpt.com/c/687a0180-e2bc-8010-9a19-90695a1bf477
        if chatbot_helper._body not in event: 
            raise KeyError("event['body'] 객체 KeyError 발생!")
        
        # logger._info("[테스트] 사용자 입력 채팅 정보 - %s" %event['body'])
        chatbot_logger.log_write(chatbot_logger._info, "[테스트] 사용자 입력 채팅 정보", event[chatbot_helper._body])

        # TODO: 아래와 같은 오류 메시지 출력으로 인해 메서드 json.loads 사용해서 (기존) json 문자열 -> (변경) json 형식의 Dictionary 객체 변환(파싱) 처리 (2025.07.21 minjae)
        # 오류 메시지 - string indices must be integers, not 'str'
        # 참고 URL - https://docs.python.org/ko/3.13/library/json.html
        # 참고 2 URL - https://0pen3r.tistory.com/200
        # 참고 3 URL - https://kim-jong-hyun.tistory.com/148
        # 참고 4 URL - https://chatgpt.com/c/687d89d3-ab18-8010-a0ea-03039b64c94e
        event_body = json.loads(event[chatbot_helper._body])   # JSON 문자열을 Dictionary 객체로 파싱
        chatbot_logger.log_write(chatbot_logger._info, "[테스트] event_body['action']", event_body[chatbot_helper._action])
        
        # ColdStart(콜드 스타트)
        # ColdStart는 아마존 웹서비스(AWS) 람다 함수(Lambda Function)가 처음 호출되거나 오랜 시간 동안 호출되지 않다가 다시 호출될 때 발생하는 초기화 과정이다.
        # ColdStart - 아마존 웹서비스(AWS) 람다 함수(Lambda Function) 초기 응답 속도 느림(Cold Start) 의미  
        # json 페이로드 형식
        # {
        #   "body": "{ \"action\": \"aws-lambda_function-container-WarmUp\" }"
        # }
        if chatbot_helper._cold_start in event_body[chatbot_helper._action]:
            chatbot_logger.log_write(chatbot_logger._info, "[ColdStart -> WarmUp] AWS Lambda Function 컨테이너 초기화", "OK!")
            return

        kakao_request = event_body   

        file_name = chatbot_helper._botlog_file_path
        
        if False == os.path.exists(file_name):
            dbReset(file_name)
        else:   # 아마존 웹서비스(AWS) 람다 함수(Lambda Function) -> 로그 텍스트 파일("/tmp/botlog.txt") 존재하는 경우   
            chatbot_logger.log_write(chatbot_logger._info, "파일 존재 여부", "File Exists")   # 지금 현재 파일이 있다고 메시지 "File Exists" 로그 기록 

        res_queue = q.Queue()   

        request_respond = threading.Thread(target=resChatbot,
                                           args=(kakao_request, res_queue, file_name))
        
        request_respond.start()

    except Exception as e:   # 하위 코드 블록에서 예외가 발생해도 변수 e에다 넣고 아래 코드 실행됨
        # 테스트 오류 로그 기록  
        error_msg = str(e)  # str() 함수 사용해서 Exception 클래스 객체 e를 문자열로 변환 및 오류 메시지 변수 error_msg에 할당 (문자열로 변환 안할시 챗봇에서 스킬서버 오류 출력되면서 챗봇이 답변도 안하고 장시간 멈춤 상태 발생.)
        # logger._error('[테스트] 오류 - %s' %error_msg)
        chatbot_logger.log_write(chatbot_logger._error, "[테스트] 오류", error_msg)
    finally:   # 예외 발생 여부와 상관없이 항상 마지막에 실행할 코드
        
        if None is res_queue:   # 챗봇 답변 내용 담을 큐 객체 res_queue가 None인 경우 
            chatbot_logger.log_write(chatbot_logger._info, "[테스트] handler - finally 강제 종료", "[사유] 큐(res_queue) 객체 생성 안 함.")
            return  # finally 문 종료 
             
        while(time.time() - start_time < chatbot_helper._time_limit):   # 챗봇 응답 시간 3.5초 이내인 경우
            if False == res_queue.empty():
                resFormat = res_queue.get()  # 큐(res_queue)에서 데이터 가져오기 
                res_queue.task_done()   # 큐(res_queue)에서 가져온 데이터에 대한 작업 완료
                chatbot_logger.log_write(chatbot_logger._info, "[테스트] resFormat 정보", resFormat)

                run_flag= True   
                break    
            time.sleep(chatbot_helper._polling_interval) 
 
        if False == run_flag:   # 챗봇 응답 시간 5초 초과한 경우     
            resFormat = kakao.timeover_quickRepliesResFormat(chatbot_helper._done_thinking)   

        res_msg = json.dumps(resFormat) 
        # logger._info("[테스트] 챗봇 답변 채팅 정보 - %s" %res_msg)
        chatbot_logger.log_write(chatbot_logger._info, "[테스트] 챗봇 답변 채팅 정보", res_msg)

        return {   # 카카오톡 서버로 전송할 json 형태의 데이터 리턴
            'statusCode': chatbot_helper._statusCode_success,
            'body': res_msg,
            'headers': {
                'Access-Control-Allow-Origin': '*',
            }
        }
    
# 챗봇 답변 요청 및 응답 확인
def resChatbot(kakao_request, res_queue, file_name):
    global masterEntity    # 챗봇 마스터 데이터 싱글톤 객체 
 
    botRes = None          # 챗봇 답변 내용  
    resFormat = None       # 카카오 json format 형식 기반 챗봇 답변 내용
    master_data = None     # 챗봇 마스터 데이터 객체 
    userRequest_msg = kakao_request[chatbot_helper._userRequest][chatbot_helper._utterance]   # 사용자 입력 채팅 정보 가져오기 
    
    try:
        # 챗봇 응답 시간 5초 초과시 응답 재요청 기능 구현 
        # 참고 URL - https://claude.ai/chat/d550ac84-5c0c-4805-a600-9fdfd1236714
        if chatbot_helper._done_thinking in userRequest_msg:   # 시간 5초 초과시 응답 재요청
            with open(file_name) as f:
                last_update = f.read()  
                chatbot_logger.log_write(chatbot_logger._info, '[테스트] last_update', last_update)
            if len(last_update.split()) >= chatbot_helper._multiWord:   # 변수 last_update에 저장된 문자열을 공백('')단위로 분리한 단어들의 개수가 1개보다 많은 경우 (여러 단어로 구성)
                kind = last_update.split()[chatbot_helper._firstWord_Idx]    # 변수 last_update에 저장된 문자열을 공백('')단위로 분리한 첫 번째 단어 변수 kind에 저장 (예) ask, img 등등... 
                if kind == "img":   # 변수 kind에 저장된 문자열이 'img'인 경우 
                    botRes, prompt = last_update.split()[chatbot_helper._secondWord_Idx],last_update.split()[chatbot_helper._thirdWord_Idx]   # 변수 last_update에 저장된 문자열 중 공백('')단위로 분리한 두 번째와 세 번째 단어 각각 botRes와 prompt에 저장
                    chatbot_logger.log_write(chatbot_logger._info, '[테스트] /img - botRes (last_update.split()[chatbot_helper._secondWord_Idx])', botRes)
                    chatbot_logger.log_write(chatbot_logger._info, '[테스트] /img - prompt (last_update.split()[chatbot_helper._thirdWord_Idx])', prompt)
                    res_queue.put(kakao.simple_imageResFormat(botRes,prompt))
                else:   # 변수 kind에 저장된 문자열이 'img' 아닌 경우 
                    botRes = last_update[chatbot_helper._askPrefix_Len:]   # 변수 last_update에 저장된 문자열 중 다섯 번째 문자(last_update[chatbot_helper._askPrefix_Length:]) 부터 끝까지 변수 botRes에 저장 (숫자 4 의미 - "ask "(공백 '' 포함) 문자열 제거하고 나머지 텍스트 가져옴)
                    chatbot_logger.log_write(chatbot_logger._info, '[테스트] /ask - botRes (last_update[4:])', botRes)
                    res_queue.put(kakao.simple_textResFormat(botRes))
                dbReset(file_name)    

        elif '/img' in userRequest_msg:   # DALLE2 이미지 응답
            dbReset(file_name)   
            prompt = userRequest_msg.replace("/img", "")
            botRes = openAI.getImageURLFromDALLE(prompt)
            res_queue.put(kakao.simple_imageResFormat(botRes,prompt))

            botlog_msg = f"img {str(botRes)} {str(prompt)}"
            dbSave(file_name, botlog_msg)

        elif '/ask' in userRequest_msg:   # ChatGPT 텍스트 응답 메시지 
            dbReset(file_name)  
            prompt = userRequest_msg.replace("/ask", "")
            botRes = openAI.getMessageFromGPT(prompt)
            res_queue.put(kakao.simple_textResFormat(botRes))

            chatbot_logger.openAI_log_write(chatbot_logger._info, "ChatGPT 텍스트 답변", botRes)
            botlog_msg = f"ask {str(botRes)}" 
            dbSave(file_name, botlog_msg)

        elif True == masterEntity.get_isValid:   # 마스터 데이터 유효성 검사 결과 성공한 경우   
            resFormat, master_data = kakao.getResFormat(userRequest_msg, masterEntity.get_master_datas, masterEntity)

            if master_data is not None:   # 챗봇 특정 아이템 카드(basicCard, carousel) or 바로가기 그룹(quickReplies) 마스터 데이터 값이 존재하는 경우 
                saveLog(file_name, chatbot_logger._info, f"({master_data[chatbot_helper._levelNo]}: {master_data[chatbot_helper._displayName]} - 사용자 입력 채팅 정보: '{userRequest_msg}')")
            else:   # 챗봇 특정 아이템 카드(basicCard, carousel) or 바로가기 그룹(quickReplies) 마스터 데이터 값이 존재하지 않는 경우   
                saveLog(file_name, chatbot_logger._info, f"(etc: [기술지원 문의 제외 일반 문의] - 사용자 입력 채팅 정보: '{userRequest_msg}')")

            res_queue.put(resFormat)

        else:   # 마스터 데이터 유효성 검사 결과 실패인 경우
            raise Exception(chatbot_helper._error_title + 
                            "사유: 마스터 데이터 유효성 검사 결과 실패!\n" + 
                            chatbot_helper._error_ssflex)

        # TODO: 추후 필요시 아래 주석친 코드 참고 예정 (2025.09.12 minjae)
        # else:
        #     base_res = kakao.base_ResFormat()
        #     res_queue.put(base_res)

    except Exception as e:   # 하위 코드 블록에서 예외가 발생해도 변수 e에다 넣고 아래 코드 실행됨  
        error_msg = str(e) 
        chatbot_logger.log_write(chatbot_logger._error, "[테스트] 오류", error_msg)
        res_queue.put(kakao.error_textResFormat(error_msg))
        raise    # raise로 함수 resChatbot의 현재 예외를 다시 발생시켜서 함수 resChatbot 호출한 상위 코드 블록으로 넘김                             

# 아마존 웹서비스(AWS) 람다 함수(Lambda Function) -> 로그 텍스트 파일("/tmp/botlog.txt") 전용 함수 
# 로그(텍스트) 초기화 및 작성 
def saveLog(file_name, log_level, botlog_msg):
    dbReset(file_name)   
    chatbot_logger.log_write(log_level, "[테스트] AWS 로그 기록", botlog_msg)
    dbSave(file_name, botlog_msg)

# 로그(텍스트) 초기화  
def dbReset(file_name):
    with open(file_name, 'w') as f:
        f.write("")

# 로그(텍스트) 작성  
def dbSave(file_name, botlog_msg):
    with open(file_name, 'w') as f:
        f.write(botlog_msg)