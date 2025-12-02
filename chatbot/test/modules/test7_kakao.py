"""
* [카카오톡 서버 전송 용도] json 포맷 전용 모듈
참고 URL - https://chatgpt.com/c/69002b43-44c0-8322-8298-e7871b39da2a

* 챗봇 응답 타입별 json 포맷
참고 URL - https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format

* 메타 데이터 (meta_data)
참고 URL - https://namu.wiki/w/%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0
참고 2 URL - https://ko.wikipedia.org/wiki/%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0#cite_note-NISO-22

* Race Condition
참고 URL - https://en.wikipedia.org/wiki/Race_condition
참고 2 URL - https://namu.wiki/w/%EA%B2%BD%EC%9F%81%20%EC%83%81%ED%83%9C
참고 3 URL - https://lake0989.tistory.com/121

* 파이썬 패키지, 모듈
참고 URL - https://docs.python.org/ko/3.13/tutorial/modules.html
참고 2 URL - https://wikidocs.net/1418
참고 3 URL - https://dojang.io/mod/page/view.php?id=2450

* 파이썬 Type Hints
참고 URL - https://docs.python.org/ko/3.14/library/typing.html
참고 2 URL - https://peps.python.org/pep-0484/
참고 3 URL - https://devpouch.tistory.com/189
참고 4 URL - https://supermemi.tistory.com/entry/Python-3-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-%EC%9D%98%EB%AF%B8%EB%8A%94-%EB%AC%B4%EC%97%87%EC%9D%BC%EA%B9%8C-%EC%A3%BC%EC%84%9D

* 파이썬 Type Hints class Any
참고 URL - https://docs.python.org/ko/3.9/library/typing.html#the-any-type
"""

# 1. 공통 모듈 먼저 import
from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트

# 2. log 모듈 import
from utils.log import logger       # 챗봇 전역 로그 객체(logger)  

# 3. Type Hints class Any import
from typing import Any

def outputs_format(outputs: list[dict]) -> dict[str, Any]:
    """
    Description: 출력 그룹 json 포맷 가져오기

    Parameters: outputs - 출력 그룹 리스트

    Returns: 출력 그룹 json 포맷
    """

    return {
        "version": "2.0",
        "template": {
            "outputs": outputs,
            "quickReplies": []
        }
    }

def quickReplies_format(master_data: dict[str, Any], buttons: list[dict]) -> dict[str, Any]:
    """
    Description: 바로가기 그룹 json 포맷 가져오기

    Parameters: master_data - 특정 마스터 데이터
                buttons - 버튼 리스트 (label + messageText)

    Returns: 바로가기 그룹 json 포맷
    """

    return {
        'version': '2.0', 
        'template': {
            'outputs': [
                {
                    "simpleText": {
                        "text": master_data[chatbot_helper._description]
                    }
                }
            ], 
            'quickReplies': buttons
        }
    }

def textCard_format(master_data: dict[str, Any], buttons: list[dict]) -> dict[str, Any]:
    """
    Description: 텍스트 카드 json 포맷 가져오기

    Parameters: master_data - 특정 마스터 데이터
                buttons - 버튼 리스트 (label + messageText) 

    Returns: 텍스트 카드 json 포맷
    """

    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "textCard": {
                        "title": master_data[chatbot_helper._title],
                        "description": master_data[chatbot_helper._description],
                        "buttons": buttons
                    }
                }
            ],
            "quickReplies": []
        }
    }

