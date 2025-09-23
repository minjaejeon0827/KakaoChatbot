# 싱글톤(singleton) 패턴 전용 모듈

import asyncio   # 비동기 프로그래밍(async - await) 전용 모듈 
import logging   # 로그 작성 전용 모듈

from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트
from modules import chatbot_logger   # 챗봇 커스텀 로그 작성 모듈 -> 챗봇 전역 로그 객체(logger) 사용 못하는 경우 import 처리

# TODO: 순환 임포트(circular import) 문제(modules.singleton.py → modules.log import 처리 <-> modules.log.py → modules.singleton.KSTFormatter import 처리)로 인해 아래와 같은 오류 발생하여 챗봇 전역 로그 객체(logger) import 처리문 주석 처리 진행 (2025.09.19 minjae)
# 참고 URL - https://claude.ai/chat/b9d2cade-0c63-4549-98cb-6a35f03c86c9
# 오류 메시지 
# 1. [ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': cannot import name 'logger' from partially initialized module 'modules.log' (most likely due to a circular import) (/var/task/modules/log.py)Traceback (most recent call last):
# 2. [ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': cannot import name 'KSTFormatter' from partially initialized module 'modules.singleton' (most likely due to a circular import) (/var/task/modules/singleton.py)Traceback (most recent call last):
# from modules.log import logger    # 챗봇 전역 로그 객체(logger)  
from restAPI import chatbot_restServer    # 챗봇 웹서버 Rest API 메서드 

from datetime import datetime 
from zoneinfo import ZoneInfo    # 대한민국 표준시 설정 전용 모듈

from enum import Enum    # Enum 열거형 구조체 전용 모듈

# 데이터 유효성 검사 Enum 열거형 구조체 클래스 
# 참고 URL - https://docs.python.org/ko/3.9/library/enum.html#functional-api
# 참고 2 URL - https://wikidocs.net/105486
class EnumValidator(Enum):
    """
    Description: 

    Attributes:

    Parameters:

    Properties:
    
    """

    NOT_EXISTENCE = 0   # 데이터 존재 안 함.
    EXISTENCE = 1   # 데이터 존재함.

# 챗봇 마스터 데이터 싱글톤(singleton) 클래스 
# 마스터 데이터 - SW 프로그램을 실행하기 위해 사용되는 기준 데이터 의미. (특정 기업의 업무지식 및 비즈니스 운영의 핵심 정보 반영 필수!) 
# 참고 URL - https://en.wikipedia.org/wiki/Master_data
# 참고 2 URL - https://wiki1.kr/index.php/%EB%A7%88%EC%8A%A4%ED%84%B0%EB%8D%B0%EC%9D%B4%ED%84%B0#cite_note-masterdata_synopsis-2
# 참고 3 URL - https://claude.ai/chat/5a7fdfc5-6cb8-4286-bb10-a3082e164934

