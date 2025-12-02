"""
* [카카오톡 서버 전송 용도] json 포맷 전용 모듈
참고 URL - https://chatgpt.com/c/69002b43-44c0-8322-8298-e7871b39da2a

* 파이썬 Type Hints
참고 URL - https://docs.python.org/ko/3.14/library/typing.html
참고 2 URL - https://peps.python.org/pep-0484/
참고 3 URL - https://devpouch.tistory.com/189
참고 4 URL - https://supermemi.tistory.com/entry/Python-3-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-%EC%9D%98%EB%AF%B8%EB%8A%94-%EB%AC%B4%EC%97%87%EC%9D%BC%EA%B9%8C-%EC%A3%BC%EC%84%9D

* 챗봇 응답 타입별 json 포맷
참고 URL - https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format

* 파이썬 패키지, 모듈 
참고 URL - https://docs.python.org/ko/3.13/tutorial/modules.html
참고 2 URL - https://wikidocs.net/1418
참고 3 URL - https://dojang.io/mod/page/view.php?id=2450
"""

# 1. 공통 모듈 먼저 import 처리
from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트

# 2. log 모듈 import 처리 
from utils.log import logger       # 챗봇 전역 로그 객체(logger)  

def outputs_json(outputs: list[dict]) -> dict:
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

def quickReplies_json(replies: dict, quickReplies: list[dict]) -> dict:
    """
    Description: 바로가기 그룹 json 포맷 가져오기

    Parameters: replies - 특정 마스터 데이터
                quickReplies - 버튼 리스트 (label + messageText)

    Returns: 바로가기 그룹 json 포맷
    """

    return {
        'version': '2.0', 
        'template': {
            'outputs': [
                {
                    "simpleText": {
                        "text": replies[chatbot_helper._description]
                    }
                }
            ], 
            'quickReplies': quickReplies
        }
    }

def textCard_json(card: dict, buttons: list[dict]) -> dict:
    """
    Description: 텍스트 카드 json 포맷 가져오기

    Parameters: card - 특정 마스터 데이터
                buttons - 버튼 리스트 (label + messageText) 

    Returns: 텍스트 카드 json 포맷
    """

    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "textCard": {
                        "title": card[chatbot_helper._title],
                        "description": card[chatbot_helper._description],
                        "buttons": buttons
                    }
                }
            ],
            "quickReplies": []
        }
    }

# TODO: 추후 필요시 함수 파라미터 quickReplies를 default 파라미터로 구현 예정 (2025.09.03 minjae)
def basicCard_json(card: dict, buttons: list[dict]) -> dict:
    """
    Description: 기본형 카드 json 포맷 가져오기

    Parameters: card - 특정 마스터 데이터
                buttons - 버튼 리스트 (label + messageText)

    Returns: 기본형 카드 json 포맷
    """

    outputs = []

    # card[chatbot_helper._text]에 할당된 값이 null 또는 공백("")일 경우 basicCard 가 카카오톡 채팅방에 출력 안되는 오류 발생함. 
    # 하여 null 또는 공백("")이 아닌 문자열로 할당 해야함. (2025.09.03 minjae)
    # 참고 URL - https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty-in-python
    # 참고 2 URL - https://hello-bryan.tistory.com/131
    # 참고 3 URL - https://jino-dev-diary.tistory.com/42
    # 참고 4 URL - https://claude.ai/chat/eaf7856e-1b5e-4c26-992e-de1683005638
    if card[chatbot_helper._text]:   # card[chatbot_helper._text]에 할당된 값이 null 또는 공백("")이 아닌 경우 (None or Empty String Check)
        outputs.append({
            "simpleText": {
                "text": card[chatbot_helper._text]
            }
        })

    outputs.append({   # basicCard 항상 추가
        "basicCard": {
            "title": card[chatbot_helper._title],
            "description": card[chatbot_helper._description],
            "thumbnail": {
                "imageUrl": card[chatbot_helper._thumbnail][chatbot_helper._imageUrl],
                "link": {
                    "web": card[chatbot_helper._thumbnail][chatbot_helper._webLinkUrl]
                }
            },
            "buttons": buttons
        }
    })

    return outputs_json(outputs)

def carousel_json(card: dict, items: list[dict]) -> dict:
    """
    Description: 아이템형 케로셀 json 포맷 가져오기

    Parameters: card - 특정 마스터 데이터
                items - 아이템 리스트 (imageTitle + thumbnail + itemList 등등...) 

    Returns: 아이템형 케로셀 json 포맷 
    """
    
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": card[chatbot_helper._text]
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

