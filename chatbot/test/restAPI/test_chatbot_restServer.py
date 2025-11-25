# 챗봇 Rest API 함수 전용 모듈  
import json   # 웹서버로부터 받은 json 데이터 처리 패키지 json
import asyncio   # 비동기 프로그래밍(async - await) 전용 모듈
 
from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트 
from utils import chatbot_logger   # 챗봇 커스텀 로그 작성 모듈 -> 챗봇 전역 로그 객체(logger) 사용 못하는 경우 import 처리

# TODO: 추후 테스트 웹서버 구축 후 마스터 데이터 다운로드 Rest API 함수 getMasterDownLoadAsync 로직 수정 예정 (2025.09.11 minjae)
# 마스터 데이터 다운로드 
async def getMasterDownLoadAsync(masterEntity_json_filepath):
    master_datas = None   # 전체 마스터 데이터 (Dictionary)

    try:
        chatbot_logger.log_write(chatbot_logger._info, '[테스트] 웹서버 마스터 데이터 다운로드', 'Start!')

        # TODO: 마스터 데이터 json 파일(masterEntity.json) 읽어서 Dictionary 객체 변환 구현 (2025.07.25 minjae)
        # 참고 URL - https://wikidocs.net/126088
        # 참고 2 URL - https://chatgpt.com/c/688313d0-c32c-8010-8c38-b05fe54c0244
        with open(masterEntity_json_filepath, 'r', encoding='utf-8') as json_file:
            res = json.load(json_file)

            # TODO: 오류 로그 "[테스트] 오류 - 'startCard'" 기록되면서 챗봇 실행 오류 발생하여 코드 
            #       (기존) master_datas = json.loads(res['masterEntity']) -> (변경) master_datas = res['masterEntity'] 완료 (2025.08.18 minjae)
            # 참고 URL - https://claude.ai/chat/d46eab6c-4e09-4440-a8d2-9136f101b200
            # master_datas = json.loads(res['masterEntity'])
            master_datas = res[chatbot_helper._masterEntity]    

            await asyncio.sleep(0.1)    # 0.1초 대기. asyncio.sleep 비동기 함수도 네이티브 코루틴이다. (async def로 만든 코루틴은 네이티브 코루틴이라고 한다.)
        
        chatbot_logger.log_write(chatbot_logger._info, '[테스트] 웹서버 마스터 데이터 다운로드 결과', 'OK!')   
    
    except Exception as e:     
        error_msg = str(e)    
        chatbot_logger.log_write(chatbot_logger._error, "[테스트] 오류", error_msg) 
    finally:
        return master_datas

    
# 참고
# 비동기 프로그래밍 전용 모듈 asyncio (asyncio는 async/await 구문을 사용하여 동시성 코드를 작성하는 라이브러리이다.)
# 참고 URL - https://docs.python.org/3/library/asyncio.html
# 참고 2 URL - https://docs.python.org/ko/3/library/asyncio-task.html
# 참고 3 URL - https://dojang.io/mod/page/view.php?id=2469
# 참고 4 URL - https://wikidocs.net/125092
# 참고 5 URL - https://wikidocs.net/252232

# TODO: 마스터 데이터 다운로드 함수 로직 추후 구현 예정 (2025.05.26 minjae)
# 참고 URL - https://wikidocs.net/28
# ***** 테스트 기능 구현 순서 *****  
# 1. masterEntity.json 파일 읽어와서 2차원 리스트 변환 및 변수 masterDatas에 값 할당
# 2. 변수 masterDatas 리턴  
# 3. 2번에서 리턴 받은 masterDatas 가지고 데이터 유효성 검사(isValidator()) 진행 

# TODO: 필요시 마스터 데이터 json 파일(masterEntity.json) json 구조 수정 진행 (2025.08.29 minjae)
# 참고 URL - https://claude.ai/chat/6df9cfce-001d-4da4-8150-25fb984cee4f
# 참고 2 URL - https://claude.ai/chat/72631fb7-ae64-4538-a9a8-f136e59f3207

# TODO: 아래 주석친 내용 필요시 참고 (2025.09.11 minjae)
# TODO: 테스터용 마스터 데이터 json 파일(test_masterEntity.json) json 양식 작성 (2025.07.24 minjae) 
# 참고 URL - https://chatgpt.com/c/68819688-4654-8010-b1a2-ff5a0bd71816
# 참고 2 URL - https://chatgpt.com/c/6882d4e2-f8ac-8010-afb9-9934c123cb32
# {
#   "body": "{ \"action\": \"aws-lambda_function-container-WarmUp\",
#              \"startBtns\": [\"채팅 상담\", \"챗봇 문의\", \"원격 지원\"] }"
# }

# TODO: 테스터용 마스터 데이터 json 파일(masterEntity.json) json 양식 수정 (2025.09.05 minjae) 
# 참고 URL - https://claude.ai/chat/24019d34-c0c9-46e9-9fe3-1372bdcc0115
# 참고 2 URL - https://claude.ai/chat/90aed67b-eb29-418a-8c4f-a40ac3601b11