def basicCard_format(master_data: dict[str, Any], buttons: list[dict]) -> dict[str, Any]:
    """
    Description: 기본형 카드 json 포맷 가져오기

    Parameters: master_data - 특정 마스터 데이터
                buttons - 버튼 리스트 (label + messageText)

    Returns: 기본형 카드 json 포맷
    """

    outputs = []

    # master_data[chatbot_helper._text]에 할당된 값이 null 또는 공백("")일 경우 basicCard 가 카카오톡 채팅방에 출력 안되는 오류 발생함. 
    # 하여 null 또는 공백("")이 아닌 문자열로 할당 해야함. (2025.09.03 minjae)
    # 참고 URL - https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty-in-python
    # 참고 2 URL - https://hello-bryan.tistory.com/131
    # 참고 3 URL - https://jino-dev-diary.tistory.com/42
    # 참고 4 URL - https://claude.ai/chat/eaf7856e-1b5e-4c26-992e-de1683005638
    if master_data[chatbot_helper._text]:   # master_data[chatbot_helper._text]에 할당된 값이 null 또는 공백("")이 아닌 경우 (None or Empty String Check)
        outputs.append({
            "simpleText": {
                "text": master_data[chatbot_helper._text]
            }
        })

    outputs.append({   # basicCard 항상 추가
        "basicCard": {
            "title": master_data[chatbot_helper._title],
            "description": master_data[chatbot_helper._description],
            "thumbnail": {
                "imageUrl": master_data[chatbot_helper._thumbnail][chatbot_helper._imageUrl],
                "link": {
                    "web": master_data[chatbot_helper._thumbnail][chatbot_helper._webLinkUrl]
                }
            },
            "buttons": buttons
        }
    })

    return outputs_format(outputs)

def carousel_format(master_data: dict[str, Any], items: list[dict]) -> dict[str, Any]:
    """
    Description: 아이템형 케로셀 json 포맷 가져오기

    Parameters: master_data - 특정 마스터 데이터
                items - 아이템 리스트 (imageTitle + thumbnail + itemList 등등...) 

    Returns: 아이템형 케로셀 json 포맷 
    """
    
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": master_data[chatbot_helper._text]
                    }
                },
                {
                    "carousel": {
                        "type": "itemCard",
                        "items": items
                    }
                }
            ]
        }
    }

def empty_response(master_data: dict[str, Any] = None) -> dict[str, Any]:
    """
    Description: 기술지원 문의 제외 일반 문의 json 포맷 가져오기
                 카카오톡 채팅방에 응답 메시지를 출력하고 싶지 않은 경우 비어있는 메세지 전송 

    Parameters: master_data - 특정 마스터 데이터 (default parameter)
                참고 URL - https://docs.python.org/ko/3/glossary.html#term-parameter

    Returns: 기술지원 문의 제외 일반 문의 json 포맷
    """

    # logger.info(f"[테스트] master_data - {master_data}")

    empty_format = {
        'version': '2.0',
        'template': {
            'outputs': [], 
            'quickReplies': []
        }
    }

    return { "format": empty_format, "meta_data": master_data }

def simple_text(text: str) -> dict[str, Any]:
    """
    Description: 텍스트 메세지 json 포맷 가져오기
                 카카오톡 채팅방에 텍스트 메시지(text) 전송 

    Parameters: text - 챗봇 답변 내용  

    Returns: 텍스트 메세지 json 포맷
    """
 
    return {
        'version': '2.0', 
        'template': {
            'outputs': [
                {
                    "simpleText": {
                        "text": text
                    }
                }
            ], 
            'quickReplies': []
        }
    }

# TODO: 아래 주석친 코드 필요시 사용 예정 (2025.09.29 minjae)
# def simple_image(text: str, prompt: str) -> dict[str, Any]:
#     """
#     Description: DALLE2 이미지 json 포맷 가져오기
#                  카카오톡 채팅방에 DALLE2 이미지 전송

#     Parameters: text - DALLE2 이미지 URL 주소 
#                 prompt - 사용자가 카카오톡 채팅방에 그려 달라고 요청한 이미지 설명 
    
#     Returns: DALLE2 이미지 json 포맷
#     """

#     output_text = prompt + "내용에 관한 이미지 입니다"

#     return {
#         'version': '2.0', 
#         'template': {
#             'outputs': [
#                 {
#                     "simpleImage": {
#                         "imageUrl": text,
#                         "altText": output_text
#                     }
#                 }
#             ], 
#             'quickReplies': []
#         }
#     }   

