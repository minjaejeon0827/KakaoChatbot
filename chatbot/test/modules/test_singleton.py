# 싱글톤(singleton) 패턴 전용 모듈

# * 파이썬 클래스(class), 메서드(method), 함수(function) Docstring - 문서화 작성 예시 
# 참고 URL - https://peps.python.org/pep-0257/
# 참고 2 URL - https://wikidocs.net/16050
# 참고 3 URL - https://soma0sd.tistory.com/130
# 참고 4 URL - https://spirit0833.tistory.com/3
# 참고 5 URL - https://m.blog.naver.com/withnicebambi/223553537062

import asyncio   # 비동기 프로그래밍(async - await) 전용 모듈
import logging  # 로그 작성 전용 모듈 

from utils import chatbot_logger               # 폴더 "modules" -> 챗봇 로그 작성 모듈 
from commons import chatbot_helper       # 폴더 "commons" -> 챗봇 전용 도움말 텍스트 
from restAPI import chatbot_restServer   # 폴더 "restAPI" -> 챗봇 웹서버 Rest API 메서드 

from datetime import datetime 
from zoneinfo import ZoneInfo  # 로그 출력시 대한민국 표준시로 출력하기 위해 패키지 "zoneinfo" 불러오기 

from enum import Enum   # Enum 열거형 구조체 사용하기 위해 패키지 "enum"  

# 데이터 유효성 검사 Enum 열거형 구조체 클래스 
# 참고 URL - https://docs.python.org/ko/3.9/library/enum.html#functional-api
# 참고 2 URL - https://wikidocs.net/105486
class EnumValidator(Enum):
    NOT_EXISTENCE = 0   # 데이터 존재 안 함.
    EXISTENCE = 1   # 데이터 존재함.