# TODO: 아래 함수 empty_response 필요시 로직 수정 예정 (2025.09.03 minjae) 
def empty_response() -> dict:
    """
    Description: 기술지원 문의 제외 일반 문의 json 포맷 가져오기
                 카카오톡 채팅방에 응답 메시지를 출력하고 싶지 않은 경우 비어있는 메세지 전송 

    Parameters: 없음.

    Returns: 기술지원 문의 제외 일반 문의 json 포맷
    """

    return {
        'version': '2.0', 
        'template': {
            'outputs': [], 
            'quickReplies': []
        }
    }    

def simple_text(text: str) -> dict:
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
# def simple_image(text: str, prompt: str) -> dict:
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

def error_text(error_msg: str) -> dict:
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

def timeOver_quickReplies(requestAgain_msg: str) -> dict:
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

def common_basicCard(card: dict) -> tuple[dict, dict]:
    """
    Description: [공통] 기본형 카드 json 포맷 가져오기 

    Parameters: card - 특정 마스터 데이터

    Returns: basicCard_json(card, buttons) - [공통] 기본형 카드 json 포맷
             card - 특정 마스터 데이터
    """

    buttons = []
    
    # 그리디 알고리즘 (Greedy Algorithm) - 탐욕법이라고 불리며, 현재 상황에서 지금 당장 좋은 것만 고르는 방법이다.
    # 참고 URL - https://youtu.be/5OYlS2QQMPA?si=LzCRpZvGmEXI5Ean
    # 참고 2 URL - https://youtu.be/_TG0hVYJ6D8?si=j85mnzUabJeClsoQ
    for basicButton in card[chatbot_helper._buttons]:   # [공통] 기본형 카드 버튼 텍스트 및 메세지 추가 
        if basicButton[chatbot_helper._webLinkUrl]:   # basicButton[chatbot_helper._webLinkUrl]에 할당된 값이 null 또는 공백("")이 아닌 경우 (None or Empty String Check)
            buttons.append({
                "action": chatbot_helper._webLink,
                "label": basicButton[chatbot_helper._label], 
                "webLinkUrl": basicButton[chatbot_helper._webLinkUrl]
            })

        else:   # basicButton[chatbot_helper._webLinkUrl]에 할당된 값이 null 또는 공백("")인 경우
            buttons.append({
                "action": chatbot_helper._message,
                "label": basicButton[chatbot_helper._label],
                "messageText": basicButton[chatbot_helper._messageText]
            })

    return (basicCard_json(card, buttons), card)
    
def common_quickReplies(replies: dict) -> tuple[dict, dict]:
    """
    Description: [공통] 바로가기 그룹 json 포맷 가져오기

    Parameters: replies - 특정 마스터 데이터

    Returns: quickReplies_json(replies, quickReplies) - [공통] 바로가기 그룹 json 포맷
             replies - 특정 마스터 데이터
    """

    quickReplies = []

    # 그리디 알고리즘 (Greedy Algorithm) - 탐욕법이라고 불리며, 현재 상황에서 지금 당장 좋은 것만 고르는 방법이다.
    # 참고 URL - https://youtu.be/5OYlS2QQMPA?si=LzCRpZvGmEXI5Ean
    # 참고 2 URL - https://youtu.be/_TG0hVYJ6D8?si=j85mnzUabJeClsoQ
    for repliesButton in replies[chatbot_helper._buttons]:   # [공통] 바로가기 그룹 버튼 텍스트 및 메세지 추가 
        if repliesButton[chatbot_helper._webLinkUrl]:   # repliesButton[chatbot_helper._webLinkUrl]에 할당된 값이 null 또는 공백("")이 아닌 경우 (None or Empty String Check)
            quickReplies.append({
                "action": chatbot_helper._webLink,
                "label": repliesButton[chatbot_helper._label], 
                "webLinkUrl": repliesButton[chatbot_helper._webLinkUrl]
            })

        else:   # repliesButton[chatbot_helper._webLinkUrl]에 할당된 값이 null 또는 공백("")인 경우
            quickReplies.append({
                "action": chatbot_helper._message,
                "label": repliesButton[chatbot_helper._label],
                "messageText": repliesButton[chatbot_helper._messageText]
            }) 

    return (quickReplies_json(replies, quickReplies), replies)