def error_text(error_msg: str) -> dict[str, Any]:
    """
    Description: 오류 메세지 json 포맷 가져오기
                 카카오톡 채팅방에 오류 메세지 전송

    Parameters: error_msg - 오류 메세지

    Returns: 오류 메세지 json 포맷
    """
 
    return {
        'version': '2.0', 
        'template': {
            'outputs': [
                {
                    "simpleText": {
                        "text": error_msg
                    }
                }
            ], 
            "quickReplies": [
                {
                    "action": chatbot_helper._message,
                    "label": chatbot_helper._beginning,
                    "messageText": chatbot_helper._beginning
                }
            ]
        }
    }       

def timeOver_quickReplies(requestAgain_msg: str) -> dict[str, Any]:
    """
    Description: 응답 재요청 json 포맷 가져오기
                 챗봇 응답 시간 5초 초과시 응답 재요청 메세지 전송

    Parameters: requestAgain_msg - 응답 재요청 메세지

    Returns: 응답 재요청 json 포맷
    """

    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": chatbot_helper._checkRequest
                    }
                }
            ],
            "quickReplies": [
                {
                    "action": chatbot_helper._message,
                    "label": requestAgain_msg,
                    "messageText": requestAgain_msg
                }
            ]
        }
    }

def _create_buttons(master_data: dict[str, Any], message_prefix: str = None) -> list[dict]:
    """
    Description: [공통] 버튼 리스트 생성

    Parameters: master_data - 특정 마스터 데이터
                message_prefix - 버튼 messageText 접두사 (default parameter)
                참고 URL - https://docs.python.org/ko/3/glossary.html#term-parameter

    Returns: buttons - [공통] 버튼 리스트 (label + messageText)
    """

    buttons = []

    # 브루트 포스 완전 탐색 알고리즘 (Brute Force Algorithm) - 무차별 대입법이라고 불리며, 문제를 해결하기 위해 가능한 경우의 수를 모두 검사(완전 탐색)해보는 방법이다.
    # 참고 URL - https://ko.wikipedia.org/wiki/%EB%AC%B4%EC%B0%A8%EB%B3%84_%EB%8C%80%EC%9E%85_%EA%B2%80%EC%83%89
    # 참고 2 URL - https://wikidocs.net/233719
    # 참고 3 URL - https://youtu.be/QhMY4t2xwG0?si=uYsaL7CLHmx-RHV8
    for button in master_data[chatbot_helper._buttons]:   # [공통] 버튼 텍스트 및 메세지 추가
        if button[chatbot_helper._webLinkUrl]:   # button[chatbot_helper._webLinkUrl]에 할당된 값이 null 또는 공백("")이 아닌 경우 (None or Empty String Check)
            buttons.append({
                "action": chatbot_helper._webLink,
                "label": button[chatbot_helper._label],
                "webLinkUrl": button[chatbot_helper._webLinkUrl]
            })
            
        else:   # button[chatbot_helper._webLinkUrl]에 할당된 값이 null 또는 공백("")인 경우
            messageText = f"{message_prefix} {button[chatbot_helper._messageText]}" if message_prefix else button[chatbot_helper._messageText]
            buttons.append({
                "action": chatbot_helper._message,
                "label": button[chatbot_helper._label],
                "messageText": messageText
            })

    return buttons

def common_basicCard(master_data: dict[str, Any]) -> dict[str, Any]:
    """
    Description: [공통] 기본형 카드 json 포맷 가져오기 

    Parameters: master_data - 특정 마스터 데이터

    Returns: basicCard_format(master_data, buttons) - [공통] 기본형 카드 json 포맷
             master_data - 특정 마스터 데이터
    """

    buttons = _create_buttons(master_data)   # [공통] 버튼 리스트 생성

    return { "format": basicCard_format(master_data, buttons), "meta_data": master_data }

def common_quickReplies(master_data: dict[str, Any]) -> dict[str, Any]:
    """
    Description: [공통] 바로가기 그룹 json 포맷 가져오기

    Parameters: master_data - 특정 마스터 데이터

    Returns: quickReplies_format(master_data, buttons) - [공통] 바로가기 그룹 json 포맷
             master_data - 특정 마스터 데이터
    """

    buttons = _create_buttons(master_data)

    return { "format": quickReplies_format(master_data, buttons), "meta_data": master_data }

