"""
* 싱글톤 (singleton) 패턴 전용 모듈 

*** 파이썬 문서 ***
* 1. 클래스
참고 URL - https://docs.python.org/ko/3/tutorial/classes.html
참고 2 URL - https://wikidocs.net/28
참고 3 URL - https://wikidocs.net/215474

* 2. 클래스 인스턴스 변수 접근제한자 private 대신 언더바(__) 2개 사용
참고 URL - https://docs.python.org/ko/3/reference/expressions.html#private-name-mangling
참고 2 URL - https://wikidocs.net/297028
참고 3 URL - https://wikidocs.net/297029
참고 4 URL - https://oniondev.tistory.com/20

* 3. functools @cached_property
참고 URL - https://docs.python.org/ko/dev/library/functools.html
참고 2 URL - https://sosodev.tistory.com/entry/Python-cachedproperty-%EA%B0%92%EC%9D%84-%EC%9E%AC%EC%82%AC%EC%9A%A9-%ED%95%98%EA%B8%B0

* 4. 패키지, 모듈
참고 URL - https://docs.python.org/ko/3.13/tutorial/modules.html
참고 2 URL - https://wikidocs.net/1418
참고 3 URL - https://dojang.io/mod/page/view.php?id=2450

* 5. Type Hints
참고 URL - https://docs.python.org/ko/3.14/library/typing.html
참고 2 URL - https://peps.python.org/pep-0484/
참고 3 URL - https://devpouch.tistory.com/189
참고 4 URL - https://supermemi.tistory.com/entry/Python-3-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-%EC%9D%98%EB%AF%B8%EB%8A%94-%EB%AC%B4%EC%97%87%EC%9D%BC%EA%B9%8C-%EC%A3%BC%EC%84%9D

* 6. Type Hints class Any
참고 URL - https://docs.python.org/ko/3.9/library/typing.html#the-any-type

"""  

# 1. 공통 모듈 먼저 import 처리
from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트

# 2. 챗봇 커스텀 로그 기록 모듈 import 처리
from utils import chatbot_logger   # log.py -> 챗봇 전역 로그 객체(logger) 사용 못하는 경우 import 처리

# 3. Type Hints class Any import
from typing import Any, Self

# 4. 나머지 모듈 import 처리
import logging   # 로그 기록 
import asyncio   # 비동기 프로그래밍(async - await) 

from functools import cached_property
from datetime import datetime
from zoneinfo import ZoneInfo    # 대한민국 표준시 설정

# TODO: 순환 임포트(circular import) 문제(modules.singleton.py → modules.log import 처리 <-> modules.log.py → modules.singleton.KSTFormatter import 처리)로 인해 아래와 같은 오류 발생하여 챗봇 전역 로그 객체(logger) import 처리문 주석 처리 진행 (2025.09.19 minjae)
# 참고 URL - https://claude.ai/chat/b9d2cade-0c63-4549-98cb-6a35f03c86c9
# 오류 메시지 
# 1. [ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': cannot import name 'logger' from partially initialized module 'modules.log' (most likely due to a circular import) (/var/task/modules/log.py)Traceback (most recent call last):
# 2. [ERROR] Runtime.ImportModuleError: Unable to import module 'lambda_function': cannot import name 'KSTFormatter' from partially initialized module 'modules.singleton' (most likely due to a circular import) (/var/task/modules/singleton.py)Traceback (most recent call last):
# from modules.log import logger   # 챗봇 전역 로그 객체(logger)  
from restAPI import chatbot_restServer   # 챗봇 웹서버 Rest API 메서드 
from enum import Enum    # Enum 열거형 구조체 

class EnumValidator(Enum):   # 명시적으로 Enum 클래스 상속
    """
    Description: 데이터 유효성 검사 Enum 열거형 구조체 클래스
                 참고 URL - https://docs.python.org/ko/3.9/library/enum.html#functional-api
                 참고 2 URL - https://wikidocs.net/105486

    Attributes: NOT_EXISTENCE (int) - 데이터 존재 안 함. (default: 0)
                EXISTENCE (int) - 데이터 존재함. (default: 1)
    """

    NOT_EXISTENCE = 0
    EXISTENCE = 1

