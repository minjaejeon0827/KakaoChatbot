# TODO: 공통 필요시 구현 예정 (2025.09.05 minjae)
# ------------------   공통  -------------------
# 
# ---------------------------------------------- 

# -----   카카오 챗봇 (lambda_function.py)  -----

# TODO: 필요시 변수 _event_body_key 사용 예정 (2025.09.05 minjae)
# _event_body_key = 'body'   # # lambda_function.py -> handler 함수 -> event['body'] 키값

# coldStart(콜드 스타트)
# coldStart는 아마존 웹서비스(AWS) 람다 함수(Lambda Function)가 처음 호출되거나 오랜 시간 동안 호출되지 않다가 다시 호출될 때 발생하는 초기화 과정(container-WarmUp)이다.
# json 페이로드 형식
# {
#   "body": "{ \"action\": \"aws-lambda_function-container-WarmUp\" }"
# }
_coldStart = 'aws-lambda_function-container-WarmUp' 
_botlog_file_path = '/tmp/botlog.txt'   # 아마존 웹서비스(AWS) 람다 함수(Lambda Function) -> 로그 텍스트 파일("/tmp/botlog.txt") 경로
_timeLimit = 3.5   # 카카오 챗봇 답변 가능 제한 시간

# TODO: 큐(res_queue) 폴링(polling) 간격 변수명 짓기 (2025.08.20 minjae)
# 참고 URL - https://claude.ai/chat/f1d34ae8-3e62-4919-92c6-c94277481c76
_pollingInterval = 0.01   # 큐(res_queue) 폴링(polling) 간격
_doneThinking = '생각 다 끝났나요?'   # 시간 5초 초과한 경우 카카오 챗봇 응답 메시지 
_masterEntity_json_filepath = './resources/json/masterEntity.json'   # 마스터 데이터 json 파일 경로

# -----      카카오 전용 모듈 (kakao.py)     -----

# 기술지원 업무 프로세스
_inst = '설치'
_ask = '문의'
_askInst = f'{_inst} {_ask}'

_product = '제품'
_autodeskProduct = f'Autodesk {_product}'
_boxProduct = f'상상진화 BOX {_product}'
_accountProduct = f'계정 & {_product}배정'
_askAccountProduct = f'{_accountProduct} {_ask}'
# _consult = '상담'
# _consultChatting = f'채팅 {_consult}' 

_checkingRequest = '요청사항 확인 중이에요.\n잠시후 아래 말풍선을 눌러주세요.'   # 시간 5초 초과시 응답 (바로가기 그룹 전송)

# start 
_start = '/start'   # 시작 화면

# level1 
_remote_botRes = '아래 링크를 클릭하시면 원격 지원이 시작됩니다.\nhttps://113366.com/client/download?relayUri=imbu'   # 원격 지원
_chatbot = f'챗봇 {_ask}'   # 챗봇 문의
_chatbotItem_Idx = 0   # [챗봇 문의] itemList 'title', 'description'

# TODO: level2 필요시 구현 예정 (2025.09.05 minjae)
# level2 - 문의 유형 

# level3 
_askInst_autodeskProduct = f'{_autodeskProduct} {_askInst}' # Autodesk 제품 설치 문의
_askInst_boxProduct = f'{_boxProduct} {_askInst}'   # 상상진화 BOX 제품 설치 문의
# _ask_accountProduct = f'{_accountProduct} {_ask}'   # 계정 & 제품배정 문의 

# TODO: level4 필요시 구현 예정 (2025.09.05 minjae)
# level4 
# - Autodesk 제품 버전 Language Pack
# - Autodesk 제품 버전

# TODO: level5 필요시 추가 구현 예정 (2025.09.05 minjae)
# level5 - Autodesk 제품 설치 언어
# _langPack = 'Language Pack'
# _instMethod = f'{_inst} 방법'

# end - 마지막 화면

# 버튼 Label + messageText 
_beginning = '처음으로'
_video = '동영상'   
_survey = '만족도 조사'  

# 버튼 인덱스 번호
_videoButton_Idx = 1   # [마지막 화면] 버튼 "동영상" (masterEntity.json -> "endCard" Dictionary -> "buttons" list 객체 인덱스 번호)  
_webLinkUrl_Idx = 0   # [마지막 화면] 버튼 "동영상"과 연동할 webLinkUrl 인덱스 번호 (masterEntity.json -> "endCard" Dictionary -> "autoCADInfos", "revitInfos", "navisworksManageInfos", "infraWorksInfos", "civil3DInfos", "revitBoxInfos", "cadBoxInfos", "energyBoxInfos", "accountInfos" list 객체 인덱스 번호
_botRes_Idx = 0   # [마지막 화면] Autodesk, Box 제품별 카카오 챗봇 답변 내용 인덱스 번호