def common_ver_quickReplies(userRequest_msg: str, master_data: dict[str, Any]) -> dict[str, Any]:
    """
    Description: [공통] Autodesk or 상상진화 BOX 제품 버전 바로가기 그룹 json 포맷 가져오기

    Parameters: userRequest_msg - 사용자 입력 채팅 메세지
                master_data - 특정 마스터 데이터

    Returns: quickReplies_format(master_data, buttons) - [공통] Autodesk or 상상진화 BOX 제품 버전 바로가기 그룹 json 포맷
             master_data - 특정 마스터 데이터
    """

    message_prefix = f"{chatbot_helper._instType} {userRequest_msg}"
    buttons = _create_buttons(master_data, message_prefix)

    return { "format": quickReplies_format(master_data, buttons), "meta_data": master_data }

def get_response(userRequest_msg: str, masterEntity: dict[str, Any]) -> dict[str, Any]:
    """
    Description: 카카오 json 포맷 가져오기  

    Parameters: userRequest_msg - 사용자 입력 채팅 메세지 
                masterEntity - 마스터 데이터 담는 싱글톤(singleton) 객체

    Returns: 1. 카카오 json 포맷 기반 챗봇 답변 내용,
             2. 특정 마스터 데이터 (예) 아이템 카드 (basicCard, carousel) or 바로가기 그룹 (quickReplies)
    """

    # 아래와 같은 오류 메시지 출력되어 (기존) masterEntity.get_master_datas() -> (변경) masterEntity.get_master_datas 처리함. (2025.09.16 minjae)
    # 오류 메시지 - 'dict' object is not callable
    # master_datas = masterEntity.get_master_datas()
    master_datas = masterEntity.get_master_datas   # 전체 마스터 데이터

    # 파이썬 람다 표현식
    # 참고 URL - https://docs.python.org/ko/2/tutorial/controlflow.html#lambda-expressions

    eq_operator_mappings = {   # if 조건절 eq 연산자(==) 매핑 Dictionary 객체
        chatbot_helper._instSupport_adskProduct: lambda: common_quickReplies(master_datas[chatbot_helper._adskReplies]),   # level3 - Autodesk 제품 설치 문의
        chatbot_helper._instSupport_boxProduct: lambda: common_quickReplies(master_datas[chatbot_helper._boxReplies]),   # level3 - 상상진화 BOX 제품 설치 문의
        # TODO: 아래 주석친 코드 필요시 사용 예정 (2025.10.30 minjae)
        # chatbot_helper._ask_accountProduct: lambda: account_quickReplies(master_datas[chatbot_helper._accountReplies])   # level3 - 계정 & 제품배정 문의

        # level4 - 상상진화 BOX 제품 버전
        chatbot_helper._revitBox: lambda: common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._boxVerReplies]),
        chatbot_helper._cadBox: lambda: common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._boxVerReplies]),
        chatbot_helper._energyBox: lambda: common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._boxVerReplies]),

        # level4 - Autodesk 제품 버전
        chatbot_helper._autoCAD: lambda: common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._adskVerReplies]),
        chatbot_helper._revit: lambda:  common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._adskVerReplies]),
        chatbot_helper._navisworksManage: lambda: common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._adskVerReplies]),
        chatbot_helper._infraWorks: lambda: common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._adskVerReplies]),
        chatbot_helper._civil3D: lambda: common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._adskVerReplies]) 
    }

    in_operator_mappings = {   # if 조건절 in 연산자 매핑 Dictionary 객체
        chatbot_helper._start: lambda: common_basicCard(master_datas[chatbot_helper._startCard]),   # start - 시작 화면
        chatbot_helper._beginning: lambda: common_basicCard(master_datas[chatbot_helper._startCard]),   # start - 처음으로
        chatbot_helper._remote_text: lambda: empty_response(master_datas[chatbot_helper._startCard]),   # level1 - 원격 지원
        chatbot_helper._ask_chatbot: lambda: chatbot_carousel(master_datas[chatbot_helper._chatbotCard]),   # level1 - 챗봇 문의
        chatbot_helper._adskProduct: lambda: subCat_basicCard(userRequest_msg, master_datas[chatbot_helper._subCatCard]),   # level2 - 문의 유형 (Autodesk 제품)
        chatbot_helper._boxProduct: lambda: subCat_basicCard(userRequest_msg, master_datas[chatbot_helper._subCatCard]),   # level2 - 문의 유형 (상상진화 BOX 제품)
        # end - 텍스트 + basicCard Autodesk or 상상진화 BOX 제품 설치 방법 매핑 Dictionary 객체
        f"{chatbot_helper._instType} {chatbot_helper._revitBox}": lambda: end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._revitBoxInfos]),
        f"{chatbot_helper._instType} {chatbot_helper._cadBox}": lambda: end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._cadBoxInfos]),
        f"{chatbot_helper._instType} {chatbot_helper._energyBox}": lambda: end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._energyBoxInfos]),
        f"{chatbot_helper._instType} {chatbot_helper._autoCAD}": lambda: end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._autoCADInfos]),
        f"{chatbot_helper._instType} {chatbot_helper._revit}": lambda: end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._revitInfos]),
        f"{chatbot_helper._instType} {chatbot_helper._navisworksManage}": lambda: end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._navisworksManageInfos]),
        f"{chatbot_helper._instType} {chatbot_helper._infraWorks}": lambda: end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._infraWorksInfos]),
        f"{chatbot_helper._instType} {chatbot_helper._civil3D}": lambda: end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._civil3DInfos])

        # TODO: 오류 메시지 "TypeError: unhashable type: 'list'" 출력되어 아래 주석친 코드 사용 안 함. (2025.10.30 minjae)
        # unhashable type 오류는 파이썬에서 해시(Hash) 가능하지 않은 자료형을 부적절하게 사용하려 할 때 발생하는 오류이다.
        # 참고 URL - https://kimpanda.tistory.com/289
        # chatbot_messageTexts: lambda: conditional_action(userRequest_msg, chatbot_messageTexts, subCat_basicCard(userRequest_msg, master_datas[chatbot_helper._subCatCard])),   # level2 - 문의 유형
        # adsk_messageTexts: lambda: conditional_action(userRequest_msg, adsk_messageTexts, common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._adskVerReplies])),   # level4 - Autodesk 제품 버전
        # box_messageTexts: lambda: conditional_action(userRequest_msg, box_messageTexts, common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._boxVerReplies])),   # level4 - 상상진화 BOX 제품 버전
    }

    try:
        logger.info("[테스트] 카카오 json 포맷 가져오기 - 시작!")

        # TODO: 아래 주석친 코드 필요시 참고 (2025.10.30 minjae)
        # raise Exception(chatbot_helper._error_title + 
        #                 '사유: 카카오 json 포맷 가져오기 오류 발생!!!\n'+
        #                 chatbot_helper._error_ssflex)   # 예외 발생시킴

        # 브루트 포스 완전 탐색 알고리즘 (Brute Force Algorithm) - 무차별 대입법이라고 불리며, 문제를 해결하기 위해 가능한 경우의 수를 모두 검사(완전 탐색)해보는 방법이다.
        # 참고 URL - https://ko.wikipedia.org/wiki/%EB%AC%B4%EC%B0%A8%EB%B3%84_%EB%8C%80%EC%9E%85_%EA%B2%80%EC%83%89
        # 참고 2 URL - https://wikidocs.net/233719
        # 참고 3 URL - https://youtu.be/QhMY4t2xwG0?si=uYsaL7CLHmx-RHV8

        # TODO: eq_operator_mappings, in_operator_mappings Dictionary 타입 객체들을 for문으로 루핑하기 위해 items() 메서드 사용 구현 (2025.10.29 minjae)
        # 참고 URL - https://docs.python.org/ko/3.13/tutorial/datastructures.html#looping-techniques
        # 조기 종료(return) 통해 불필요한 후속 탐색을 줄이는 최적화된 브루트 포스 완전 탐색 알고리즘 (Brute Force Algorithm) - "브루트 포스(Brute Force) 완전 탐색 알고리즘 기반 탐색 구조 + 그리디(Greedy) 알고리즘 방식 조기 종료" 혼합형
        for key, handler in eq_operator_mappings.items():   # 사용자 입력(userRequest_msg)에 맞는 핸들러 함수(handler) 찾아 실행
            if key == userRequest_msg:
                logger.info(f"[테스트] [eq_operator_mappings] key: '{key}', userRequest_msg: '{userRequest_msg}'")
                return handler()
            
        for key, handler in in_operator_mappings.items():   # 사용자 입력(userRequest_msg)에 맞는 핸들러 함수(handler) 찾아 실행
            if key in userRequest_msg:
                logger.info(f"[테스트] [in_operator_mappings] key: '{key}', userRequest_msg: '{userRequest_msg}'")
                return handler()
            
        # TODO: 오류 메시지 "TypeError: cannot unpack non-iterable NoneType object" 출력 원인 파악 (2025.10.30 minjae)
        # 오류 원인 - 함수나 메서드가 None 값을 반환했을 때, 해당 None 값을 언패킹(unpacking) 하려고 시도할 경우 발생. 즉, Python에서 None 객체는 반복(iteration)이 불가능하므로, 언패킹(unpacking) 불가.
        # 참고 URL - https://python.realjourney.co.kr/entry/Pytorch-TypeError-cannot-unpack-non-iterable-NoneType-object

        # 사용자가 카카오 챗봇 버튼이 아닌 일반 메시지를 채팅창에 입력시 아래처럼 오류 메시지가 출력되어 원인 파악하니 함수 실행 결과 None으로 반환되고
        # lambda_function.py 소스파일 -> chatbot_response 함수에서 res_queue.put(response) 실행할 때 발생하는 오류로 확인 되어 아래처럼 else 절 코드 추가 (2025.10.30 minjae)
        # 참고 URL - https://claude.ai/chat/2035baf1-0f86-4d08-af37-0091c8358dbb
        # 오류 메시지 - "TypeError: 'NoneType' object is not subscriptable"
        logger.info("[테스트] [기술지원 문의 제외 일반 문의] 카카오 json 포맷 가져오기 - 완료!")
        return empty_response()   # 기술지원 문의 제외 일반 문의
        
    except Exception as e:     
        error_msg = str(e)
        logger.error(f"[테스트] 오류 - {error_msg}")
        raise