# 챗봇 마스터 데이터 싱글톤(singleton) 클래스 
# 마스터 데이터 - SW 프로그램을 실행하기 위해 사용되는 기준 데이터 의미. (특정 기업의 업무지식 및 비즈니스 운영의 핵심 정보 반영 필수!) 
# 참고 URL - https://en.wikipedia.org/wiki/Master_data
# 참고 2 URL - https://wiki1.kr/index.php/%EB%A7%88%EC%8A%A4%ED%84%B0%EB%8D%B0%EC%9D%B4%ED%84%B0#cite_note-masterdata_synopsis-2
# 참고 3 URL - https://claude.ai/chat/5a7fdfc5-6cb8-4286-bb10-a3082e164934
# __new__ 메서드는 클래스(MasterEntity)에 정의되어 있지 않으면 알아서 부모 클래스(object)의 __new__ 메서드가 호출되어 객체 생성
# 클래스(MasterEntity) 정의할 때 __new__ 메서드를 사용자가 작성할 수도 있는데 이 경우 부모 클래스(object)의 __new__ 메서드가 아니라 
# 클래스(MasterEntity)에 정의된 __new__ 메서드가 호출되는데 이를 오버라이드(override) 했다고 표현
# 생성된 객체에 속성(property) 추가할 때 __init__ 메서드 호출
class MasterEntity(object):
    def __new__(_class, *args, **kwargs):      # MasterEntity 클래스에서 재 정의된 __new__ 메서드이며, 매개변수 _class의 경우 여기서는 MasterEntity 클래스 의미함.
        if not hasattr(_class, "_instance"):   # 해당 클래스에 _instance 속성(property - 객체)이 없다면
            chatbot_logger.log_write(chatbot_logger._info, '[테스트] MasterEntity __new__ 메서드', 'Called!')
            _class._instance = super().__new__(_class)  
        return _class._instance                   

    def __init__(self, valid_targets):  # 객체 생성 시 전달된 모든 인자(valid_targets는 제외)를 __new__ 메서드가 먼저 받고, 그 다음 __init__ 메서드로 전달
        _class = type(self)
        if not hasattr(_class, "_init"):   # 해당 클래스에 _init 속성(property)이 없다면
            chatbot_logger.log_write(chatbot_logger._info, '[테스트] MasterEntity __init__ 메서드', 'Called!') 

            asyncio.run(self.initSettingAsync(valid_targets))   # 이벤트 루프(asyncio.run) 실행하여 비동기 메서드 self.initSettingAsync(valid_targets) 호출                
                  
            _class._init = True   # 초기화 완료  

    @property
    def get_master_datas(self):   
        return self.__master_datas

    # TODO: setter 메서드 set_master_datas 필요시 사용 예정 (2025.09.15 minjae)
    # @get_master_datas.setter
    # def set_master_datas(self, master_datas):   
    #     self.__master_datas = master_datas

    @property
    def get_chatbot_messageTexts(self):
        return self.__chatbot_messageTexts

    # TODO: setter 메서드 set_chatbot_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_chatbot_messageTexts.setter
    # def set_chatbot_messageTexts(self, chatbot_messageTexts):
    #     self.__chatbot_messageTexts = chatbot_messageTexts

    @property
    def get_adsk_messageTexts(self):
        return self.__adsk_messageTexts

    # TODO: setter 메서드 set_adsk_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_adsk_messageTexts.setter
    # def set_adsk_messageTexts(self, adsk_messageTexts):
    #     self.__adsk_messageTexts = adsk_messageTexts

    @property
    def get_box_messageTexts(self):
        return self.__box_messageTexts

    # TODO: setter 메서드 set_box_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_box_messageTexts.setter
    # def set_box_messageTexts(self, box_messageTexts):
    #     self.__box_messageTexts = box_messageTexts


    @property
    def get_isValid(self):   
        return self.__isValid

    # TODO: setter 메서드 set_isValid 필요시 사용 예정 (2025.09.15 minjae)
    # @get_isValid.setter
    # def set_isValid(self, isValid):  
    #     self.__isValid = isValid

    @property
    def get_valid_targets(self):   
        return self.__valid_targets

    # TODO: setter 메서드 set_valid_targets 필요시 사용 예정 (2025.09.15 minjae)
    # @get_valid_targets.setter
    # def set_valid_targets(self, valid_targets):   
    #     self.__valid_targets = valid_targets

    # 마스터 데이터 초기 셋팅
    async def initSettingAsync(self, valid_targets):

        try:
            chatbot_logger.log_write(chatbot_logger._info, '[테스트] 마스터 데이터 초기 셋팅', 'Start!')

            self.__master_datas = await chatbot_restServer.getMasterDownLoadAsync(chatbot_helper._masterEntity_json_file_path)   # 마스터 데이터 다운로드  
            # TODO: 리스트 컴프리헨션 문법 사용하여 "buttons" 리스트 객체(master_datas[chatbot_helper._chatbotCard][chatbot_helper._buttons])에 속한 
            #       키(key) 'messageText'에 할당된 값(button[chatbot_helper._messageText])만 추출하여 리스트 객체([button[chatbot_helper._messageText] for button in master_datas[chatbot_helper._chatbotCard][chatbot_helper._buttons]])로 변환 처리 (2025.08.25 minjae) 
            # 참고 URL - https://docs.python.org/ko/3.13/tutorial/datastructures.html#list-comprehensions
            # 참고 2 URL - https://claude.ai/chat/a6e38078-6a1f-4c67-a1f2-442f04d86938
            self.__chatbot_messageTexts = [ chatbotButton[chatbot_helper._messageText] for chatbotButton in self.__master_datas[chatbot_helper._chatbotCard][chatbot_helper._buttons] ]   # [챗봇 문의] 버튼 메시지 텍스트 리스트  
            self.__adsk_messageTexts = [ adskButton[chatbot_helper._messageText] for adskButton in self.__master_datas[chatbot_helper._adskReplies][chatbot_helper._buttons] ]   # [Autodesk 제품 설치 문의] 버튼 메시지 텍스트 리스트 
            self.__box_messageTexts = [ boxButton[chatbot_helper._messageText] for boxButton in self.__master_datas[chatbot_helper._boxReplies][chatbot_helper._buttons] ]   # [상상진화 BOX 제품 설치 문의] 버튼 메시지 텍스트 리스트
            self.__valid_targets = valid_targets      
            self.__isValid = self.isValidator()     

            chatbot_logger.log_write(chatbot_logger._info, '[테스트] 마스터 데이터 초기 셋팅 결과', 'OK!') 
        
        except Exception as e:     
            error_msg = str(e)     
            chatbot_logger.log_write(chatbot_logger._error, "[테스트] 오류", error_msg)     

    # TODO: 추후 필요시 마스터 데이터 유효성 검사 메서드 isValidator 로직 수정 예정 (2025.09.02 minjae)
    # 웹서버로 부터 받아온 마스터 데이터 유효성 검사
    # 참고 URL - https://chatgpt.com/c/68017acc-672c-8010-8649-7fa39f17d834
    def isValidator(self):
        # master_datas = None   # 전체 마스터 데이터 (Dictionary) 
        master_datas = self.get_master_datas     # 전체 마스터 데이터 (Dictionary) 
        valid_targets = self.get_valid_targets   # 마스터 데이터 유효성 검사 대상 리스트

        try:
            chatbot_logger.log_write(chatbot_logger._info, '[테스트] 마스터 데이터 유효성 검사 대상 리스트', valid_targets)
            chatbot_logger.log_write(chatbot_logger._info, '[테스트] 마스터 데이터 유효성 검사', 'Start!')

            if None is master_datas:   # 전체 마스터 데이터 (Dictionary)가 None일 경우 
                raise Exception("마스터 데이터 로드 실패!")

            # TODO: Dictionary 객체 master_datas를 for문으로 루핑하기 위해 items() 메서드 사용 구현 (2025.09.02 minjae)
            # 참고 URL - https://docs.python.org/ko/3.13/tutorial/datastructures.html#looping-techniques 
            for parent_key, parent_value in master_datas.items():
                # logger.log_write(logger._info, '[테스트] master_datas', f'key: {key} / value: {value}')
                master_data = parent_value
                for child_key, child_value in master_data.items():
                    if child_key in valid_targets:   # 유효성 검사 대상 키들만 확인
                        chatbot_logger.log_write(chatbot_logger._info, '[테스트] master_data', f'key: {child_key} / value: {child_value}')
                        # 파이썬 함수 len 사용하여 문자열, 리스트 객체 길이 구하기
                        # 참고 URL - https://wikidocs.net/215513            
                        if (None is child_value or EnumValidator.NOT_EXISTENCE.value >= len(child_value)):   # child_value 값이 존재하지 않거나(None) 길이가 0보다 작거나 같은 경우 
                            chatbot_logger.log_write(chatbot_logger._error, '[테스트] 마스터 데이터 유효성 검사 결과', 'Fail!')
                            return False   # 마스터 데이터 유효성 검사 오류 

            chatbot_logger.log_write(chatbot_logger._info, '[테스트] 마스터 데이터 유효성 검사 결과', 'OK!')
            return True   # 마스터 데이터 유효성 검사 성공 
        
        except Exception as e:     
            error_msg = str(e)     
            chatbot_logger.log_write(chatbot_logger._error, "[테스트] 오류", error_msg)     
            return False   # 마스터 데이터 유효성 검사 오류 
                