class MasterEntity(object):
    """
    Description: 

    Attributes:

    Parameters:

    Properties:

    Methods:
    
    """

    def __new__(_class, *args, **kwargs):      
        """
        Description: 객체 생성자
                     부모 클래스(object) 상속 받은 마스터 데이터 싱글톤(singleton) 클래스(MasterEntity)에서 재정의된 생성자(__new__) 이다. 
                     
                     *** 주요 특징 ***         
                     1. __new__ 메서드는 해당 클래스(MasterEntity)에 정의되어 있지 않으면 알아서 부모 클래스(object)의 __new__ 메서드가 호출되어 객체 생성
                     2. 해당 클래스 정의할 때, __new__ 메서드를 사용자가 작성할 수도 있는데 이 경우 부모 클래스(object)의 __new__ 메서드가 아니라 
                        해당 클래스에 정의된 __new__ 메서드가 호출되는데 이를 오버라이드(override) 했다고 표현   

                     참고 URL - https://docs.python.org/ko/3.6/reference/datamodel.html#object.__new__

        Parameters: 
        _class (class): MasterEntity 클래스
        *args (tuple): 위치 가변 인자
        **kwargs (Dictionary): 키워드 가변 인자

        Returns: 
        object: 마스터 데이터 싱글톤(singleton) 클래스(MasterEntity) 객체
        """

        if not hasattr(_class, "_instance"):   # 해당 클래스에 _instance 속성(property - 객체)이 없다면
            _class._instance = super().__new__(_class)  
            chatbot_logger.info("[테스트] MasterEntity __new__ 메서드 - 호출 완료!")
        return _class._instance                         

    def __init__(self, valid_targets):  
        """
        Description: 생성된 객체 초기화

                     *** 주요 특징 ***
                     1. 객체 생성 시 전달된 모든 인자(valid_targets는 제외)를 __new__ 메서드가 먼저 받고, 그 다음 __init__ 메서드로 전달
                     2. 생성된 객체에 속성(property) 추가 및 값 할당 

                     참고 URL - https://docs.python.org/ko/3.6/reference/datamodel.html#object.__init__

        Parameters: 
        self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)
        valid_targets (list): 마스터 데이터 유효성 검사 대상 리스트

        Returns: 없음. 
        """

        _class = type(self)
        if not hasattr(_class, "_init"):   # 해당 클래스에 _init 속성(property)이 없다면 
            asyncio.run(self.initSettingAsync(valid_targets))   # 이벤트 루프(asyncio.run) 실행하여 비동기 메서드 self.initSettingAsync(valid_targets) 호출     
            chatbot_logger.info("[테스트] MasterEntity __init__ 메서드 - 호출 완료!")           
            _class._init = True   # 초기화 완료  

    @property
    def get_master_datas(self):   
        """
        Description: 마스터 데이터 가져오기 

        Parameters: 
        self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)

        Returns: 
        Dictionary: 마스터 데이터 
        """
        
        return self.__master_datas

    # TODO: setter 메서드 set_master_datas 필요시 사용 예정 (2025.09.15 minjae)
    # @get_master_datas.setter
    # def set_master_datas(self, master_datas):   
    #     """
    #     Description: 마스터 데이터 셋팅  

    #     Parameters: 
    #     self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)
    #     master_datas (Dictionary): 마스터 데이터 

    #     Returns: 없음.
    #     """
        
    #     self.__master_datas = master_datas

    @property
    def get_chatbot_messageTexts(self):
        """
        Description: [챗봇 문의] 버튼 메시지 텍스트 리스트 가져오기   

        Parameters: 
        self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)

        Returns: 
        list: [챗봇 문의] 버튼 메시지 텍스트 리스트
        """

        return self.__chatbot_messageTexts

    # TODO: setter 메서드 set_chatbot_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_chatbot_messageTexts.setter
    # def set_chatbot_messageTexts(self, chatbot_messageTexts):
    #     """
    #     Description: [챗봇 문의] 버튼 메시지 텍스트 리스트 셋팅

    #     Parameters: 
    #     self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)
    #     chatbot_messageTexts (list): [챗봇 문의] 버튼 메시지 텍스트 리스트

    #     Returns: 없음. 
    #     """
        
    #     self.__chatbot_messageTexts = chatbot_messageTexts

    @property
    def get_adsk_messageTexts(self):
        """
        Description: [Autodesk 제품 설치 문의] 버튼 메시지 텍스트 리스트 가져오기 

        Parameters: 
        self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)

        Returns: 
        list: [Autodesk 제품 설치 문의] 버튼 메시지 텍스트 리스트
        """

        return self.__adsk_messageTexts

    # TODO: setter 메서드 set_adsk_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_adsk_messageTexts.setter
    # def set_adsk_messageTexts(self, adsk_messageTexts):
    #     """
    #     Description: [Autodesk 제품 설치 문의] 버튼 메시지 텍스트 리스트 셋팅

    #     Parameters: 
    #     self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)
    #     adsk_messageTexts (list): [Autodesk 제품 설치 문의] 버튼 메시지 텍스트 리스트

    #     Returns: 없음.  
    #     """

    #     self.__adsk_messageTexts = adsk_messageTexts

    @property
    def get_box_messageTexts(self):
        """
        Description: [상상진화 BOX 제품 설치 문의] 버튼 메시지 텍스트 리스트 가져오기

        Parameters: 
        self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)

        Returns: 
        list: [상상진화 BOX 제품 설치 문의] 버튼 메시지 텍스트 리스트
        """

        return self.__box_messageTexts

    # TODO: setter 메서드 set_box_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_box_messageTexts.setter
    # def set_box_messageTexts(self, box_messageTexts):
    #     """
    #     Description: [상상진화 BOX 제품 설치 문의] 버튼 메시지 텍스트 리스트 셋팅

    #     Parameters: 
    #     self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)
    #     box_messageTexts (list): [상상진화 BOX 제품 설치 문의] 버튼 메시지 텍스트 리스트

    #     Returns: 없음. 
    #     """

    #     self.__box_messageTexts = box_messageTexts

    @property
    def get_valid_targets(self):   
        """
        Description: 마스터 데이터 유효성 검사 대상 리스트 가져오기

        Parameters: 
        self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)

        Returns: 
        list: 마스터 데이터 유효성 검사 대상 리스트
        """
                
        return self.__valid_targets

    # TODO: setter 메서드 set_valid_targets 필요시 사용 예정 (2025.09.15 minjae)
    # @get_valid_targets.setter
    # def set_valid_targets(self, valid_targets):   
    #     """
    #     Description: 마스터 데이터 유효성 검사 대상 리스트 셋팅 

    #     Parameters: 
    #     self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)
    #     valid_targets (list): 마스터 데이터 유효성 검사 대상 리스트

    #     Returns: 없음. 
    #     """
        
    #     self.__valid_targets = valid_targets

    @property
    def get_isValid(self):   
        """
        Description: 마스터 데이터 유효성 검사 결과 가져오기  

        Parameters: 
        self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)

        Returns: 
        bool: 마스터 데이터 유효성 검사 결과
        """

        return self.__isValid

    # TODO: setter 메서드 set_isValid 필요시 사용 예정 (2025.09.15 minjae)
    # @get_isValid.setter
    # def set_isValid(self, isValid):  
    #     """
    #     Description: 마스터 데이터 유효성 검사 결과 셋팅 

    #     Parameters: 
    #     self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)
    #     isValid (bool): 마스터 데이터 유효성 검사 결과

    #     Returns: 없음. 
    #     """
        
    #     self.__isValid = isValid

    async def initSettingAsync(self, valid_targets):
        """
        Description: 마스터 데이터 초기 셋팅  

        Parameters: 
        self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)  
        valid_targets (list): 마스터 데이터 유효성 검사 대상 리스트

        Returns: 없음.
        """

        try:
            chatbot_logger.info("[테스트] 마스터 데이터 초기 셋팅 - 시작!")

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
 
            chatbot_logger.info("[테스트] 마스터 데이터 초기 셋팅 결과 - 완료!")
        
        except Exception as e:     
            error_msg = str(e)          
            chatbot_logger.error(f"[테스트] 오류 - {error_msg}") 

    # TODO: 추후 필요시 아래 메서드 isValidator 로직 수정 예정 (2025.09.02 minjae)
    def isValidator(self):
        """
        Description: 마스터 데이터 유효성 검사           
                     참고 URL - https://chatgpt.com/c/68017acc-672c-8010-8649-7fa39f17d834 

        Parameters: 
        self (object): 마스터 데이터 싱글톤(singleton) 클래스 객체 자신 (MasterEntity class)

        Returns: 
        bool: 마스터 데이터 유효성 검사 결과 
        """
                
        # master_datas = None    
        master_datas = self.get_master_datas     # 마스터 데이터
        valid_targets = self.get_valid_targets   # 마스터 데이터 유효성 검사 대상 리스트

        try:
            chatbot_logger.info(f"[테스트] 마스터 데이터 유효성 검사 대상 리스트 - {valid_targets}")
            chatbot_logger.info("[테스트] 마스터 데이터 유효성 검사 - 시작!")

            if None is master_datas:    
                raise Exception("마스터 데이터 로드 실패!")

            # TODO: Dictionary 객체 master_datas를 for문으로 루핑하기 위해 items() 메서드 사용 구현 (2025.09.02 minjae)
            # 참고 URL - https://docs.python.org/ko/3.13/tutorial/datastructures.html#looping-techniques 
            for parent_key, parent_value in master_datas.items():
                chatbot_logger.info(f"[테스트] master_datas - parent_key: {parent_key} / parent_value: {parent_value}")
                master_data = parent_value
                for child_key, child_value in master_data.items():
                    if child_key in valid_targets:   # 유효성 검사 대상 키들만 확인
                        chatbot_logger.info(f"[테스트] master_data - child_key: {child_key} / child_value: {child_value}")
                        # 파이썬 함수 len 사용하여 문자열, 리스트 객체 길이 구하기
                        # 참고 URL - https://wikidocs.net/215513            
                        if (None is child_value or EnumValidator.NOT_EXISTENCE.value >= len(child_value)):   # child_value 값이 존재하지 않거나(None) 길이가 0보다 작거나 같은 경우 
                            chatbot_logger.info("[테스트] 마스터 데이터 유효성 검사 결과 - 오류!")
                            return False   

            chatbot_logger.info("[테스트] 마스터 데이터 유효성 검사 결과 - 완료!")
            return True    
        
        except Exception as e:     
            error_msg = str(e)           
            chatbot_logger.error(f"[테스트] 오류 - {error_msg}")
            return False    
                