# class MasterEntity(object):   # 명시적으로 object 클래스 상속
class MasterEntity:   # 암시적으로 object 클래스 상속
    """
    Description: 마스터 데이터 싱글톤 (singleton) 클래스

                 * 참고
                 마스터 데이터 - SW 프로그램을 실행하기 위해 사용되는 기준 데이터 의미. (특정 기업의 업무지식 및 비즈니스 운영의 핵심 정보 반영 필수!) 
                 참고 URL - https://en.wikipedia.org/wiki/Master_data
                 참고 2 URL - https://wiki1.kr/index.php/%EB%A7%88%EC%8A%A4%ED%84%B0%EB%8D%B0%EC%9D%B4%ED%84%B0#cite_note-masterdata_synopsis-2
                 참고 3 URL - https://claude.ai/chat/5a7fdfc5-6cb8-4286-bb10-a3082e164934 

                 class Docstring 작성 가이드라인
                 참고 URL - https://claude.ai/chat/0556e5bc-59d5-4d40-8b12-acf1e8388ee9
 
                 Properties Docstring 작성 가이드라인
                 참고 URL - https://claude.ai/chat/37ddea1f-89db-470b-b789-1781893801b7

    Attributes: _instance (MasterEntity) - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)
                _init (bool) - 인스턴스 초기화 완료 여부 (True: 완료, False: 실패)

                __master_datas (dict[str, Any]) - 전체 마스터 데이터
                __chatbot_messageTexts (list) - [챗봇 문의] 버튼 메시지 리스트
                __adsk_messageTexts (list) - [Autodesk 제품 설치 문의] 버튼 메시지 리스트
                __box_messageTexts (list) - [상상진화 BOX 제품 설치 문의] 버튼 메시지 리스트
                __valid_targets (list[str]) - 마스터 데이터 유효성 검사 시 확인할 대상 키(key) 리스트
                __isValid (bool) - 마스터 데이터 유효성 검사 통과 여부 (True: 유효함, False: 유효하지 않음)

    Parameters: *args (tuple) - object 위치 가변 인자
                **kwargs (dict) - object 키워드 가변 인자

                valid_targets (list[str]) - 마스터 데이터 유효성 검사 대상 리스트
                (예시) [ "buttons", "items", "autoCADInfos", "revitInfos", "navisworksManageInfos", "infraWorksInfos", "civil3DInfos", "revitBoxInfos", "cadBoxInfos", "energyBoxInfos", "accountInfos", "etcInfos" ]

    Properties (읽기 전용): get_master_datas (dict[str, Any]) - 전체 마스터 데이터 가져오기
                           get_chatbot_messageTexts (list[str]) - [챗봇 문의] 버튼 메시지 리스트 가져오기
                           get_adsk_messageTexts (list[str]) - [Autodesk 제품 설치 문의] 버튼 메시지 리스트 가져오기
                           get_box_messageTexts (list[str]) - [상상진화 BOX 제품 설치 문의] 버튼 메시지 리스트 가져오기
                           get_valid_targets (list[str]) - 마스터 데이터 유효성 검사 대상 리스트 가져오기
                           get_isValid (bool) - 마스터 데이터 유효성 검사 결과 가져오기

    Methods: initSettingAsync - 마스터 데이터 초기 설정
             isValidator - 마스터 데이터 유효성 검사

    Notes: - 싱글톤 (singleton) 패턴으로 구현되어 여러 번 인스턴스 (Instance) 생성해도 동일한 객체 반환
           - 아마존 웹서비스 람다 함수(AWS Lambda function) 환경에서는 단일 스레드(single thread)로 실행되므로 스레드 락(_lock = threading.Lock()) 불필요
           _lock = threading.Lock()   # _lock = threading.Lock() 용도 - 일반적인 Python 응용 프로그램 환경에서 여러 스레드가 동시에 싱글톤 (singleton) 클래스 인스턴스 (Instance)를 생성하려 할 때 또는 Race condition으로 인해 여러 인스턴스 (Instance)가 생성될 가능성이 있을 때 사용함.
    """

    # _lock = threading.Lock()   # _lock = threading.Lock() 용도 - 일반적인 Python 응용 프로그램 환경에서 여러 스레드가 동시에 싱글톤 (singleton) 클래스 인스턴스 (Instance)를 생성하려 할 때 또는 Race condition으로 인해 여러 인스턴스 (Instance)가 생성될 가능성이 있을 때 사용함.

    def __new__(_class, *args: tuple, **kwargs: dict) -> Self:
        """
        Description: 객체 생성자 - 부모 클래스 (object) 상속 받아 재정의된 생성자 (__new__) 
                     
                     *** 주요 특징 ***         
                     1. __new__ 메서드는 해당 클래스 (MasterEntity)에 정의되어 있지 않으면 알아서 부모 클래스 (object)의 __new__ 메서드가 호출되어 객체 생성
                     2. 해당 클래스 정의할 때, __new__ 메서드를 개발자가 작성할 수도 있는데 이 경우 부모 클래스 (object)의 __new__ 메서드가 아니라 
                        해당 클래스에 정의된 __new__ 메서드가 호출되는데 이를 오버라이드 (override) 했다고 표현   

                     참고 URL - https://docs.python.org/ko/3.6/reference/datamodel.html#object.__new__

        Parameters: _class - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity)
                    *args - 위치 가변 인자
                    **kwargs - 키워드 가변 인자

        Returns: _class._instance - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)
        """

        if not hasattr(_class, "_instance"):   # 해당 클래스에 _instance 속성 (property) 없다면
            _class._instance = super().__new__(_class)  
            chatbot_logger.info("[테스트] MasterEntity __new__ 메서드 - 호출 완료!")

        return _class._instance

    def __init__(self, valid_targets: list[str]) -> None:
        """
        Description: 생성된 객체 초기화

                     *** 주요 특징 ***
                     1. 객체 생성 시 전달된 모든 인자 (valid_targets 제외)를 __new__ 메서드가 먼저 받고, 그 다음 __init__ 메서드로 전달
                     2. 생성된 객체에 속성 (property) 추가 및 값 할당 

                     참고 URL - https://docs.python.org/ko/3.6/reference/datamodel.html#object.__init__

        Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)
                    valid_targets - 마스터 데이터 유효성 검사 대상 리스트

        Returns: 없음. 
        """

        _class = type(self)
        if not hasattr(_class, "_init"):   # 해당 클래스에 _init 속성 (property) 없다면 
            asyncio.run(self.initSettingAsync(valid_targets))   # 이벤트 루프(asyncio.run) 실행하여 비동기 메서드 self.initSettingAsync(valid_targets) 호출     
            chatbot_logger.info("[테스트] MasterEntity __init__ 메서드 - 호출 완료!")           
            _class._init = True   # 초기화 완료  

    @cached_property
    def get_master_datas(self) -> dict[str, Any]:
        """
        Description: 전체 마스터 데이터 가져오기 

        Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)

        Returns: self.__master_datas - 전체 마스터 데이터 
        """
        
        return self.__master_datas

    # TODO: setter 메서드 set_master_datas 필요시 사용 예정 (2025.09.15 minjae)
    # @get_master_datas.setter
    # def set_master_datas(self, master_datas: dict[str, Any]) -> None:
    #     """
    #     Description: 전체 마스터 데이터 설정  

    #     Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)
    #                 master_datas - 전체 마스터 데이터 

    #     Returns: 없음.
    #     """
        
    #     self.__master_datas = master_datas

    @cached_property
    def get_chatbot_messageTexts(self) -> list[str]:
        """
        Description: [챗봇 문의] 버튼 메시지 리스트 가져오기   

        Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)

        Returns: self.__chatbot_messageTexts - [챗봇 문의] 버튼 메시지 리스트
        """

        return self.__chatbot_messageTexts

    # TODO: setter 메서드 set_chatbot_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_chatbot_messageTexts.setter
    # def set_chatbot_messageTexts(self, chatbot_messageTexts: list[str]) -> None:
    #     """
    #     Description: [챗봇 문의] 버튼 메시지 리스트 설정

    #     Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)
    #                 chatbot_messageTexts - [챗봇 문의] 버튼 메시지 리스트

    #     Returns: 없음. 
    #     """
        
    #     self.__chatbot_messageTexts = chatbot_messageTexts

    @cached_property
    def get_adsk_messageTexts(self) -> list[str]:
        """
        Description: [Autodesk 제품 설치 문의] 버튼 메시지 리스트 가져오기 

        Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)

        Returns: self.__adsk_messageTexts - [Autodesk 제품 설치 문의] 버튼 메시지 리스트
        """

        return self.__adsk_messageTexts

    # TODO: setter 메서드 set_adsk_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_adsk_messageTexts.setter
    # def set_adsk_messageTexts(self, adsk_messageTexts: list[str]) -> None:
    #     """
    #     Description: [Autodesk 제품 설치 문의] 버튼 메시지 리스트 설정

    #     Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)
    #                 adsk_messageTexts - [Autodesk 제품 설치 문의] 버튼 메시지 리스트

    #     Returns: 없음.
    #     """

    #     self.__adsk_messageTexts = adsk_messageTexts

    @cached_property
    def get_box_messageTexts(self) -> list[str]:
        """
        Description: [상상진화 BOX 제품 설치 문의] 버튼 메시지 리스트 가져오기

        Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)

        Returns: self.__box_messageTexts - [상상진화 BOX 제품 설치 문의] 버튼 메시지 리스트
        """

        return self.__box_messageTexts

    # TODO: setter 메서드 set_box_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_box_messageTexts.setter
    # def set_box_messageTexts(self, box_messageTexts: list[str]) -> None:
    #     """
    #     Description: [상상진화 BOX 제품 설치 문의] 버튼 메시지 리스트 설정

    #     Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)
    #                 box_messageTexts - [상상진화 BOX 제품 설치 문의] 버튼 메시지 리스트

    #     Returns: 없음. 
    #     """

    #     self.__box_messageTexts = box_messageTexts

    @cached_property
    def get_valid_targets(self) -> list[str]:
        """
        Description: 마스터 데이터 유효성 검사 대상 리스트 가져오기

        Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)

        Returns: self.__valid_targets - 마스터 데이터 유효성 검사 대상 리스트
        """
                
        return self.__valid_targets

    # TODO: setter 메서드 set_valid_targets 필요시 사용 예정 (2025.09.15 minjae)
    # @get_valid_targets.setter
    # def set_valid_targets(self, valid_targets: list[str]) -> None:
    #     """
    #     Description: 마스터 데이터 유효성 검사 대상 리스트 설정 

    #     Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)
    #                 valid_targets - 마스터 데이터 유효성 검사 대상 리스트

    #     Returns: 없음. 
    #     """
        
    #     self.__valid_targets = valid_targets

    @cached_property
    def get_isValid(self) -> bool:
        """
        Description: 마스터 데이터 유효성 검사 결과 가져오기  

        Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)

        Returns: self.__isValid - 마스터 데이터 유효성 검사 결과
        """

        return self.__isValid

    # TODO: setter 메서드 set_isValid 필요시 사용 예정 (2025.09.15 minjae)
    # @get_isValid.setter
    # def set_isValid(self, isValid: bool) -> None:
    #     """
    #     Description: 마스터 데이터 유효성 검사 결과 설정 

    #     Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)
    #                 isValid - 마스터 데이터 유효성 검사 결과

    #     Returns: 없음. 
    #     """
        
    #     self.__isValid = isValid

    async def initSettingAsync(self, valid_targets: list[str]) -> None:
        """
        Description: 마스터 데이터 초기 설정

        Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)  
                    valid_targets - 마스터 데이터 유효성 검사 대상 리스트

        Returns: 없음.
        """

        try:
            chatbot_logger.info("[테스트] 마스터 데이터 초기 설정 - 시작!")
            chatbot_logger.info(f"[테스트] help 함수 호출 및 chatbot_restServer 모듈 전체 docstring 내용 확인 - {help(chatbot_restServer)}")
            chatbot_logger.info(f"[테스트] help 함수 호출 및 chatbot_restServer.get_masterDownLoadAsync 함수 docstring 내용 확인 - {help(chatbot_restServer.get_masterDownLoadAsync)}")
            chatbot_logger.info(f"[테스트] chatbot_restServer.get_masterDownLoadAsync 함수 속성 __doc__ 사용 및 docstring 내용 확인 - {chatbot_restServer.get_masterDownLoadAsync.__doc__}")

            self.__master_datas = await chatbot_restServer.get_masterDownLoadAsync(chatbot_helper._masterEntity_json_file_path)   # 전체 마스터 데이터 다운로드  
            # TODO: 리스트 컴프리헨션 문법 사용하여 "buttons" 리스트 객체 (self.__master_datas[chatbot_helper._chatbotCard][chatbot_helper._buttons])에 속한 
            #       키(key) 'messageText'에 할당된 값 (chatbotButton[chatbot_helper._messageText])만 추출하여 리스트 객체 self.__chatbot_messageTexts 값 할당 처리 (2025.08.25 minjae) 
            # 참고 URL - https://docs.python.org/ko/3.13/tutorial/datastructures.html#list-comprehensions
            # 참고 2 URL - https://claude.ai/chat/a6e38078-6a1f-4c67-a1f2-442f04d86938
            self.__chatbot_messageTexts = [ chatbotButton[chatbot_helper._messageText] for chatbotButton in self.__master_datas[chatbot_helper._chatbotCard][chatbot_helper._buttons] ]   # [챗봇 문의] 버튼 메시지 리스트  
            self.__adsk_messageTexts = [ adskButton[chatbot_helper._messageText] for adskButton in self.__master_datas[chatbot_helper._adskReplies][chatbot_helper._buttons] ]   # [Autodesk 제품 설치 문의] 버튼 메시지 리스트 
            self.__box_messageTexts = [ boxButton[chatbot_helper._messageText] for boxButton in self.__master_datas[chatbot_helper._boxReplies][chatbot_helper._buttons] ]   # [상상진화 BOX 제품 설치 문의] 버튼 메시지 리스트
            self.__valid_targets = valid_targets
            self.__isValid = self.isValidator()
 
            chatbot_logger.info("[테스트] 마스터 데이터 초기 설정 결과 - 완료!")
        
        except Exception as e:
            error_msg = str(e)          
            chatbot_logger.error(f"[테스트] 오류 - {error_msg}") 

    # TODO: 추후 필요시 아래 메서드 isValidator 로직 수정 예정 (2025.09.02 minjae)
    def isValidator(self) -> bool:
        """
        Description: 마스터 데이터 유효성 검사
                     참고 URL - https://chatgpt.com/c/68017acc-672c-8010-8649-7fa39f17d834 

        Parameters: self - 마스터 데이터 싱글톤 (singleton) 클래스 (MasterEntity) 인스턴스 (Instance)

        Returns: 마스터 데이터 유효성 검사 결과 
        """
        
        master_datas = self.get_master_datas     # 전체 마스터 데이터
        valid_targets = self.get_valid_targets   # 마스터 데이터 유효성 검사 대상 리스트

        try:
            chatbot_logger.info(f"[테스트] 마스터 데이터 유효성 검사 대상 리스트 - {valid_targets}")
            chatbot_logger.info("[테스트] 마스터 데이터 유효성 검사 - 시작!")

            if None is master_datas:    
                raise Exception("전체 마스터 데이터 로드 실패!")
            
            # 그리디 알고리즘 (Greedy Algorithm) - 탐욕법이라고 불리며, 현재 상황에서 지금 당장 좋은 것만 고르는 방법이다.
            # 참고 URL - https://youtu.be/5OYlS2QQMPA?si=LzCRpZvGmEXI5Ean
            # 참고 2 URL - https://youtu.be/_TG0hVYJ6D8?si=j85mnzUabJeClsoQ

            # dict 객체 master_datas를 for문으로 루핑하기 위해 items() 메서드 호출 (2025.09.02 minjae)
            # 참고 URL - https://docs.python.org/ko/3.13/tutorial/datastructures.html#looping-techniques 
            for parent_key, parent_value in master_datas.items():
                chatbot_logger.info(f"[테스트] master_datas - parent_key: {parent_key} / parent_value: {parent_value}")
                master_data = parent_value
                for child_key, child_value in master_data.items():
                    if child_key in valid_targets:   # 유효성 검사 대상 키들만 확인
                        chatbot_logger.info(f"[테스트] master_data - child_key: {child_key} / child_value: {child_value}")
                        # 파이썬 함수 len 사용하여 문자열, 리스트 객체 길이 구하기
                        # 참고 URL - https://docs.python.org/ko/3/library/functions.html#len                               
                        if (None is child_value or EnumValidator.NOT_EXISTENCE.value >= len(child_value)):   # child_value 값이 존재하지 않거나(None) 길이가 0보다 작거나 같은 경우 
                            chatbot_logger.info("[테스트] 마스터 데이터 유효성 검사 결과 - 오류!")
                            return False

            chatbot_logger.info("[테스트] 마스터 데이터 유효성 검사 결과 - 완료!")
            return True
        
        except Exception as e:     
            error_msg = str(e)           
            chatbot_logger.error(f"[테스트] 오류 - {error_msg}")
            return False    
                