# 로그 기록 시 대한민국 시간대 설정을 위한 사용자 정의 Formatter 싱글톤(singleton) 클래스 (pytz 라이브러리 사용 안 함.)
# 참고 URL - https://claude.ai/chat/8fc1ceeb-fe95-4d1b-8517-ecec83beb3f2
class KSTFormatter(logging.Formatter):
    # TODO: 아마존 웹서비스 람다 함수(AWS Lambda function) 환경에서는 단일 스레드(single thread)로 실행되므로 아래 주석친 코드(_lock = threading.Lock()) 사용할 필요 없음. (2025.09.18 minjae)
    # _lock = threading.Lock()   # _lock = threading.Lock() 용도 - 일반적인 Python 응용 프로그램 환경에서 여러 스레드가 동시에 싱글톤을 생성하려 할 때 또는 Race condition으로 인해 여러 인스턴스가 생성될 가능성이 있을 때 사용한다.

    def __new__(_class, *args, **kwargs):      # KSTFormatter 클래스에서 재 정의된 __new__ 메서드이며, 매개변수 _class의 경우 여기서는 KSTFormatter 클래스 의미함.
        if not hasattr(_class, "_instance"):   # 해당 클래스에 _instance 속성(property - 객체)이 없다면 
            ----- print("[%s] %s" %("Chatbot", "[테스트] KSTFormatter __new__ 메서드: Called!"))
            _class._instance = super().__new__(_class)  
        return _class._instance                         

    def __init__(self, *args, **kwargs):  # 객체 생성 시 전달된 모든 인자를 __new__ 메서드가 먼저 받고, 그 다음 __init__ 메서드로 전달
        _class = type(self)
        if not hasattr(_class, "_init"):   # 해당 클래스에 _init 속성(property)이 없다면
            ----- print("[%s] %s" %("Chatbot", "[테스트] KSTFormatter __init__ 메서드: Called!"))

            # TODO: 아래와 같은 오류 메시지 출력되어 부모 클래스(logging.Formatter) __init__ 메서드(super().__init__(*args, **kwargs)) 호출 구현 (2025.09.18 minjae)
            # 오류 메시지: AttributeError: 'KSTFormatter' object has no attribute '_style'
            super().__init__(*args, **kwargs)

            self.__kst = ZoneInfo("Asia/Seoul")   # 대한민국 표준시로 시간 설정할 수 있도록 ZoneInfo 클래스 싱글톤 객체 __kst 생성
            ----- print("[%s] %s" %("Chatbot", "[테스트] ZoneInfo 클래스 싱글톤 객체 __kst 생성 완료"))
                  
            _class._init = True   # 초기화 완료

    @property
    def get_kst(self):   
        return self.__kst

    # TODO: setter 메서드 set_kst 필요시 사용 예정 (2025.09.18 minjae)
    # @get_kst.setter
    # def set_kst(self, kst):   
    #     self.__kst = kst

    # def formatTime(self, record, datefmt=None):
    #     # UTC+9 (대한민국 시간) 적용
    #     dt = datetime.datetime.fromtimestamp(record.created) + datetime.timedelta(hours=9)
    #     if datefmt:
    #         return dt.strftime(datefmt)
    #     else:
    #         return dt.strftime('%Y-%m-%d %H:%M:%S')
        
    # 대한민국 현재 시간 포맷에 맞게 변환
    # TODO: 아래 주석친 코드처럼 매개변수 record 사용하지 않더라도 생략하고 구현시 오류 발생하여 매개변수 record 작성 필수! (2025.09.18 minjae)
    # def formatTime(self, datefmt=None):
    def formatTime(self, record, datefmt=None):
        # TODO: zoneinfo 파이썬 라이브러리 사용하여 로그 출력시 대한민국 표준시로 출력 기능 구현 (2025.06.13 minjae)
        # 참고 URL - https://docs.python.org/ko/3.9/library/zoneinfo.html#module-zoneinfo
        # 참고 2 URL - https://wikidocs.net/236273
        # 참고 3 URL - https://chatgpt.com/c/684b79a8-8c20-8010-9d14-41ab28f12747

        time_stamp = datetime.fromtimestamp(record.created, tz=self.__kst)   # record의 생성 시간을 KST(self.__kst)로 변환

        # TODO : 대한민국 현재 날짜와 시간을 특정 포맷으로 변환하기 구현 (2025.03.27 minjae)
        # 참고 URL - https://wikidocs.net/269063
        if datefmt: return time_stamp.strftime(datefmt)
        else: return time_stamp.strftime('%Y-%m-%d %H:%M:%S')

