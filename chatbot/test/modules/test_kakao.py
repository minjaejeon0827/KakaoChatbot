# [카카오톡 서버 전송 용도] json 포맷 전용 모듈

# 챗봇 응답 타입별 JSON 포맷
# 참고 URL - https://kakaobusiness.gitbook.io/main/tool/chatbot/skill_guide/answer_json_format

# import logging   # 로그 작성 라이브러리

from modules import chatbot_logger           # 폴더 "modules" -> 챗봇 로그 작성 모듈 
from commons import chatbot_helper   # 폴더 "commons" -> 챗봇 전용 도움말 텍스트 

# "outputs" json 포맷
def outputs_json(outputs):
    return {
        "version": "2.0",
        "template": {
            "outputs": outputs,
            "quickReplies": []
        }
    }


# "quickReplies" json 포맷
def quickReplies_json(replies, quickReplies):
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

# "textCard" json 포맷
def textCard_json(card, buttons):
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "textCard": {
                        "title": card[chatbot_helper._title],
                        "description": card[chatbot_helper._description],
                        "buttons" : buttons
                    }
                }
            ],
            "quickReplies": []
        }
    }

# TODO: 추후 필요시 함수 파라미터 quickReplies를 default 파라미터로 구현 예정 (2025.09.03 minjae)
# "basicCard" json 포맷
def basicCard_json(card, buttons):
    outputs = []

    # TODO: card[chatbot_helper._botRes]에 할당된 값이 null 또는 공백("")일 경우 basicCard 가 카카오톡 채팅방에 출력 안되는 오류 발생함. 
    #       하여 null 또는 공백("")이 아닌 문자열로 할당 해야함. (2025.09.03 minjae)
    # 참고 URL - https://stackoverflow.com/questions/9573244/how-to-check-if-the-string-is-empty-in-python
    # 참고 2 URL - https://hello-bryan.tistory.com/131
    # 참고 3 URL - https://jino-dev-diary.tistory.com/42
    # 참고 4 URL - https://claude.ai/chat/eaf7856e-1b5e-4c26-992e-de1683005638
    if card[chatbot_helper._botRes]:   # card[chatbot_helper._botRes]에 할당된 값이 null 또는 공백("")이 아닌 경우 (None or Empty String Check)
        outputs.append({
            "simpleText": {
                "text": card[chatbot_helper._botRes]
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

# "carousel" json 포맷
def carousel_json(card, items):
    return {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": card[chatbot_helper._botRes]
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

# TODO: 아래 함수 base_response 필요시 로직 수정 예정 (2025.09.03 minjae)
# 비어있는 메세지 전송 (카카오톡 서버로 비어있는 메시지 전송)
# 카카오톡 채팅방에 메시지를 출력하고 싶지 않은 경우 사용 
def base_response():
    return {
        'version': '2.0', 
        'template': {
            'outputs': [], 
            'quickReplies': []
        }
    } 

# 텍스트 메세지 전송 (카카오톡 서버로 텍스트 전송)
# 카카오톡 채팅방에 보낼 메시지를 매개변수 botRes에 input으로 받기(인자로 전달)
def simple_text(botRes):
    # 카카오톡 채팅방에 보낼 메시지가 저장된 매개변수 botRes를
    # 아래 json 형태(Format)에서 항목 'outputs' -> 항목 "simpleText" -> "text"안에 매개변수 botRes를 넣어서
    # 변수 res에 저장하기 
    return {
        'version': '2.0', 
        'template': {
            'outputs': [
                {
                    "simpleText": {
                        "text": botRes
                    }
                }
            ], 
            'quickReplies': []
        }
    } 

# 그림 전송 (카카오톡 서버로 그림 전송)
def simple_image(botRes, prompt):
    output_text = prompt + "내용에 관한 이미지 입니다"
    return {
        'version': '2.0', 
        'template': {
            'outputs': [
                {
                    "simpleImage": {
                        "imageUrl": botRes,
                        "altText": output_text
                    }
                }
            ], 
            'quickReplies': []
        }
    }   

# 오류 메세지 전송 (카카오톡 서버로 텍스트 전송)
# 오류 발생시 카카오톡 서버로 오류 메시지 전송 전용 JSON 형태(Format)의 데이터로 전달하기 위한 함수
# 카카오톡 채팅방에 보낼 메시지를 매개변수 error_msg에 input으로 받기(인자로 전달)
def error_text(error_msg):
    # 카카오톡 채팅방에 보낼 메시지가 저장된 매개변수 error_msg를
    # 아래 json 형태(Format)에서 항목 'outputs' -> 항목 "simpleText" -> "text"안에 매개변수 error_msg을 넣어서
    # 변수 res에 저장하기 
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
                    "action": "message",
                    "label": chatbot_helper._beginning,
                    "messageText": chatbot_helper._beginning
                }
            ]
        }
    }    