class KSTFormatter(logging.Formatter):   # 명시적으로 logging.Formatter 클래스 상속
    """
    Description: 대한민국 표준시 설정 싱글톤 (singleton) 클래스 (pytz 라이브러리 사용 안 함.)
                 참고 URL - https://claude.ai/chat/8fc1ceeb-fe95-4d1b-8517-ecec83beb3f2

                 class Docstring 작성 가이드라인
                 참고 URL - https://claude.ai/chat/6c33a991-97cf-4736-8bcd-724cbf1a58ee

                 Properties Docstring 작성 가이드라인
                 참고 URL - https://claude.ai/chat/37ddea1f-89db-470b-b789-1781893801b7

    Attributes: _instance (KSTFormatter) - 대한민국 표준시 설정 싱글톤 (singleton) 클래스 (KSTFormatter) 인스턴스 (Instance)
                _init (bool) - 인스턴스 초기화 완료 여부 (True: 완료, False: 실패)
                __kst (ZoneInfo): 대한민국 표준시(Asia/Seoul) 클래스 (ZoneInfo) 인스턴스 (Instance)

    Parameters: *args (tuple) - logging.Formatter 위치 가변 인자 (fmt, datefmt 등)
                **kwargs (dict) - logging.Formatter 키워드 가변 인자

    Properties (읽기 전용): get_kst (ZoneInfo) - 설정된 대한민국 표준시 (Asia/Seoul) 클래스 (ZoneInfo) 인스턴스 (Instance) 가져오기
    
    Methods: formatTime - LogRecord(record)의 생성 시간(현재 날짜 및 시간)을 대한민국 표준시로 변환하여 포맷된 문자열 가져오기 

    Notes: 사용 예시: formatter = KSTFormatter('[%(levelname)s] [%(asctime)s] [%(filename)s | %(funcName)s - L%(lineno)d]: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

           - 싱글톤 패턴으로 구현되어 여러 번 인스턴스를 생성해도 동일한 객체 반환
           - 아마존 웹서비스 람다 함수(AWS Lambda function) 환경에서는 단일 스레드(single thread)로 실행되므로 스레드 락(_lock = threading.Lock()) 불필요
           _lock = threading.Lock()   # _lock = threading.Lock() 용도 - 일반적인 Python 응용 프로그램 환경에서 여러 스레드가 동시에 싱글톤 (singleton) 클래스 인스턴스 (Instance)를 생성하려 할 때 또는 Race condition으로 인해 여러 인스턴스 (Instance)가 생성될 가능성이 있을 때 사용함.
    """
    
    # _lock = threading.Lock()   # _lock = threading.Lock() 용도 - 일반적인 Python 응용 프로그램 환경에서 여러 스레드가 동시에 싱글톤 (singleton) 클래스 인스턴스 (Instance)를 생성하려 할 때 또는 Race condition으로 인해 여러 인스턴스 (Instance)가 생성될 가능성이 있을 때 사용함.

    def __new__(_class, *args: tuple, **kwargs: dict) -> Self:
        """
        Description: 객체 생성자 - 부모 클래스 (logging.Formatter) 상속 받아 재정의된 생성자(__new__)
                     
                     *** 주요 특징 ***         
                     1. __new__ 메서드는 해당 클래스 (KSTFormatter)에 정의되어 있지 않으면 알아서 부모 클래스 (logging.Formatter)의 __new__ 메서드가 호출되어 객체 생성
                     2. 해당 클래스 정의할 때, __new__ 메서드를 개발자가 작성할 수도 있는데 이 경우 부모 클래스 (logging.Formatter)의 __new__ 메서드가 아니라 
                        해당 클래스에 정의된 __new__ 메서드가 호출되는데 이를 오버라이드 (override) 했다고 표현

                     참고 URL - https://docs.python.org/ko/3.6/reference/datamodel.html#object.__new__

        Parameters: _class - 대한민국 표준시 설정 싱글톤 (singleton) 클래스 (KSTFormatter)
                    *args - 위치 가변 인자
                    **kwargs - 키워드 가변 인자

        Returns: _class._instance - 대한민국 표준시 설정 싱글톤 (singleton) 클래스 (KSTFormatter) 인스턴스 (Instance)
        """

        if not hasattr(_class, "_instance"):   # 해당 클래스에 _instance 속성 (property) 없다면 
            _class._instance = super().__new__(_class)  
            chatbot_logger.info("[테스트] KSTFormatter __new__ 메서드 - 호출 완료!")
            
        return _class._instance                

    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """
        Description: 생성된 객체 초기화

                     *** 주요 특징 ***
                     1. 객체 생성 시 전달된 모든 인자를 __new__ 메서드가 먼저 받고, 그 다음 __init__ 메서드로 전달
                     2. 생성된 객체에 속성 (property) 추가 및 값 할당 

                     참고 URL - https://docs.python.org/ko/3.6/reference/datamodel.html#object.__init__

        Parameters: self - 대한민국 표준시 설정 싱글톤 (singleton) 클래스 (KSTFormatter) 인스턴스 (Instance)
                    *args - 위치 가변 인자
                    **kwargs - 키워드 가변 인자

        Returns: 없음. 
        """
                
        _class = type(self)
        if not hasattr(_class, "_init"):   # 해당 클래스에 _init 속성 (property) 없다면
            # 아래와 같은 오류 메시지 출력되어 부모 클래스 (logging.Formatter) __init__ 메서드 (super().__init__(*args, **kwargs)) 호출 (2025.09.18 minjae)
            # 오류 메시지: AttributeError: 'KSTFormatter' object has no attribute '_style'
            super().__init__(*args, **kwargs)   # 싱글톤 (singleton) 클래스 (KSTFormatter)의 부모 클래스 (logging.Formatter) 초기화자 super().__init__(*args, **kwargs) 실행 시 파라미터 datefmt 전달 인자 값이 None일 경우 로그 기록 형식 기본 값 할당 (default_time_format = '%Y-%m-%d %H:%M:%S')

            self.__kst = ZoneInfo("Asia/Seoul")   # 대한민국 표준시 설정할 수 있도록 클래스 (ZoneInfo) 인스턴스 (Instance) __kst 생성
            chatbot_logger.info("[테스트] 싱글톤 (singleton) 클래스 (KSTFormatter) 인스턴스 (Instance) __kst - 생성 완료!")
            chatbot_logger.info("[테스트] KSTFormatter __init__ 메서드 - 호출 완료!")
            _class._init = True   # 초기화 완료

    @cached_property
    def get_kst(self) -> ZoneInfo:
        """
        Description: 설정된 대한민국 표준시 (Asia/Seoul) 클래스 (ZoneInfo) 인스턴스 (Instance) 가져오기

        Parameters: self - 대한민국 표준시 설정 싱글톤 (singleton) 클래스 (KSTFormatter) 인스턴스 (Instance)

        Returns: self.__kst - 설정된 대한민국 표준시 (Asia/Seoul) 클래스 (ZoneInfo) 인스턴스 (Instance)
        """

        return self.__kst

    # TODO: setter 메서드 set_kst 필요시 사용 예정 (2025.09.18 minjae)
    # @get_kst.setter
    # def set_kst(self, kst: ZoneInfo) -> None:
    #     """
    #     Description: 설정된 대한민국 표준시 (Asia/Seoul) 클래스 (ZoneInfo) 인스턴스 (Instance) 설정

    #     Parameters: self - 대한민국 표준시 설정 싱글톤 (singleton) 클래스 (KSTFormatter) 인스턴스 (Instance)
    #                 kst - 설정된 대한민국 표준시 (Asia/Seoul) 클래스 (ZoneInfo) 인스턴스 (Instance)

    #     Returns: 없음.
    #     """

    #     self.__kst = kst
        
    def formatTime(self, record: logging.LogRecord, datefmt: str = None) -> str:
        """
        Description: LogRecord (record)의 생성 시간 (현재 날짜 및 시간)을 대한민국 표준시로 변환하여 포맷된 문자열 가져오기
                     아래 코드처럼 매개변수 record 생략하고 구현시 오류 발생하여 매개변수 record 작성 필수! (2025.09.18 minjae)
                     def formatTime(self, datefmt=None):

                     *** 파이썬 공식 문서 ***
                     - formatTime(record, datefmt=None)
                     참고 URL - https://docs.python.org/ko/3/library/logging.html#logging.Formatter.formatTime

                     - class logging.LogRecord(name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None) 
                     참고 2 URL - https://docs.python.org/ko/3/library/logging.html#logrecord-objects

                     - LogRecord attributes 
                     참고 3 URL - https://docs.python.org/ko/3/library/logging.html#logrecord-attributes

        Parameters: self - 대한민국 표준시 설정 싱글톤 (singleton) 클래스 (KSTFormatter) 인스턴스 (Instance)
                    record - 지정된 LogRecord (record) 클래스 (logging.LogRecord) 인스턴스 (Instance)
                    datefmt - 날짜 출력 형식 문자열. (default parameter) 
                              datefmt 값이 None일 경우 기본 값 사용 (예) self.default_time_format = '%Y-%m-%d %H:%M:%S'.

        Returns: time_stamp.strftime(datefmt) / time_stamp.strftime(chatbot_helper._datefmt) - 지정된 LogRecord (record)의 생성 시간 (현재 날짜 및 시간)을 대한민국 표준시 포맷된 문자열
        """
                
        # zoneinfo 파이썬 라이브러리 사용하여 로그 출력시 대한민국 표준시 출력 기능 구현 (2025.06.13 minjae)
        # 참고 URL - https://docs.python.org/ko/3.9/library/zoneinfo.html#module-zoneinfo
        # 참고 2 URL - https://wikidocs.net/236273
        # 참고 3 URL - https://chatgpt.com/c/684b79a8-8c20-8010-9d14-41ab28f12747
        time_stamp = datetime.fromtimestamp(record.created, tz=self.__kst)   # LogRecord (record)의 생성 시간을 KST (self.__kst)로 변환

        # 대한민국 현재 날짜와 시간을 특정 포맷으로 변환하기 구현 (2025.03.27 minjae)
        # 참고 URL - https://wikidocs.net/269063
        if datefmt: return time_stamp.strftime(datefmt)
        else: return time_stamp.strftime(chatbot_helper._datefmt)