def common_ver_quickReplies(userRequest_msg: str, verReplies: dict) -> tuple[dict, dict]:
    """
    Description: [공통] Autodesk or 상상진화 BOX 제품 버전 바로가기 그룹 json 포맷 가져오기

    Parameters: userRequest_msg - 사용자 입력 채팅 메세지
                verReplies - 특정 마스터 데이터

    Returns: quickReplies_json(verReplies, verQuickReplies) - [공통] Autodesk or 상상진화 BOX 제품 버전 바로가기 그룹 json 포맷
             verReplies - 특정 마스터 데이터
    """

    verQuickReplies = []
     
    for verButton in verReplies[chatbot_helper._buttons]:   # [공통] Autodesk or 상상진화 BOX 제품 버전 바로가기 그룹 버튼 텍스트 및 메세지 추가
        verQuickReplies.append({
            "action": chatbot_helper._message,
            "label": verButton[chatbot_helper._label],
            "messageText": f"{chatbot_helper._instType} {userRequest_msg} {verButton[chatbot_helper._messageText]}"
        })

    return (quickReplies_json(verReplies, verQuickReplies), verReplies)

# TODO: 아래 함수 get_response 필요시 로직 수정 예정 (2025.09.04 minjae)
def get_response(userRequest_msg: str, masterEntity: dict) -> tuple[dict, dict]:
    """
    Description: 카카오 json 포맷 가져오기  

    Parameters: userRequest_msg - 사용자 입력 채팅 메세지 
                masterEntity - 마스터 데이터 담는 싱글톤(singleton) 객체   

    Returns: response - 카카오 json 포맷 기반 챗봇 답변 내용
             master_data - 특정 마스터 데이터 (예) 아이템 카드 (basicCard, carousel) or 바로가기 그룹 (quickReplies)
    """

    response = None   

    # 아래와 같은 오류 메시지 출력되어 (기존) masterEntity.get_master_datas() -> (변경) masterEntity.get_master_datas 처리함. (2025.09.16 minjae)
    # 오류 메시지 - 'dict' object is not callable
    # master_datas = masterEntity.get_master_datas()
    master_datas = masterEntity.get_master_datas   # 전체 마스터 데이터  
    master_data = None   # 특정 마스터 데이터     

    chatbot_messageTexts = masterEntity.get_chatbot_messageTexts   # [챗봇 문의] 버튼 메시지 리스트    
    adsk_messageTexts = masterEntity.get_adsk_messageTexts         # [Autodesk 제품 설치 문의] 버튼 메시지 리스트
    box_messageTexts = masterEntity.get_box_messageTexts           # [상상진화 BOX 제품 설치 문의] 버튼 메시지 리스트 

    try:
        logger.info("[테스트] 카카오 json 포맷 가져오기 - 시작!") 
        # logger.info(f"[테스트] master_datas - {master_datas}")
        # logger.info(f"[테스트] chatbot_messageTexts - {chatbot_messageTexts}")
        # logger.info(f"[테스트] adsk_messageTexts - {adsk_messageTexts}")
        # logger.info(f"[테스트] box_messageTexts - {box_messageTexts}")
    
        # TODO: 아래 주석친 코드 필요시 참고 (2025.08.27 minjae)
        # raise Exception(chatbot_helper._error_title + 
        #                 '사유: 카카오 json 포맷 가져오기 오류 발생!!!\n'+
        #                 chatbot_helper._error_ssflex)   # 예외 발생시킴

        if (chatbot_helper._start in userRequest_msg or chatbot_helper._beginning in userRequest_msg):   # start - 시작 화면 or 처음으로
            (response, master_data) = common_basicCard(master_datas[chatbot_helper._startCard])

        elif chatbot_helper._remote_text == userRequest_msg:   # level1 - 원격 지원
            response = empty_response()
            master_data = master_datas[chatbot_helper._startCard]

        elif chatbot_helper._ask_chatbot == userRequest_msg:   # level1 - 챗봇 문의 
            (response, master_data) = chatbot_carousel(master_datas[chatbot_helper._chatbotCard])

        elif userRequest_msg in chatbot_messageTexts:   # level2 - 문의 유형 
            (response, master_data) = subCat_basicCard(userRequest_msg, master_datas[chatbot_helper._subCatCard])

        elif chatbot_helper._instSupport_adskProduct == userRequest_msg:   # level3 - Autodesk 제품 설치 문의
            (response, master_data) = common_quickReplies(master_datas[chatbot_helper._adskReplies])

        elif userRequest_msg in adsk_messageTexts:   # level4 - Autodesk 제품 버전
            (response, master_data) = common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._adskVerReplies])

        elif chatbot_helper._instSupport_boxProduct == userRequest_msg:   # level3 - 상상진화 BOX 제품 설치 문의
            (response, master_data) = common_quickReplies(master_datas[chatbot_helper._boxReplies])

        elif userRequest_msg in box_messageTexts:   # level4 - 상상진화 BOX 제품 버전
            (response, master_data) = common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._boxVerReplies])

        # TODO: 아래 주석친 코드 필요시 사용 예정 (2025.08.27 minjae)
        # elif chatbot_helper._ask_accountProduct == userRequest_msg:   # level3 - 계정 & 제품배정 문의 
        #     (response, master_data) = account_quickReplies(master_datas[chatbot_helper._accountReplies])

        elif (chatbot_helper._instType in userRequest_msg):   # end - 텍스트 + basicCard Autodesk or 상상진화 BOX 제품 설치 방법 
            # 상상진화 BOX 제품 2025, 2026 버전 공통 설치 방법
            if (chatbot_helper._revitBox in userRequest_msg):   # RevitBOX
                (response, master_data) = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._revitBoxInfos])  

            elif (chatbot_helper._cadBox in userRequest_msg):   # CADBOX
                (response, master_data) = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._cadBoxInfos])
     
            elif (chatbot_helper._energyBox in userRequest_msg):   # EnergyBOX
                (response, master_data) = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._energyBoxInfos])

            # Autodesk 제품 2025, 2026 버전 공통 설치 방법
            elif (chatbot_helper._autoCAD in userRequest_msg):   # AutoCAD  
                (response, master_data) = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._autoCADInfos])   

            elif (chatbot_helper._revit in userRequest_msg):   # Revit 
                (response, master_data) = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._revitInfos])   

            elif (chatbot_helper._navisworksManage in userRequest_msg):   # Navisworks Manage
                (response, master_data) = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._navisworksManageInfos])   

            elif (chatbot_helper._infraWorks in userRequest_msg):   # InfraWorks
                (response, master_data) = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._infraWorksInfos])   
                
            elif (chatbot_helper._civil3D in userRequest_msg):   # Civil3D 
                (response, master_data) = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._civil3DInfos])   
        
        # TODO: 아래 주석친 코드 필요시 사용 예정 (2025.08.27 minjae)
        # elif chatbot_helper._survey in userRequest_msg:   # 만족도 조사
        #     (response, master_data) = common_basicCard(master_datas[chatbot_helper._surveyCard])
        
        # 사용자가 카카오 챗봇 버튼이 아닌 일반 메시지를 채팅창에 입력시 아래처럼 오류 메시지가 출력되어 원인 파악 결과 response 변수가 None으로 리턴되어 
        # lambda_function.py 소스파일 -> chatbot_response 함수에서 res_queue.put(response) 실행할 때 발생하는 오류로 확인 되어 아래처럼 else 절 코드 추가 (2025.09.12 minjae)
        # 참고 URL - https://claude.ai/chat/2035baf1-0f86-4d08-af37-0091c8358dbb
        # 오류 메시지 - "TypeError: 'NoneType' object is not subscriptable"
        else:   # 기술지원 문의 제외 일반 문의 
            response = empty_response()

        # TODO: 아래 주석친 코드 필요시 사용 예정 (2025.09.05 minjae)
        # elif (chatbot_helper._accountType in userRequest_msg):  # end - 텍스트 + basicCard 계정 & 제품배정 
        #     if chatbot_helper._anyQuestion in userRequest_msg:   # '기타 문의' 
        #         (response, master_data) = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._accountInfos][chatbot_helper._anyQuestion])

        #     elif chatbot_helper._resetPassword in userRequest_msg:   # '계정 비밀번호 분실'
        #         (response, master_data) = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._accountInfos][chatbot_helper._resetPassword])

        #     else:   # [구현 예정!] '기타 문의', '계정 비밀번호 분실' 제외한 다른 문의 
        #         (response, master_data) = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._etcInfos][chatbot_helper._etcTest])

        logger.info("[테스트] 카카오 json 포맷 가져오기 - 완료!")
        return (response, master_data) 
        
    except Exception as e:     
        error_msg = str(e)
        logger.error(f"[테스트] 오류 - {error_msg}")
        raise       