# 기술지원 유형 
_instType = 'Inst -'   # 설치 

# CASE 1: Autodesk 제품
# _adskType = 'Autodesk -'
_autoCAD = 'AutoCAD'
_revit = 'Revit'
_navisworksManage = 'Navisworks Manage'
# TODO: Navisworks Simulate 제품 판매 불가(제품 재고 X)인 관계로 설치지원 제품을 'InfraWorks'로 대체함. (2025.08.21 minjae)
# _navisworks_Simulate = 'Navisworks Simulate'
_civil3D = 'Civil3D'
_infraWorks = 'InfraWorks'

# CASE 2: 상상진화 BOX 제품
# _boxType = 'BOX -' 
_revitBox = 'RevitBOX'
_cadBox = 'CADBOX'
_energyBox = 'EnergyBOX'

# TODO: CASE 3 필요시 구현 예정 (2025.09.05 minjae)
# CASE 3: 계정 & 제품배정
# _accountType = 'Account -' 


# ----------------------------------------------

# ----- 마스터 데이터(masterEntity.json) 파일 -----
# json 데이터 파싱(parsing) 용도 사용 

# 공통 - 카드 or 바로가기 그룹 객체 안에 속한 키(key)
_levelNo = 'levelNo'
_displayName = 'displayName'
_botRes = 'botRes'
_title = 'title'
_description = 'description'
_thumbnail = 'thumbnail'
_imageUrl = 'imageUrl'
_buttons = 'buttons'
_label = 'label'
_messageText = 'messageText'
_webLinkUrl = 'webLinkUrl'

# 바로가기 그룹 이름 (quickReplies Name)
_adskReplies = 'adskReplies'
# _adskVerPackReplies = 'adskVerPackReplies'
_adskVerReplies = 'adskVerReplies'
_boxReplies = 'boxReplies'
_boxVerReplies = 'boxVerReplies'
_accountReplies = 'accountReplies'

# 카드 이름 (card Name)
_startCard = 'startCard'
_chatbotCard = 'chatbotCard'
_subCatCard = 'subCatCard'
# _adskLangCard = 'adskLangCard'
_endCard = 'endCard'
_surveyCard = 'surveyCard'

# 카드 객체(endCard) 안에 속한 메타 데이터 키(key) 
# 메타 데이터 
# 참고 URL - https://ko.wikipedia.org/wiki/%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0#cite_note-1
# 참고 2 URL - https://terms.tta.or.kr/dictionary/dictionaryView.do?subject=%EB%A9%94%ED%83%80+%EB%8D%B0%EC%9D%B4%ED%84%B0
# 참고 3 URL - https://claude.ai/chat/99872ec0-7105-4e08-8107-fab2d351e7bb
_autoCADInfos = 'autoCADInfos'
_revitInfos = 'revitInfos'
_navisworksManageInfos = 'navisworksManageInfos'
_infraWorksInfos = 'infraWorksInfos'
_civil3DInfos = 'civil3DInfos'
_revitBoxInfos = 'revitBoxInfos'
_cadBoxInfos = 'cadBoxInfos'
_energyBoxInfos = 'energyBoxInfos' 
_accountInfos = 'accountInfos'
_etcInfos = 'etcInfos'


# ----------------------------------------------

# -------------------- 참고 --------------------

# 파이썬 절대 경로와 상대 경로
# 참고 URL - https://wikidocs.net/153154

# Autodesk 제품 설치 방법 TEXT 파일 경로 
# _autoCAD_2025_2026_filepath = './resources/text/adsk/autoCAD_2025_2026_Installation_Guide.txt'
# _revit_2025_2026_filepath = './resources/text/adsk/revit_2025_2026_Installation_Guide.txt'
# _navisworksManage_2025_2026_filepath = './resources/text/adsk/navisworksManage_2025_2026_Installation_Guide.txt'
# _infraworks_2025_2026_filepath = './resources/text/adsk/infraworks_2025_2026_Installation_Guide.txt'
# _civil3D_2025_2026_filepath = './resources/text/adsk/civil3D_2025_2026_Installation_Guide.txt'

# BOX 제품 설치 방법 TEXT 파일 경로
# _revitBox_2022_2026_filepath = './resources/text/box/revitBox_2022_2026_Installation_Guide.txt'
# _cadBox_2022_2026_filepath = './resources/text/box/cadBox_2022_2026_Installation_Guide.txt'
# _energyBox_2022_2026_filepath = './resources/text/box/energyBox_2022_2026_Installation_Guide.txt'

# ----------------------------------------------  