def chatbot_carousel(master_data: dict[str, Any]) -> dict[str, Any]:
    """  
    Description: 챗봇 문의 아이템형 케로셀 json 포맷 가져오기

    Parameters: master_data - 특정 마스터 데이터

    Returns: carousel_format(master_data, chatbot_items) - 챗봇 문의 아이템형 케로셀 json 포맷
             master_data - 특정 마스터 데이터
    """

    buttons = []
     
    for chatbotButton in master_data[chatbot_helper._buttons]:   # 챗봇 문의 아이템형 케로셀 3가지 버튼 텍스트 및 메세지 추가
        buttons.append({
            "action": chatbot_helper._message,
            "label": chatbotButton[chatbot_helper._label],
            "messageText": chatbotButton[chatbot_helper._messageText]
        })

    chatbot_items = []
    chatbot_items.append({
        "imageTitle": {
            "title": master_data[chatbot_helper._title],
            "description": master_data[chatbot_helper._description]
        },
        # "title": "",
        # "description": "",
        "thumbnail": {
            "imageUrl": master_data[chatbot_helper._thumbnail][chatbot_helper._imageUrl],
            "link": {
                "web": master_data[chatbot_helper._thumbnail][chatbot_helper._webLinkUrl]
            }
        },
        "itemList": [
            {
                "title": master_data[chatbot_helper._itemList][chatbot_helper._chatbotItem_Idx][chatbot_helper._title],
                "description": master_data[chatbot_helper._itemList][chatbot_helper._chatbotItem_Idx][chatbot_helper._description]
            }
        ],
        "itemListAlignment": "left",
        "buttons": buttons,
        "buttonLayout": "vertical"
    })

    return { "format": carousel_format(master_data, chatbot_items), "meta_data": master_data }