# 로그 기록 시 대한민국 표준시 설정을 위한 사용자 정의 Formatter 싱글톤(singleton) 클래스 (pytz 라이브러리 사용 안 함.)
# 참고 URL - https://claude.ai/chat/8fc1ceeb-fe95-4d1b-8517-ecec83beb3f2
class KSTFormatter(logging.Formatter):
    """
    Description: 

    Attributes:

    Parameters:

    Properties:
    
    Methods:
    """
            
    # TODO: 아마존 웹서비스 람다 함수(AWS Lambda function) 환경에서는 단일 스레드(single thread)로 실행되므로 아래 주석친 코드(_lock = threading.Lock()) 사용할 필요 없음. (2025.09.18 minjae)
    # _lock = threading.Lock()   # _lock = threading.Lock() 용도 - 일반적인 Python 응용 프로그램 환경에서 여러 스레드가 동시에 싱글톤을 생성하려 할 때 또는 Race condition으로 인해 여러 인스턴스가 생성될 가능성이 있을 때 사용한다.

    def __new__(_class, *args, **kwargs):      # KSTFormatter 클래스에서 재정의된 __new__ 메서드이며, 매개변수 _class의 경우 여기서는 KSTFormatter 클래스 의미함.
        """
        Description: 

        Parameters: 

        Returns: 
        """

        if not hasattr(_class, "_instance"):   # 해당 클래스에 _instance 속성(property - 객체)이 없다면 
            _class._instance = super().__new__(_class)  
            chatbot_logger.info("[테스트] KSTFormatter __new__ 메서드 - 호출 완료!")
        return _class._instance                         

    def __init__(self, *args, **kwargs):  # 객체 생성 시 전달된 모든 인자를 __new__ 메서드가 먼저 받고, 그 다음 __init__ 메서드로 전달
        """
        Description: 

        Parameters: 

        Returns: 
        """
                
        _class = type(self)
        if not hasattr(_class, "_init"):   # 해당 클래스에 _init 속성(property)이 없다면
            # TODO: 아래와 같은 오류 메시지 출력되어 부모 클래스(logging.Formatter) __init__ 메서드(super().__init__(*args, **kwargs)) 호출 구현 (2025.09.18 minjae)
            # 오류 메시지: AttributeError: 'KSTFormatter' object has no attribute '_style'
            super().__init__(*args, **kwargs)

            self.__kst = ZoneInfo("Asia/Seoul")   # 대한민국 표준시 설정할 수 있도록 ZoneInfo 클래스 객체 __kst 생성
            chatbot_logger.info("[테스트] ZoneInfo 클래스 싱글톤 객체 __kst - 생성 완료!")
            chatbot_logger.info("[테스트] KSTFormatter __init__ 메서드 - 호출 완료!")
            _class._init = True   # 초기화 완료

    @property
    def get_kst(self):   
        """
        Description: 대한민국 표준시 설정 가져오기 (ZoneInfo class) 

        Parameters: 
        self (object): 대한민국 표준시 설정 Formatter 싱글톤(singleton) 클래스 객체 자신 (KSTFormatter class)

        Returns: 
        object: 대한민국 표준시 설정 (ZoneInfo class) 
        """

        return self.__kst

    # TODO: setter 메서드 set_kst 필요시 사용 예정 (2025.09.18 minjae)
    # @get_kst.setter
    # def set_kst(self, kst):   
    #     """
    #     Description: 대한민국 표준시 설정 셋팅 (ZoneInfo class)  

    #     Parameters: 
    #     self (object): 대한민국 표준시 설정 Formatter 싱글톤(singleton) 클래스 객체 자신 (KSTFormatter class)
    #     kst (object): 대한민국 표준시 설정 (ZoneInfo class) 

    #     Returns: 없음.
    #     """

    #     self.__kst = kst
        
    def formatTime(self, record, datefmt=None):
        """
        Description: 지정된 LogRecord(record)의 생성 시간(현재 날짜 및 시간)을 대한민국 표준시 포맷된 문자열로 가져오기
                     아래 코드처럼 매개변수 record 사용하지 않더라도 생략하고 구현시 오류 발생하여 매개변수 record 작성 필수! (2025.09.18 minjae)
                     def formatTime(self, datefmt=None):
                     
                     파이썬 공식 문서 
                     - formatTime(record, datefmt=None)
                     참고 URL - https://docs.python.org/ko/3/library/logging.html#logging.Formatter.formatTime

                     - class logging.LogRecord(name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None) 
                     참고 2 URL - https://docs.python.org/ko/3/library/logging.html#logrecord-objects

                     - LogRecord attributes (속성) 
                     참고 3 URL - https://docs.python.org/ko/3/library/logging.html#logrecord-attributes  

        Parameters:  
        self (object): 대한민국 표준시 포맷 객체 자신 (KSTFormatter class) 
        record (object): 지정된 LogRecord(record) 객체 (logging.LogRecord class)
        datefmt (str): 날짜 출력 형식 문자열. datefmt 값이 None일 경우 기본 값 사용 (예) self.default_time_format = '%Y-%m-%d %H:%M:%S'.

        Returns: 
        str: 지정된 LogRecord(record)의 생성 시간(현재 날짜 및 시간)을 대한민국 표준시 포맷된 문자열 (time_stamp.strftime(datefmt) / time_stamp.strftime('%Y-%m-%d %H:%M:%S'))
        """
                
        # zoneinfo 파이썬 라이브러리 사용하여 로그 출력시 대한민국 표준시 출력 기능 구현 (2025.06.13 minjae)
        # 참고 URL - https://docs.python.org/ko/3.9/library/zoneinfo.html#module-zoneinfo
        # 참고 2 URL - https://wikidocs.net/236273
        # 참고 3 URL - https://chatgpt.com/c/684b79a8-8c20-8010-9d14-41ab28f12747
        time_stamp = datetime.fromtimestamp(record.created, tz=self.__kst)   # LogRecord(record)의 생성 시간을 KST(self.__kst)로 변환

        # 대한민국 현재 날짜와 시간을 특정 포맷으로 변환하기 구현 (2025.03.27 minjae)
        # 참고 URL - https://wikidocs.net/269063
        if datefmt: return time_stamp.strftime(datefmt)
        else: return time_stamp.strftime('%Y-%m-%d %H:%M:%S')

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