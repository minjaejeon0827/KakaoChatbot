"""
* 챗봇 전용 도움말 텍스트 
"""

# region 공통 

_datefmt='%Y-%m-%d %H:%M:%S'   # 로그 기록 형식 (년-월-일 시:분:초)

# 오류 안내 메시지 (raise Exception)
_error_title = '[테스트] [오류 안내]'
_error_techSupport = '상상진화 기술지원 콜센터 02-3474-2263\n연락 부탁드립니다.'

# endregion 공통 

# region lambda_function.py

# handler 함수 -> event['body'] - 카카오톡 채팅방 채팅 정보 할당된 변수 의미.
_body = 'body'   # 키 'body'
_action = 'action'   # 키 'action'

# ***** 아마존 웹서비스 람다 함수 (AWS Lambda Function) *****
# 콜드 스타트 (coldstart) - 초기 응답 속도 느림 (coldstart) 현상 의미
# 아마존 웹서비스 람다 함수 (AWS Lambda Function)가 처음 호출되거나 오랜 시간 동안 호출되지 않다가 다시 호출될 때 발생하는 초기화 과정 의미. (container-warmup)
# 아마존 웹서비스 Amazon EventBridge -> 항목 "Scheduler" -> 항목 "일정" -> 일정 이름 "test_kakao_health-check" 클릭 -> "test_kakao_health-check" 화면 이동 -> 탭 "대상" 클릭시
# 아래와 같은 json 페이로드 형식이 구현됨. 
# json 페이로드 형식
# {
#   "body": "{ \"action\": \"aws-lambda_function-container-warmup\" }"
# }
# _cold_start = 'aws-lambda_function-container-warmup'
_warmup_request = 'aws-lambda_function-container-warmup'
_tmp = '/tmp/'                          # 임시 로그 텍스트 파일 상위 폴더
_chatbot_file_name = 'chatbot.txt'     # 임시 로그 텍스트 파일 이름
# _botlog_file_path = '/tmp/botlog.txt'   # 테스트용 임시 로그 텍스트 파일 상대 경로 ('/tmp/botlog.txt') 
_time_limit = 3.5   # 챗봇 응답 가능 제한 시간

# 큐(res_queue) 폴링(polling) 간격 변수명 짓기
# 참고 URL - https://claude.ai/chat/f1d34ae8-3e62-4919-92c6-c94277481c76
_polling_interval = 0.01   # 큐(res_queue) 폴링(polling) 간격
_done_thinking = '생각 다 끝났나요?'   # 챗봇 응답 시간 5초 초과한 경우 챗봇 응답 메시지 
_statusCode_success = 200      # HTTP 응답 상태 코드 성공 
_userRequest = 'userRequest'   # 사용자 -> 챗봇 질문 요청
_user = 'user'                 # 카카오톡 채팅 입력 사용자 정보
_id = 'id'                     # 카카오톡 채팅 입력 사용자 아이디
_utterance = 'utterance'       # 사용자가 카카오 채팅방에 입력한 문자열

# 챗봇 응답 시간 5초 초과시 응답 재요청 기능 구현 
# 참고 URL - https://claude.ai/chat/d550ac84-5c0c-4805-a600-9fdfd1236714
# _multiWord = 2  # 공백('')단위로 분리한 단어들의 개수 2개 이상인 경우 
# _firstWord_Idx = 0   # 공백('')단위로 분리한 첫 번째 단어(last_update.split()[0]) 인덱스 
# _secondWord_Idx = 1   # 공백('')단위로 분리한 두 번째 단어(last_update.split()[1]) 인덱스 
# _thirdWord_Idx = 2   # 공백('')단위로 분리한 세 번째 단어(last_update.split()[2]) 인덱스 
# _askPrefix_Len = 4   # 접두사 길이 (공백 포함) (예) "ask "