# 시간 5초 초과시 응답 (바로가기 그룹 전송)
def timeover_quickReplies(requestAgain_msg):
    return {
        "version":"2.0",
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
                    "action": "message",
                    "label": requestAgain_msg,
                    "messageText": requestAgain_msg
                }
            ]
        }
    }   

# 공통 - 기본형 카드 (카카오톡 서버로 기본 카드 전송)
def common_basicCard(card):
    buttons = []
    
    for basicButton in card[chatbot_helper._buttons]:   # 기본형 카드 버튼 텍스트 및 메세지 추가 
        if basicButton[chatbot_helper._webLinkUrl]:   # basicButton[chatbot_helper._webLinkUrl]에 할당된 값이 null 또는 공백("")이 아닌 경우 (None or Empty String Check)
            buttons.append({
                "action":  "webLink",
                "label": basicButton[chatbot_helper._label], 
                "webLinkUrl": basicButton[chatbot_helper._webLinkUrl]
            })

        else:   # basicButton[chatbot_helper._webLinkUrl]에 할당된 값이 null 또는 공백("")인 경우
            buttons.append({
                "action": "message",
                "label": basicButton[chatbot_helper._label],
                "messageText": basicButton[chatbot_helper._messageText]
            })

    return basicCard_json(card, buttons), card
   
# 공통 - 바로가기 그룹 (카카오톡 서버로 바로가기 그룹 전송) 
def common_quickReplies(replies):
    quickReplies = []

    for repliesButton in replies[chatbot_helper._buttons]:   # 바로가기 그룹 버튼 텍스트 및 메세지 추가 
        if repliesButton[chatbot_helper._webLinkUrl]:   # repliesButton[chatbot_helper._webLinkUrl]에 할당된 값이 null 또는 공백("")이 아닌 경우 (None or Empty String Check)
            quickReplies.append({
                "action":  "webLink",
                "label": repliesButton[chatbot_helper._label], 
                "webLinkUrl": repliesButton[chatbot_helper._webLinkUrl]
            })

        else:   # repliesButton[chatbot_helper._webLinkUrl]에 할당된 값이 null 또는 공백("")인 경우
            quickReplies.append({
                "action": "message",
                "label": repliesButton[chatbot_helper._label],
                "messageText": repliesButton[chatbot_helper._messageText]
            }) 

    return quickReplies_json(replies, quickReplies), replies

# 공통 - level4 Autodesk or 상상진화 BOX 제품 버전 바로가기 그룹 (카카오톡 서버로 바로가기 그룹 전송)
def common_ver_quickReplies(userRequest_msg, verReplies):
    verQuickReplies = []
     
    for verButton in verReplies[chatbot_helper._buttons]:   # Autodesk or 상상진화 BOX 제품 버전 버튼 텍스트 및 메세지 추가
        verQuickReplies.append({
            "action": "message",
            "label": verButton[chatbot_helper._label],
            "messageText": f"{chatbot_helper._instType} {userRequest_msg} {verButton[chatbot_helper._messageText]}"
        })

    return quickReplies_json(verReplies, verQuickReplies), verReplies