# Log 싱글톤(singleton) 클래스
# 주의사항 - logging 라이브러리 getLogger 함수 사용할 경우 따로 싱글톤(singleton) 클래스 구현할 필요없다.
# Logger 자체가 Singleton 패턴 이다. 
# getLogger 함수를 호출 한다고 매번 새로운 instance가 return되는게 아니라 이미 그 이름으로 존재하는 Logger를 return한다.
# 참고 URL - https://chuun92.tistory.com/7
# 참고 2 URL - https://malwareanalysis.tistory.com/527
# 참고 3 URL - https://github.com/sungwook-practice/python_logging_logger.git
# 참고 4 URL - https://velog.io/@qlgks1/python-python-logging-%ED%95%B4%EB%B6%80
# class Log(object):
#    logger = None

# Logger 싱글톤(singleton) 클래스 
# 참고 URL - https://ko.wikipedia.org/wiki/%ED%95%9C%EA%B5%AD_%ED%91%9C%EC%A4%80%EC%8B%9C
# 참고 2 URL - https://namu.wiki/w/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%20%ED%91%9C%EC%A4%80%EC%8B%9C
# 참고 3 URL - https://claude.ai/chat/668f891e-0933-4be4-9fe3-1501f5ee4a8b
# 참고 4 URL - https://gemini.google.com/app/4a765afe3354a6f3?is_sa=1&is_sa=1&android-min-version=301356232&ios-min-version=322.0&campaign_id=bkws&utm_source=sem&utm_source=google&utm_medium=paid-media&utm_medium=cpc&utm_campaign=bkws&utm_campaign=2024koKR_gemfeb&pt=9008&mt=8&ct=p-growth-sem-bkws&gclsrc=aw.ds&gad_source=1&gad_campaignid=20437330476&gbraid=0AAAAApk5BhkFY-PS3EihuSFdGTCbo0Dve&gclid=Cj0KCQjww4TGBhCKARIsAFLXndSHcQLntbP_2PPtqGImWLQIs1IYX05tBJDhFGgPdohQVBaTb11q774aAsyxEALw_wcB
# class Logger(object): 
#     """
#     # 로그 레벨 종류 
#     |   Level   |   Value   |   When to use
#     |   DEBUG   |     10    | (주로 문제 해결을 할때 필요한) 자세한 정보. - 개발 과정에서 오류 원인 파악하고자 할 때 사용
#     |   INFO    |     20    | 작업이 정상적으로 작동하고 있다는 메시지. 
#     |  WARNING  |     30    | 예상하지 못한 일이 발생하거나, 발생 가능한 문제점을 명시. (e.g 'disk space low') 작업은 정상적으로 진행.
#     |   ERROR   |     40    | 프로그램이 함수를 실행하지 못 할 정도의 심각한 문제.
#     | CRICTICAL |     50    | 프로그램이 동작할 수 없을 정도의 심각한 문제. 
#     """
#     """
#     싱글톤 패턴으로 구현된 Logger 클래스
#     전역에서 하나의 인스턴스만 생성되어 사용됩니다.
#     """
#     ----- _instance = None
#     ----- _lock = threading.Lock()  # 멀티스레드 환경에서 안전한 싱글톤 구현
    