def chatbot_carousel(chatbotCard: dict) -> tuple[dict, dict]:
    """  
    Description: 챗봇 문의 아이템형 케로셀 json 포맷 가져오기

    Parameters: chatbotCard - 특정 마스터 데이터

    Returns: carousel_json(chatbotCard, chatbot_items) - 챗봇 문의 아이템형 케로셀 json 포맷
             chatbotCard - 특정 마스터 데이터
    """

    chatbotButtons = []
     
    for chatbotButton in chatbotCard[chatbot_helper._buttons]:   # 챗봇 문의 아이템형 케로셀 3가지 버튼 텍스트 및 메세지 추가
        chatbotButtons.append({
            "action": chatbot_helper._message,
            "label": chatbotButton[chatbot_helper._label],
            "messageText": chatbotButton[chatbot_helper._messageText]
        })

    chatbot_items = []
    chatbot_items.append({
        "imageTitle": {
            "title": chatbotCard[chatbot_helper._title],
            "description": chatbotCard[chatbot_helper._description]
        },
        # "title": "",
        # "description": "",
        "thumbnail": {
            "imageUrl": chatbotCard[chatbot_helper._thumbnail][chatbot_helper._imageUrl],
            "link": {
                "web": chatbotCard[chatbot_helper._thumbnail][chatbot_helper._webLinkUrl]
            }
        },
        "itemList": [
            {
                "title": chatbotCard[chatbot_helper._itemList][chatbot_helper._chatbotItem_Idx][chatbot_helper._title],
                "description": chatbotCard[chatbot_helper._itemList][chatbot_helper._chatbotItem_Idx][chatbot_helper._description]
            }
        ],
        "itemListAlignment": "left",
        "buttons": chatbotButtons,
        "buttonLayout": "vertical"
    })

    return (carousel_json(chatbotCard, chatbot_items), chatbotCard)