# TODO: 아래 함수 get 필요시 로직 수정 예정 (2025.09.04 minjae)
# 카카오 json 포맷 가져오기 
def get(userRequest_msg, masterEntity):
    resFormat = None   # 카카오 json format 형식 기반 챗봇 답변 내용  

    # TODO: 아래와 같은 오류 메시지 출력되어 (기존) masterEntity.get_master_datas() -> (변경) masterEntity.get_master_datas 처리함. (2025.09.16 minjae)
    # 오류 메시지 - 'dict' object is not callable
    # master_datas = masterEntity.get_master_datas()
    master_datas = masterEntity.get_master_datas   # 전체 마스터 데이터 객체 (Dictionary) 
    master_data = None   # 챗봇 특정 아이템 카드(basicCard, carousel) or 바로가기 그룹(quickReplies) 마스터 데이터 객체  

    chatbot_messageTexts = masterEntity.get_chatbot_messageTexts   # [챗봇 문의] 버튼 메시지 텍스트 리스트    
    adsk_messageTexts = masterEntity.get_adsk_messageTexts   # [Autodesk 제품 설치 문의] 버튼 메시지 텍스트 리스트
    box_messageTexts = masterEntity.get_box_messageTexts   # [상상진화 BOX 제품 설치 문의] 버튼 메시지 텍스트 리스트 

    try:
        # TODO: 아래 변수 testlogger를 챗봇 프로그램에서 전역 로그 객체로 사용할 수 있도록 싱글톤 패턴으로 구현하기 (2025.09.17 minjae) 
        # testlogger = logging.getLogger()
        # testlogger.setLevel("INFO")
        # testlogger.info('[테스트] 카카오 json 포맷 가져오기: Start!') 
        chatbot_logger.log_write(chatbot_logger._info, '[테스트] 카카오 json 포맷 가져오기', 'Start!')
        chatbot_logger.log_write(chatbot_logger._info, '[테스트] master_datas', master_datas)
        chatbot_logger.log_write(chatbot_logger._info, '[테스트] chatbot_messageTexts', chatbot_messageTexts)
        chatbot_logger.log_write(chatbot_logger._info, '[테스트] adsk_messageTexts', adsk_messageTexts)
        chatbot_logger.log_write(chatbot_logger._info, '[테스트] box_messageTexts', box_messageTexts)   
    
        # TODO: 아래 주석친 코드 필요시 참고 (2025.08.27 minjae)
        # raise Exception(chatbot_helper._error_title + 
        #                 '사유: 카카오 json 포맷 가져오기 오류 발생!!!\n'+
        #                 '추가 문의 필요시\n'+
        #                 chatbot_helper._error_ssflex)   # 예외 발생시킴

        if (chatbot_helper._start in userRequest_msg or chatbot_helper._beginning in userRequest_msg):   # start - 시작 화면 or 처음으로
            resFormat, master_data = common_basicCard(master_datas[chatbot_helper._startCard])

        elif chatbot_helper._remote_botRes == userRequest_msg:   # level1 - 원격 지원
            resFormat = base_response()
            master_data = master_datas[chatbot_helper._startCard]

        elif chatbot_helper._chatbot == userRequest_msg:   # level1 - 챗봇 문의 
            resFormat, master_data = chatbot_carousel(master_datas[chatbot_helper._chatbotCard])

        elif userRequest_msg in chatbot_messageTexts:   # level2 - 문의 유형 
            resFormat, master_data = subCat_basicCard(userRequest_msg, master_datas[chatbot_helper._subCatCard])

        elif chatbot_helper._askInst_adskProduct == userRequest_msg:   # level3 - Autodesk 제품 설치 문의
            resFormat, master_data = common_quickReplies(master_datas[chatbot_helper._adskReplies])

        elif userRequest_msg in adsk_messageTexts:   # level4 - Autodesk 제품 버전
            resFormat, master_data = common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._adskVerReplies])

        elif chatbot_helper._askInst_boxProduct == userRequest_msg:   # level3 - 상상진화 BOX 제품 설치 문의
            resFormat, master_data = common_quickReplies(master_datas[chatbot_helper._boxReplies])

        elif userRequest_msg in box_messageTexts:   # level4 - 상상진화 BOX 제품 버전
            resFormat, master_data = common_ver_quickReplies(userRequest_msg, master_datas[chatbot_helper._boxVerReplies])

        # TODO: 아래 주석친 코드 필요시 사용 예정 (2025.08.27 minjae)
        # elif chatbot_helper._ask_accountProduct == userRequest_msg:   # level3 - 계정 & 제품배정 문의 
        #     resFormat, master_data = account_quickReplies(master_datas[chatbot_helper._accountReplies])  

        # TODO: 추후 필요시 동영상 시청 가능할 경우("videoYn": "Y")만 master_datas[chatbot_helper._endCard][chatbot_helper._buttons][chatbot_helper._videoButton_Idx][chatbot_helper._webLinkUrl] 속성에 값 할당 기능 구현하기 (2025.08.27 minjae)
        elif (chatbot_helper._instType in userRequest_msg):   # end - 텍스트 + basicCard Autodesk or 상상진화 BOX 제품 설치 방법 
            # 상상진화 BOX 제품 2025, 2026 버전 공통 설치 방법 텍스트 가져오기
            if (chatbot_helper._revitBox in userRequest_msg):   # RevitBOX     
                resFormat, master_data = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._revitBoxInfos])  

            elif (chatbot_helper._cadBox in userRequest_msg):   # CADBOX
                resFormat, master_data = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._cadBoxInfos])
     
            elif (chatbot_helper._energyBox in userRequest_msg):   # EnergyBOX
                resFormat, master_data = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._energyBoxInfos])

            # Autodesk 제품 2025, 2026 버전 공통 설치 방법 텍스트 가져오기
            elif (chatbot_helper._autoCAD in userRequest_msg):     # AutoCAD  
                resFormat, master_data = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._autoCADInfos])   

            elif (chatbot_helper._revit in userRequest_msg):   # Revit 
                resFormat, master_data = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._revitInfos])   

            elif (chatbot_helper._navisworksManage in userRequest_msg):   # Navisworks Manage
                resFormat, master_data = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._navisworksManageInfos])   

            elif (chatbot_helper._infraWorks in userRequest_msg):   # InfraWorks
                resFormat, master_data = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._infraWorksInfos])   
                
            elif (chatbot_helper._civil3D in userRequest_msg):   # Civil3D 
                resFormat, master_data = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._civil3DInfos])   
        
        elif chatbot_helper._survey in userRequest_msg:   # 만족도 조사
            resFormat, master_data = common_basicCard(master_datas[chatbot_helper._surveyCard])
        
        # TODO: 사용자가 카카오 챗봇 버튼이 아닌 일반 메시지를 채팅창에 입력시 아래처럼 오류 메시지가 출력되어 원인 파악 결과 resFormat 변수가 None으로 리턴되어 
        #       lambda_function.py 소스파일 -> resChatbot 함수에서 res_queue.put(resFormat) 실행할 때 발생하는 오류로 확인 되어 아래처럼 else 절 코드 추가 (2025.09.12 minjae)
        # 참고 URL - https://claude.ai/chat/2035baf1-0f86-4d08-af37-0091c8358dbb
        # 오류 메시지 - "TypeError: 'NoneType' object is not subscriptable"
        else:   # 기술지원 문의 제외 일반 문의
            resFormat = base_response()

        # TODO: 아래 주석친 코드 필요시 사용 예정 (2025.09.05 minjae)
        # elif (chatbot_helper._accountType in userRequest_msg):  # end - 텍스트 + basicCard 계정 & 제품배정 
        #     if chatbot_helper._anyQuestion in userRequest_msg:   # '기타 문의' 
        #         resFormat, master_data = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._accountInfos][chatbot_helper._anyQuestion])

        #     elif chatbot_helper._resetPassword in userRequest_msg:   # '계정 비밀번호 분실'
        #         resFormat, master_data = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._accountInfos][chatbot_helper._resetPassword])

        #     else:   # [구현 예정!] '기타 문의', '계정 비밀번호 분실' 제외한 다른 문의 
        #         resFormat, master_data = end_basicCard(master_datas[chatbot_helper._endCard], master_datas[chatbot_helper._endCard][chatbot_helper._etcInfos][chatbot_helper._etcTest])

        chatbot_logger.log_write(chatbot_logger._info, '[테스트] 카카오 json 포맷 가져오기', 'OK!')   
        return resFormat, master_data 
        
    except Exception as e:     
        error_msg = str(e)     
        chatbot_logger.log_write(chatbot_logger._error, "[테스트] 오류", error_msg) 
        raise       