#     # 로그 레벨 상수
#     ----- DEBUG = 'debug'
#     ----- INFO = 'info'
#     ----- WARNING = 'warning'
#     ----- ERROR = 'error'
#     ----- CRITICAL = 'critical'

#     ----- def __new__(_class, *args, **kwargs):            # Logger 클래스에서 재 정의된 __new__ 메서드이며, 매개변수 _class의 경우 여기서는 Logger 클래스 의미함.
#         """
#         싱글톤 패턴 구현: __new__ 메서드 오버라이딩
#         멀티스레드 환경에서도 안전하도록 락(lock) 사용
#         """
#         if cls._instance is None:
#             with cls._lock:
#                 # 더블 체킹 락킹 패턴
#                 if cls._instance is None:
#                     cls._instance = super().__new__(cls)
#                     cls._instance._initialized = False
#         return cls._instance


#     ----- def __init__(self):  # 객체 생성 시 전달된 모든 인자를 __new__ 메서드가 먼저 받고, 그 다음 __init__ 메서드로 전달
#         """
#         초기화 메서드
#         싱글톤이므로 한 번만 초기화됨
#         """
#         if not self._initialized:
#             self.kst = ZoneInfo("Asia/Seoul")  # 대한민국 표준시
#             self._initialized = True
            
#             # 싱글톤 객체 생성 로그 출력
#             current_frame = inspect.currentframe()
#             file_name = os.path.basename(current_frame.f_code.co_filename)
#             function_name = current_frame.f_code.co_name
#             lineno = current_frame.f_lineno
#             print(f"[Chatbot] [{self.INFO}] [{file_name} | {function_name} - L{lineno}]: Logger 싱글톤 객체 생성 완료")
    

#     ----- def _get_caller_info(self):
#         """
#         상위 호출자 파일, 함수, 라인 정보 반환
#         """
#         frame = inspect.currentframe().f_back.f_back.f_back
#         file_name = os.path.basename(frame.f_code.co_filename)
#         function_name = frame.f_code.co_name
#         lineno = frame.f_lineno
#         return file_name, function_name, lineno
    