_masterEntity_json_file_path = './resources/json/masterEntity.json'   # 전체 마스터 데이터 json 파일 상대 경로

# endregion lambda_function.py  

# region kakao.py

# 카카오 응답 데이터 
_payload = 'payload'         # 카카오톡 서버로 전송할 json 포맷 기반 챗봇 답변 내용 (페이로드)
_meta_data = 'meta_data'   # 다른 데이터 설명해 주는 데이터 (예) master_data - 특정 마스터 데이터

# 필드명 "action" - 버튼 클릭시 수행될 작업
_action = 'action'     # 실행되는 스킬의 정보를 담고있는 필드 ('webLink' or 'message')
_webLink = 'webLink'   # 웹 브라우저 열고 webLinkUrl 주소 이동
_message = 'message'   # 사용자의 발화로 messageText 실행. (바로가기 응답의 메세지 연결 기능과 동일)

# 기술지원 업무 프로세스
_inst = '설치'
_ask = '문의'
_support = '지원'
# _askInst = f'{_inst} {_ask}'
_instSupport = f'{_inst} {_support}'

_product = '제품'
_adskProduct = f'Autodesk {_product}'
_boxProduct = f'상상진화 BOX {_product}'
_accountProduct = f'계정 & {_product}배정'
_ask_accountProduct = f'{_accountProduct} {_ask}'

_checkRequest = '요청사항 확인 중이에요.\n잠시후 아래 말풍선을 눌러주세요.'   # 시간 5초 초과시 응답 (바로가기 그룹 전송)

# start 
_start = '/start'   # 시작 화면

# level1 
_remote_text = '아래 링크를 클릭하시면 원격 지원 프로그램 다운로드 시작됩니다.\nhttps://113366.com/client/download?relayUri=imbu\n\n프로그램 다운로드 완료 후\n상상진화 기술지원 콜센터 02-3474-2263\n연락 부탁드립니다.'   # 원격 지원
_ask_chatbot = f'챗봇 {_ask}'   # 챗봇 문의
# _chatbotItem_Idx = 0   # [챗봇 문의] itemList "title", "description"

# level2
_instSupport_adskProduct = f'{_adskProduct} {_instSupport}'   # Autodesk 제품 설치 지원
_instSupport_boxProduct = f'{_boxProduct} {_instSupport}'   # 상상진화 BOX 제품 설치 지원
# _ask_accountProduct = f'{_accountProduct} {_ask}'   # 계정 & 제품배정 문의

# TODO: level3 필요시 구현 예정 (2025.09.05 minjae)
# level3 - Autodesk 제품 버전 
# Language Pack 존재
# Language Pack 존재 X

# end - 마지막 화면

# 버튼 Label + messageText 
_beginning = '처음으로'
_video = '동영상'   
_survey = '만족도 조사'  

# 버튼 인덱스 번호
# _videoButton_Idx = 1   # 버튼 "동영상" (masterEntity.json -> "endCard" dict -> "buttons" list 객체 인덱스 번호)  
# _webLinkUrl_Idx = 0   # 버튼 "동영상"과 연동할 webLinkUrl 인덱스 번호 (masterEntity.json -> "endCard" dict -> "autoCADInfos", "revitInfos", "navisworksManageInfos", "infraWorksInfos", "civil3DInfos", "revitBoxInfos", "cadBoxInfos", "energyBoxInfos", "accountInfos" list 객체 인덱스 번호)
# _text_Idx = 0   # Autodesk, 상상진화 Box 제품별 챗봇 응답 내용 인덱스 번호

# 동영상 시청 
_yes = 'Y'   # 가능 
_no = 'N'   # 불가능
_version = 'version'   # 버전
_videoYn = 'videoYn'   # 가능 여부 

# 기술지원 유형 
_instType = 'Inst -'   # 설치 