# level1 케로셀 (카카오톡 서버로 기본 카드 전송)
# 챗봇 문의 기본형 카드
def chatbot_carousel(chatbotCard):
    chatbotButtons = []
     
    for chatbotButton in chatbotCard[chatbot_helper._buttons]:   # 챗봇 문의 3가지 버튼 텍스트 및 메세지 추가
        chatbotButtons.append({
            "action": "message",
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
                "title": chatbotCard[chatbot_helper._items][chatbot_helper._chatbotItem_Idx][chatbot_helper._title],
                "description": chatbotCard[chatbot_helper._items][chatbot_helper._chatbotItem_Idx][chatbot_helper._description]
            }
        ],
        "itemListAlignment" : "left",
        "buttons": chatbotButtons,
        "buttonLayout" : "vertical"
    })

    return carousel_json(chatbotCard, chatbot_items), chatbotCard

# level2 기본형 카드 (카카오톡 서버로 기본 카드 전송)
# 상담유형 안내
def subCat_basicCard(userRequest_msg, subCatCard):
    subCatButtons = []
     
    for subCatButton in subCatCard[chatbot_helper._buttons]:   # 상담유형 안내 버튼 텍스트 및 메세지 추가
        messageText = None   # 변수 (messageText) 초기화

        # 변수(subCatButton[chatbot_helper._label])에 저장된 값이 '설치 문의' and 변수(userRequest_msg)에 저장된 값이 'Autodesk 제품' 또는 '상상진화 BOX 제품'인 경우 
        if (chatbot_helper._askInst == subCatButton[chatbot_helper._label] and chatbot_helper._accountProduct != userRequest_msg):
            messageText = f"{userRequest_msg} {subCatButton[chatbot_helper._messageText]}"

        # 변수(subCatButton[chatbot_helper._label])에 저장된 값이 '계정 & 제품배정 문의'인 경우 and 변수(userRequest_msg)에 저장된 값이 '계정 & 제품배정'인 경우 
        elif (chatbot_helper._ask_accountProduct == subCatButton[chatbot_helper._label] and chatbot_helper._accountProduct == userRequest_msg):
            # messageText = f"{userRequest_msg} {chatbot_helper._ask}"
            messageText = subCatButton[chatbot_helper._messageText]

        # 위 2가지 조건에 해당되지 않는 경우 
        if None is messageText: continue   # continue 처리

        subCatButtons.append({
            "action": "message",
            "label": subCatButton[chatbot_helper._label],
            "messageText": messageText
        })

    return basicCard_json(subCatCard, subCatButtons), subCatCard