# TODO: 아래 함수 subCat_basicCard 필요시 로직 수정 예정 (2025.10.31 minjae)
def subCat_basicCard(userRequest_msg: str, master_data: dict[str, Any]) -> dict[str, Any]:
    """
    Description: 문의 유형 기본형 카드 json 포맷 가져오기 

    Parameters: userRequest_msg - 사용자 입력 채팅 메세지
                master_data - 특정 마스터 데이터

    Returns: basicCard_format(master_data, buttons) - 문의 유형 기본형 카드 json 포맷
             master_data - 특정 마스터 데이터
    """

    buttons = []
    
    # 브루트 포스 완전 탐색 알고리즘 (Brute Force Algorithm) - 무차별 대입법이라고 불리며, 문제를 해결하기 위해 가능한 경우의 수를 모두 검사(완전 탐색)해보는 방법이다.
    # 참고 URL - https://ko.wikipedia.org/wiki/%EB%AC%B4%EC%B0%A8%EB%B3%84_%EB%8C%80%EC%9E%85_%EA%B2%80%EC%83%89
    # 참고 2 URL - https://wikidocs.net/233719
    # 참고 3 URL - https://youtu.be/QhMY4t2xwG0?si=uYsaL7CLHmx-RHV8
    for subCatButton in master_data[chatbot_helper._buttons]:   # 문의 유형 기본형 카드 버튼 텍스트 및 메세지 추가
        messageText = None   

        # 변수(subCatButton[chatbot_helper._label])에 저장된 값이 '설치 문의' and 변수(userRequest_msg)에 저장된 값이 'Autodesk 제품' 또는 '상상진화 BOX 제품'인 경우 
        if (chatbot_helper._askInst == subCatButton[chatbot_helper._label] and chatbot_helper._accountProduct != userRequest_msg):
            messageText = f"{userRequest_msg} {subCatButton[chatbot_helper._messageText]}"

        # 변수(subCatButton[chatbot_helper._label])에 저장된 값이 '계정 & 제품배정 문의'인 경우 and 변수(userRequest_msg)에 저장된 값이 '계정 & 제품배정'인 경우 
        elif (chatbot_helper._ask_accountProduct == subCatButton[chatbot_helper._label] and chatbot_helper._accountProduct == userRequest_msg):
            messageText = subCatButton[chatbot_helper._messageText]

        if None is messageText: continue   # 위 2가지 조건에 해당되지 않는 경우 continue 처리

        buttons.append({
            "action": chatbot_helper._message,
            "label": subCatButton[chatbot_helper._label],
            "messageText": messageText
        })

    return { "format": basicCard_format(master_data, buttons), "meta_data": master_data }