def subCat_basicCard(userRequest_msg: str, subCatCard: dict) -> tuple[dict, dict]:
    """
    Description: 문의 유형 기본형 카드 json 포맷 가져오기 

    Parameters: userRequest_msg - 사용자 입력 채팅 메세지
                subCatCard - 특정 마스터 데이터

    Returns: basicCard_json(subCatCard, subCatButtons) - 문의 유형 기본형 카드 json 포맷
             subCatCard - 특정 마스터 데이터
    """

    subCatButtons = []
    
    # 그리디 알고리즘 (Greedy Algorithm) - 탐욕법이라고 불리며, 현재 상황에서 지금 당장 좋은 것만 고르는 방법이다.
    # 참고 URL - https://youtu.be/5OYlS2QQMPA?si=LzCRpZvGmEXI5Ean
    # 참고 2 URL - https://youtu.be/_TG0hVYJ6D8?si=j85mnzUabJeClsoQ 
    for subCatButton in subCatCard[chatbot_helper._buttons]:   # 문의 유형 기본형 카드 버튼 텍스트 및 메세지 추가
        messageText = None   

        # 변수(subCatButton[chatbot_helper._label])에 저장된 값이 '설치 문의' and 변수(userRequest_msg)에 저장된 값이 'Autodesk 제품' 또는 '상상진화 BOX 제품'인 경우 
        if (chatbot_helper._askInst == subCatButton[chatbot_helper._label] and chatbot_helper._accountProduct != userRequest_msg):
            messageText = f"{userRequest_msg} {subCatButton[chatbot_helper._messageText]}"

        # 변수(subCatButton[chatbot_helper._label])에 저장된 값이 '계정 & 제품배정 문의'인 경우 and 변수(userRequest_msg)에 저장된 값이 '계정 & 제품배정'인 경우 
        elif (chatbot_helper._ask_accountProduct == subCatButton[chatbot_helper._label] and chatbot_helper._accountProduct == userRequest_msg):
            messageText = subCatButton[chatbot_helper._messageText]

        if None is messageText: continue   # 위 2가지 조건에 해당되지 않는 경우 continue 처리

        subCatButtons.append({
            "action": chatbot_helper._message,
            "label": subCatButton[chatbot_helper._label],
            "messageText": messageText
        })

    return (basicCard_json(subCatCard, subCatButtons), subCatCard)

# TODO: 아래 주석친 코드 필요시 사용 예정 (2025.09.17 minjae)
# def adskLang_textCard(userRequest_msg: str, adskLangCard: dict) -> tuple[dict, dict]:
#     """
#     Description: Autodesk 제품 설치 언어 텍스트 카드 json 포맷 가져오기

#     Parameters: userRequest_msg - 사용자 입력 채팅 메세지
#                 adskLangCard - 특정 마스터 데이터

