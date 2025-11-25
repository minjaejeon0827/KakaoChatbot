"""
* 챗봇 Rest API 함수 전용 모듈
코드 리뷰 참고 URL - https://chatgpt.com/c/691c2981-cca4-8321-97b0-63fae70f070a
"""
 
# 1. 공통 모듈 먼저 import 
from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트 

# 2. 챗봇 커스텀 로그 기록 모듈 import
from utils import chatbot_logger   # log.py -> 챗봇 전역 로그 객체(logger) 사용 못하는 경우 import

# 3. Type Hints class Any import
from typing import Any

# 4. 나머지 모듈 import
import json      # json 데이터 처리
import asyncio   # 비동기 프로그래밍(async - await)

# TODO: 추후 테스트 웹서버 구축 후 마스터 데이터 다운로드 Rest API 함수 get_masterDownLoadAsync 로직 수정 예정 (2025.09.11 minjae)
async def get_masterDownLoadAsync(masterEntity_json_file_path: str | None = None) -> dict[str, Any]:
    """  
    Description: 전체 마스터 데이터 다운로드 및 데이터 가져오기

    Parameters: masterEntity_json_file_path - 전체 마스터 데이터 json 파일 상대 경로

    Returns: master_datas - 전체 마스터 데이터 
    """

    master_datas = None

    try:
        chatbot_logger.info("[테스트] 전체 마스터 데이터 다운로드 - 시작!")

        if None is masterEntity_json_file_path:
            raise ValueError("전체 마스터 데이터 json 파일 상대 경로 존재 안 함.")

        # 전체 마스터 데이터 json 파일(masterEntity.json) 읽어서 dict 객체 변환 구현 (2025.07.25 minjae)
        # 참고 URL - https://docs.python.org/ko/3/library/functions.html#open
        # 참고 2 URL - https://wikidocs.net/126088
        # 참고 3 URL - https://chatgpt.com/c/688313d0-c32c-8010-8c38-b05fe54c0244
        with open(masterEntity_json_file_path, 'r', encoding='utf-8') as json_file:
            response = json.load(json_file)

            # 챗봇 프로그램 오류 발생 및 로그 "[테스트] 오류 - 'startCard'" 출력되어 코드 아래처럼 변경 (2025.08.18 minjae)
            # (기존) master_datas = json.loads(response['masterEntity']) -> (변경) master_datas = response['masterEntity'] 
            # 참고 URL - https://claude.ai/chat/d46eab6c-4e09-4440-a8d2-9136f101b200
            # master_datas = json.loads(response['masterEntity'])
            master_datas = response[chatbot_helper._masterEntity]

            await asyncio.sleep(0.1)    # 0.1초 대기. asyncio.sleep 비동기 함수도 네이티브 코루틴이다. (async def로 만든 코루틴은 네이티브 코루틴이라고 한다.)
           
        chatbot_logger.info("[테스트] 전체 마스터 데이터 다운로드 결과 - 완료!")

    except (KeyError, ValueError, TypeError) as e:
        valid_error_msg = str(e)
        chatbot_logger.error(f"[테스트] 데이터 유효성 오류 - {valid_error_msg}")
    except Exception as e:
        sys_error_msg = str(e)
        chatbot_logger.critical(f"[테스트] 시스템 오류 - {sys_error_msg}")
    finally: return master_datas

"""
* 참고
비동기 프로그래밍 전용 모듈 asyncio (asyncio는 async/await 구문을 사용하여 동시성 코드를 작성하는 라이브러리이다.)
참고 URL - https://docs.python.org/3/library/asyncio.html
참고 2 URL - https://docs.python.org/ko/3/library/asyncio-task.html
참고 3 URL - https://dojang.io/mod/page/view.php?id=2469
참고 4 URL - https://wikidocs.net/125092
참고 5 URL - https://wikidocs.net/252232

TODO: 전체 마스터 데이터 다운로드 함수 로직 추후 수정 예정 (2025.05.26 minjae)
참고 URL - https://wikidocs.net/28
***** 테스트 기능 구현 순서 *****  
1. masterEntity.json 파일 읽어와서 2차원 리스트 변환 및 변수 masterDatas에 값 할당
2. 변수 masterDatas 리턴  
3. 2번에서 리턴 받은 masterDatas 가지고 싱글톤(singleton) 패턴 전용 모듈(singleton.py) -> 데이터 유효성 검사(isValidator()) 진행

TODO: 필요시 전체 마스터 데이터 json 파일(masterEntity.json) json 구조 수정 진행 (2025.08.29 minjae)
참고 URL - https://claude.ai/chat/6df9cfce-001d-4da4-8150-25fb984cee4f
참고 2 URL - https://claude.ai/chat/72631fb7-ae64-4538-a9a8-f136e59f3207

TODO: 테스터용 전체 마스터 데이터 json 파일(test_masterEntity.json) json 양식 작성 (2025.07.24 minjae) 
참고 URL - https://chatgpt.com/c/68819688-4654-8010-b1a2-ff5a0bd71816
참고 2 URL - https://chatgpt.com/c/6882d4e2-f8ac-8010-afb9-9934c123cb32
{
  "body": "{ \"action\": \"aws-lambda_function-container-WarmUp\",
             \"startBtns\": [\"채팅 상담\", \"챗봇 문의\", \"원격 지원\"] }"
}

TODO: 전체 마스터 데이터 json 파일(masterEntity.json) json 양식 수정 (2025.09.05 minjae) 
참고 URL - https://claude.ai/chat/24019d34-c0c9-46e9-9fe3-1372bdcc0115
참고 2 URL - https://claude.ai/chat/90aed67b-eb29-418a-8c4f-a40ac3601b11
"""