# TODO: 아래 주석친 코드 필요시 사용 예정 (2025.09.17 minjae)
# level5 텍스트 카드 (카카오톡 서버로 텍스트 전송)
# Autodesk 제품 설치 언어
# def adskLang_textCard(userRequest_msg, adskLangCard):
#     adskLangButtons = []
     
#     for adskLangButton in adskLangCard[chatbot_helper._buttons]:   # Autodesk 제품 설치 언어 버튼 텍스트 및 메세지 추가
#         adskLangButtons.append({
#             "action": "message",
#             "label": adskLangButton[chatbot_helper._label],
#             "messageText": f"{userRequest_msg} {adskLangButton[chatbot_helper._messageText]}"
#         })

#     return textCard_json(adskLangCard, adskLangButtons), adskLangCard

# TODO: 아래 주석친 코드 필요시 사용 예정 (2025.09.17 minjae)
# level3 바로가기 그룹 (카카오톡 서버로 바로가기 그룹 전송)
# 계정 & 제품배정 문의
# def account_quickReplies(accountReplies):
#     accountQuickReplies = []
     
#     for accountButton in accountReplies[chatbot_helper._buttons]:   # 계정 & 제품배정 문의 버튼 텍스트 및 메세지 추가   
#         messageText = f"{chatbot_helper._accountType} {accountButton[chatbot_helper._messageText]}"
#         accountQuickReplies.append({
#             "action": "message",
#             "label": accountButton[chatbot_helper._label],
#             "messageText": messageText
#         })

#     return quickReplies_json(accountReplies, accountQuickReplies), accountReplies

# TODO: 아래 함수 end_basicCard 필요시 로직 수정 예정 (2025.09.05 minjae)
# end 기본형 카드 (카카오톡 서버로 기본 카드 전송)
# 마지막화면 안내
def end_basicCard(endCard, endInfos):
    endButtons = []
    outputs = []

    # TODO: 오류 메시지 "string indices must be integers, not 'str'" 출력되어 아래처럼 코드 변경 처리함. (2025.08.28 minjae)
    # (기존) endCard -> (변경) endCard[chatbot_helper._buttons]  
    for endButton in endCard[chatbot_helper._buttons]:   # 처음으로, 동영상, 만족도 조사 버튼 텍스트 및 메세지 추가
        if (chatbot_helper._video == endButton[chatbot_helper._label] 
            and chatbot_helper._yes == endInfos[chatbot_helper._webLinkUrl_Idx][chatbot_helper._videoYn]):   # 버튼이 '동영상'이고 동영상 시청 가능할 경우 ("videoYn": "Y")
            endButtons.append({
                "action": "webLink",
                "label": endButton[chatbot_helper._label],
                "webLinkUrl": endInfos[chatbot_helper._webLinkUrl_Idx][chatbot_helper._webLinkUrl]
            })
        else:   # 동영상 시청이 불가능 ("videoYn": "N") 하거나 버튼이 "동영상" 아닐 경우 
            endButtons.append({
                "action": "message",
                "label": endButton[chatbot_helper._label],
                "messageText": endButton[chatbot_helper._messageText]
            })

    if endInfos[chatbot_helper._botRes_Idx][chatbot_helper._botRes]:   # endInfos[chatbot_helper._botRes_Idx][chatbot_helper._botRes]에 할당된 값이 null 또는 공백("")이 아닌 경우 (None or Empty String Check)
        outputs.append({
            "simpleText": {
                "text": endInfos[chatbot_helper._botRes_Idx][chatbot_helper._botRes]
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

    return outputs_json(outputs), endCard