# TODO: 아래 주석친 코드 필요시 사용 예정 (2025.09.17 minjae)
# def adskLang_textCard(userRequest_msg: str, master_data: dict[str, Any]) -> dict[str, Any]:
#     """
#     Description: Autodesk 제품 설치 언어 텍스트 카드 json 포맷 가져오기

#     Parameters: userRequest_msg - 사용자 입력 채팅 메세지
#                 master_data - 특정 마스터 데이터

#     Returns: textCard_format(master_data, buttons) - Autodesk 제품 설치 언어 텍스트 카드 json 포맷
#              master_data - 특정 마스터 데이터
#     """

#     message_prefix = userRequest_msg
#     buttons = _create_buttons(master_data, message_prefix)

#     return { "format": textCard_format(master_data, buttons), "meta_data": master_data }

# TODO: 아래 주석친 코드 필요시 사용 예정 (2025.09.17 minjae)
# def account_quickReplies(master_data: dict[str, Any]) -> dict[str, Any]:
#     """
#     Description: 계정 & 제품배정 문의 바로가기 그룹 json 포맷 가져오기

#     Parameters: master_data - 특정 마스터 데이터

#     Returns: quickReplies_format(master_data, buttons) - 계정 & 제품배정 문의 바로가기 그룹 json 포맷
#              master_data - 특정 마스터 데이터
#     """