#     ----- def _get_formatted_time(self):
#         """
#         현재 시간을 포맷에 맞게 변환
#         """
#         return datetime.now(self.kst).strftime("%Y-%m-%d %H:%M:%S")
    
#     ----- def _log_write(self, log_type, log_level, content, text):
#         """
#         공통 로그 작성 함수
#         """
#         timestamp = self._get_formatted_time()
#         file_name, function_name, lineno = self._get_caller_info()
#         print(f"[{log_type}] [{log_level}] [{timestamp}] [{file_name} | {function_name} - L{lineno}]: {content} - {text}")

#     ----- def log_write(self, log_level, content, text):
#         """
#         챗봇 로그 작성
#         """
#         self._log_write("Chatbot", log_level, content, text)

#     ----- def openAI_log_write(self, log_level, content, text):
#         """
#         OpenAI 로그 작성
#         """
#         self._log_write("OpenAI", log_level, content, text)

#     # 싱글톤 인스턴스를 반환하는 팩토리 함수
#     ----- def get_logger():
#         """
#         Logger 싱글톤 인스턴스를 반환하는 팩토리 함수
#         """
#         return Logger()

#     # 기존 함수 호환성을 위한 래퍼 함수들
#     @staticmethod
#     ----- def log_write(log_level, content, text):
#         """
#         기존 코드 호환성을 위한 래퍼 함수
#         """
#         logger = Logger()
#         logger.log_write(log_level, content, text)

#     @staticmethod
#     ----- def openAI_log_write(log_level, content, text):
#         """
#         기존 코드 호환성을 위한 래퍼 함수
#         """
#         logger = Logger()
#         logger.openAI_log_write(log_level, content, text)


# 참고 
# 싱글턴(singleton) 패턴 - 사용자가 여러 번 객체 생성을 하더라도 클래스로부터 오직 하나의 객체(유일한 객체)만 생성되도록 하는 디자인 패턴 의미.
# 참고 URL - https://wikidocs.net/69361
# 참고 2 URL - https://wikidocs.net/3693  

# 파이썬 가변인자 *args / **kwargs
# *args - 위치 가변 인자라고 불리며, 함수를 정의할 때 인자값의 개수를 가변적으로 정의해주는 기능이며, 함수 호출부에서 서로 다른 개수의 인자를 전달하고자 할 때 가변 인자(Variable argument)를 사용함. (예) foo(1, 2, 3), foo(1, 2, 3, 4) 
#         함수 호출시 args라는 변수는 여러 개의 입력에 대해 튜플로 저장한 후 이 튜플 객체를 바인딩한다. (예) (1, 2, 3), (1, 2, 3, 4)
# **kwargs - 키워드 가변 인자라고 불리며, keyword arguments의 약어(kwargs)이다. 예를들어 함수 호출부에서 a=1, b=2, c=3과 어떤 키워드와 해당 키워드에 값을 전달힌다. (예) foo(a=1, b=2, c=3)
#            함수의 결과를 살펴보면 kwargs라는 변수가 딕셔너리 객체를 바인딩함을 알 수 있습니다. 이때 딕셔너리에는 함수 호출부에서 전달한 키워드와 값이 저장된다. (예) {'a': 1, 'b': 2, 'c': 3}
# 참고 URL - https://wikidocs.net/69363
# 참고 2 URL - https://claude.ai/chat/601e10e4-39ad-48fe-aa73-7070ba600f3d

# 파이썬 Setter / Getter 
# 파이썬에서 class을 지원하기 때문에 setter/getter 또한 지원함.
# 참고 URL - https://wikidocs.net/21053

# 참고 2
# 비동기 프로그래밍 전용 모듈 asyncio (asyncio는 async/await 구문을 사용하여 동시성 코드를 작성하는 라이브러리이다.)
# 참고 URL - https://docs.python.org/3/library/asyncio.html
# 참고 2 URL - https://docs.python.org/ko/3/library/asyncio-task.html
# 참고 3 URL - https://dojang.io/mod/page/view.php?id=2469
# 참고 4 URL - https://wikidocs.net/125092
# 참고 5 URL - https://wikidocs.net/252232