#     Returns: textCard_json(adskLangCard, adskLangButtons) - Autodesk 제품 설치 언어 텍스트 카드 json 포맷
#              adskLangCard - 특정 마스터 데이터
#     """

#     adskLangButtons = []
     
#     for adskLangButton in adskLangCard[chatbot_helper._buttons]:   # Autodesk 제품 설치 언어 텍스트 카드 버튼 텍스트 및 메세지 추가
#         adskLangButtons.append({
#             "action": chatbot_helper._message,
#             "label": adskLangButton[chatbot_helper._label],
#             "messageText": f"{userRequest_msg} {adskLangButton[chatbot_helper._messageText]}"
#         })

#     return (textCard_json(adskLangCard, adskLangButtons), adskLangCard)

# TODO: 아래 주석친 코드 필요시 사용 예정 (2025.09.17 minjae)
# def account_quickReplies(accountReplies: dict) -> tuple[dict, dict]:
#     """
#     Description: 계정 & 제품배정 문의 바로가기 그룹 json 포맷 가져오기

#     Parameters: accountReplies - 특정 마스터 데이터

#     Returns: quickReplies_json(accountReplies, accountQuickReplies) - 계정 & 제품배정 문의 바로가기 그룹 json 포맷
#              accountReplies - 특정 마스터 데이터
#     """

#     accountQuickReplies = []
     
#     for accountButton in accountReplies[chatbot_helper._buttons]:   # 계정 & 제품배정 문의 바로가기 그룹 버튼 텍스트 및 메세지 추가 
#         messageText = f"{chatbot_helper._accountType} {accountButton[chatbot_helper._messageText]}"
#         accountQuickReplies.append({
#             "action": chatbot_helper._message,
#             "label": accountButton[chatbot_helper._label],
#             "messageText": messageText
#         })

#     return (quickReplies_json(accountReplies, accountQuickReplies), accountReplies)

# TODO: 아래 함수 end_basicCard 필요시 로직 수정 예정 (2025.09.05 minjae)
def end_basicCard(endCard: dict, endInfos: list[dict]) -> tuple[dict, dict]:
    """
    Description: 마지막화면 기본형 카드 json 포맷 가져오기 

    Parameters: endCard - 특정 마스터 데이터
                endInfos - 특정 기술지원 정보 리스트 (예) 설치 (Autodesk or 상상진화 BOX 제품), 계정 & 제품배정 등등...

    Returns: outputs_json(outputs) - 마지막화면 기본형 카드 json 포맷
             endCard - 특정 마스터 데이터
    """

    endButtons = []
    outputs = []

    # 그리디 알고리즘 (Greedy Algorithm) - 탐욕법이라고 불리며, 현재 상황에서 지금 당장 좋은 것만 고르는 방법이다.
    # 참고 URL - https://youtu.be/5OYlS2QQMPA?si=LzCRpZvGmEXI5Ean
    # 참고 2 URL - https://youtu.be/_TG0hVYJ6D8?si=j85mnzUabJeClsoQ
    # 오류 메시지 "string indices must be integers, not 'str'" 출력되어 아래처럼 코드 변경 처리함. (2025.08.28 minjae)
    # (기존) endCard -> (변경) endCard[chatbot_helper._buttons]  
    for endButton in endCard[chatbot_helper._buttons]:   # 처음으로, 동영상, 만족도 조사 버튼 텍스트 및 메세지 추가
        if (chatbot_helper._video == endButton[chatbot_helper._label] 
            and chatbot_helper._yes == endInfos[chatbot_helper._webLinkUrl_Idx][chatbot_helper._videoYn]):   # 버튼이 '동영상'이고 동영상 시청 가능할 경우 ("videoYn": "Y") 
            endButtons.append({
                "action": chatbot_helper._webLink,
                "label": endButton[chatbot_helper._label],
                "webLinkUrl": endInfos[chatbot_helper._webLinkUrl_Idx][chatbot_helper._webLinkUrl]
            })
        else:   # 동영상 시청이 불가능 ("videoYn": "N") 하거나 버튼이 "동영상" 아닐 경우 
            endButtons.append({
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
            "title": endCard[chatbot_helper._title],
            "description": endCard[chatbot_helper._description],
            "thumbnail": {
                "imageUrl": endCard[chatbot_helper._thumbnail][chatbot_helper._imageUrl],
                "link": {
                    "web": endCard[chatbot_helper._thumbnail][chatbot_helper._webLinkUrl]
                }
            },
            "buttons": endButtons
        }
    })

    return (outputs_json(outputs), endCard)