#     message_prefix = chatbot_helper._accountType
#     buttons = _create_buttons(master_data, message_prefix)

#     return { "format": quickReplies_format(master_data, buttons), "meta_data": master_data }

# TODO: 아래 함수 end_basicCard 필요시 로직 수정 예정 (2025.09.05 minjae)
def end_basicCard(master_data: dict[str, Any], endInfos: list[dict]) -> dict[str, Any]:
    """
    Description: 마지막화면 기본형 카드 json 포맷 가져오기 

    Parameters: master_data - 특정 마스터 데이터
                endInfos - 특정 기술지원 정보 리스트 (예) 설치 (Autodesk or 상상진화 BOX 제품), 계정 & 제품배정 등등...

    Returns: outputs_format(outputs) - 마지막화면 기본형 카드 json 포맷
             master_data - 특정 마스터 데이터
    """

    buttons = []
    outputs = []

    # 브루트 포스 완전 탐색 알고리즘 (Brute Force Algorithm) - 무차별 대입법이라고 불리며, 문제를 해결하기 위해 가능한 경우의 수를 모두 검사(완전 탐색)해보는 방법이다.
    # 참고 URL - https://ko.wikipedia.org/wiki/%EB%AC%B4%EC%B0%A8%EB%B3%84_%EB%8C%80%EC%9E%85_%EA%B2%80%EC%83%89
    # 참고 2 URL - https://wikidocs.net/233719
    # 참고 3 URL - https://youtu.be/QhMY4t2xwG0?si=uYsaL7CLHmx-RHV8
    # 오류 메시지 "string indices must be integers, not 'str'" 출력되어 아래처럼 코드 변경 처리함. (2025.08.28 minjae)
    # (기존) master_data -> (변경) master_data[chatbot_helper._buttons]  
    for endButton in master_data[chatbot_helper._buttons]:   # 처음으로, 동영상, 만족도 조사 버튼 텍스트 및 메세지 추가
        if (chatbot_helper._video == endButton[chatbot_helper._label] 
            and chatbot_helper._yes == endInfos[chatbot_helper._webLinkUrl_Idx][chatbot_helper._videoYn]):   # 버튼이 '동영상'이고 동영상 시청 가능할 경우 ("videoYn": "Y") 
            buttons.append({
                "action": chatbot_helper._webLink,
                "label": endButton[chatbot_helper._label],
                "webLinkUrl": endInfos[chatbot_helper._webLinkUrl_Idx][chatbot_helper._webLinkUrl]
            })
        else:   # 동영상 시청이 불가능 ("videoYn": "N") 하거나 버튼이 "동영상" 아닐 경우 
            buttons.append({
                "action": chatbot_helper._message,
                "label": endButton[chatbot_helper._label],
                "messageText": endButton[chatbot_helper._messageText]
            })

    if endInfos[chatbot_helper._text_Idx][chatbot_helper._text]:   # endInfos[chatbot_helper._text_Idx][chatbot_helper._text]에 할당된 값이 null 또는 공백("")이 아닌 경우 (None or Empty String Check)
        outputs.append({
            "simpleText": {
                "text": endInfos[chatbot_helper._text_Idx][chatbot_helper._text]
            }
        })

    outputs.append({   # basicCard 항상 추가
        "basicCard": {
            "title": master_data[chatbot_helper._title],
            "description": master_data[chatbot_helper._description],
            "thumbnail": {
                "imageUrl": master_data[chatbot_helper._thumbnail][chatbot_helper._imageUrl],
                "link": {
                    "web": master_data[chatbot_helper._thumbnail][chatbot_helper._webLinkUrl]
                }
            },
            "buttons": buttons
        }
    })

    return { "format": outputs_format(outputs), "meta_data": master_data }