# CASE 1: Autodesk 제품
# _adskType = 'Autodesk -'
_autoCAD = 'AutoCAD'
_revit = 'Revit'
_navisworksManage = 'Navisworks Manage'
# Navisworks Simulate 제품 판매 불가(제품 재고 X)인 관계로 설치지원 제품 'InfraWorks' 대체 (2025.08.21 minjae)
# _navisworks_Simulate = 'Navisworks Simulate'
_infraWorks = 'InfraWorks'
_civil3D = 'Civil3D'

# CASE 2: 상상진화 BOX 제품
# _boxType = 'BOX -' 
_revitBox = 'RevitBOX'
_cadBox = 'CADBOX'
_energyBox = 'EnergyBOX'

# TODO: CASE 3 필요시 구현 예정 (2025.09.05 minjae)
# CASE 3: 계정 & 제품배정
# _accountType = 'Account -' 
# _anyQuestion = 'anyQuestion'
# _resetPassword = 'resetPassword'
# _etcTest = 'etcTest'

# endregion kakao.py

# region masterEntity.json

# json 데이터 파싱(parsing) 용도 
_masterEntity = 'masterEntity'   # 전체 마스터 데이터 (masterEntity.json) 파일 객체 

# 공통 - 카드 or 바로가기 그룹 객체 안에 속한 키 (key)
_levelNo = 'levelNo'
_displayName = 'displayName'
_text = 'text'
_title = 'title'
_description = 'description'
_thumbnail = 'thumbnail'
_imageUrl = 'imageUrl'
_buttons = 'buttons'
_quickReplies = 'quickReplies'
_label = 'label'
_messageText = 'messageText'
_webLinkUrl = 'webLinkUrl'
_itemList = 'itemList'

# 바로가기 그룹 이름 (quickReplies Name)
_adskReplies = 'adskReplies'
_adskVerReplies = 'adskVerReplies'
_boxReplies = 'boxReplies'
_boxVerReplies = 'boxVerReplies'
# _accountReplies = 'accountReplies'

# 카드 이름 (card Name)
_startCard = 'startCard'
_chatbotCard = 'chatbotCard'
_endCard = 'endCard'
_surveyCard = 'surveyCard'

# 기술지원 문의 제외 일반 문의
_emptyResponse = 'emptyResponse'

# 카드 객체 (endCard) 안에 속한 메타 데이터 키 (key) 
# 메타 데이터 
# 참고 URL - https://ko.wikipedia.org/wiki/%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0#cite_note-1
# 참고 2 URL - https://terms.tta.or.kr/dict/dictionaryView.do?subject=%EB%A9%94%ED%83%80+%EB%8D%B0%EC%9D%B4%ED%84%B0
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

# endregion masterEntity.json

# region 참고

# 파이썬 절대 경로와 상대 경로
# 참고 URL - https://wikidocs.net/153154

# Autodesk 제품 설치 방법 TEXT 파일 경로 
# _autoCAD_2025_2026_file_path = './resources/text/adsk/autoCAD_2025_2026_Installation_Guide.txt'
# _revit_2025_2026_file_path = './resources/text/adsk/revit_2025_2026_Installation_Guide.txt'
# _navisworksManage_2025_2026_file_path = './resources/text/adsk/navisworksManage_2025_2026_Installation_Guide.txt'
# _infraworks_2025_2026_file_path = './resources/text/adsk/infraworks_2025_2026_Installation_Guide.txt'
# _civil3D_2025_2026_file_path = './resources/text/adsk/civil3D_2025_2026_Installation_Guide.txt'

# BOX 제품 설치 방법 TEXT 파일 경로
# _revitBox_2022_2026_file_path = './resources/text/box/revitBox_2022_2026_Installation_Guide.txt'
# _cadBox_2022_2026_file_path = './resources/text/box/cadBox_2022_2026_Installation_Guide.txt'
# _energyBox_2022_2026_file_path = './resources/text/box/energyBox_2022_2026_Installation_Guide.txt'

# endregion 참고