"""
*** 참고 ***
싱글톤 (singleton) 패턴 - 개발자가 여러 번 객체 생성을 하더라도 클래스로부터 오직 하나의 객체 (유일한 객체)만 생성되도록 하는 디자인 패턴 의미.
참고 URL - https://wikidocs.net/69361
참고 2 URL - https://wikidocs.net/3693  

파이썬 용어 정리  
Argument (인자) - 함수를 호출할 때 함수 (또는 메서드)로 전달되는 값.
Parameter (매개변수) - 함수 (또는 메서드) 정의에서 함수가 받을 수 있는 인자 (또는 어떤 경우 인자들)를 지정하는 이름 붙은 엔티티
Attribute (어트리뷰트) - 흔히 점표현식을 사용하는 이름으로 참조되는 객체와 결합한 값. (예를 들어, 객체 o가 어트리뷰트 a를 가지면, o.a처럼 참조)
참고 URL - https://docs.python.org/ko/3.10/glossary.html
참고 2 URL - https://peps.python.org/pep-0570/
참고 3 URL - https://peps.python.org/pep-3102/
참고 4 URL - https://leffept.tistory.com/418

파이썬 가변인자 *args / **kwargs
*args - 위치 가변 인자라고 불리며, 함수를 정의할 때 인자값의 개수를 가변적으로 정의해주는 기능이며, 함수 호출부에서 서로 다른 개수의 인자를 전달하고자 할 때 가변 인자 (Variable argument) 사용함. (예) foo(1, 2, 3), foo(1, 2, 3, 4) 
        함수 호출시 args라는 변수는 여러 개의 입력에 대해 튜플 (tuple)로 저장한 후 이 튜플 (tuple) 객체를 바인딩한다. (예) (1, 2, 3), (1, 2, 3, 4)
**kwargs - 키워드 가변 인자라고 불리며, keyword arguments의 약어(kwargs)이다. 예를들어 함수 호출부에서 a=1, b=2, c=3과 어떤 키워드와 해당 키워드에 값을 전달힌다. (예) foo(a=1, b=2, c=3)
           함수의 결과를 살펴보면 kwargs라는 변수가 딕셔너리 (dict) 객체를 바인딩함을 알 수 있다. 이때 딕셔너리 (dict)에는 함수 호출부에서 전달한 키워드와 값이 저장된다. (예) {'a': 1, 'b': 2, 'c': 3}
참고 URL - https://wikidocs.net/69363
참고 2 URL - https://claude.ai/chat/601e10e4-39ad-48fe-aa73-7070ba600f3d

파이썬 setter / getter 
파이썬에서 class 지원하기 때문에 setter / getter 또한 지원함.
참고 URL - https://wikidocs.net/21053

비동기 프로그래밍 asyncio (asyncio는 async / await 구문을 사용하여 동시성 코드를 작성하는 라이브러리이다.)
참고 URL - https://docs.python.org/3/library/asyncio.html
참고 2 URL - https://docs.python.org/ko/3/library/asyncio-task.html
참고 3 URL - https://dojang.io/mod/page/view.php?id=2469
참고 4 URL - https://wikidocs.net/125092
참고 5 URL - https://wikidocs.net/252232
"""