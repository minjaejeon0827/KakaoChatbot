# 싱글톤(singleton) 패턴 전용 모듈
import asyncio   # 비동기 프로그래밍(async - await) 전용 모듈
import logging  # 로그 작성 전용 모듈 

from modules import logger               # 폴더 "modules" -> 챗봇 로그 작성 모듈 
from commons import chatbot_helper       # 폴더 "commons" -> 챗봇 전용 도움말 텍스트 
from restAPI import chatbot_restServer   # 폴더 "restAPI" -> 챗봇 웹서버 Rest API 메서드 

from enum import Enum   # Enum 열거형 구조체 사용하기 위해 패키지 "enum"  

# 데이터 유효성 검사 Enum 열거형 구조체 클래스 
# 참고 URL - https://docs.python.org/ko/3.9/library/enum.html#functional-api
# 참고 2 URL - https://wikidocs.net/105486
class EnumValidator(Enum):
    """
    """

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
    """
    """

    def __new__(_class, *args, **kwargs):      # MasterEntity 클래스에서 재 정의된 __new__ 메서드이며, 매개변수 _class의 경우 여기서는 MasterEntity 클래스 의미함.
        """
        """

        if not hasattr(_class, "_instance"):   # 해당 클래스에 _instance 속성(property - 객체)이 없다면
            logger.log_write(logger._info, '[테스트] MasterEntity __new__ 메서드', 'Called!')
            _class._instance = super().__new__(_class)  
        return _class._instance                         

    def __init__(self, valid_targets):  # 객체 생성 시 전달된 모든 인자(valid_targets는 제외)를 __new__ 메서드가 먼저 받고, 그 다음 __init__ 메서드로 전달
        """
        """

        _class = type(self)
        if not hasattr(_class, "_init"):   # 해당 클래스에 _init 속성(property)이 없다면
            logger.log_write(logger._info, '[테스트] MasterEntity __init__ 메서드', 'Called!') 

            asyncio.run(self.initSettingAsync(valid_targets))   # 이벤트 루프(asyncio.run) 실행하여 비동기 메서드 self.initSettingAsync(valid_targets) 호출                
                  
            _class._init = True   # 초기화 완료  

    @property
    def get_master_datas(self):   
        """
        """

        return self.__master_datas

    # TODO: setter 메서드 set_master_datas 필요시 사용 예정 (2025.09.15 minjae)
    # @get_master_datas.setter
    # def set_master_datas(self, master_datas):   
    #     """
    #     """

    #     self.__master_datas = master_datas

    @property
    def get_chatbot_messageTexts(self):
        return self.__chatbot_messageTexts

    # TODO: setter 메서드 set_chatbot_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_chatbot_messageTexts.setter
    # def set_chatbot_messageTexts(self, chatbot_messageTexts):
    #     """
    #     """

    #     self.__chatbot_messageTexts = chatbot_messageTexts

    @property
    def get_adsk_messageTexts(self):
        """
        """

        return self.__adsk_messageTexts

    # TODO: setter 메서드 set_adsk_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_adsk_messageTexts.setter
    # def set_adsk_messageTexts(self, adsk_messageTexts):
    #     """
    #     """

    #     self.__adsk_messageTexts = adsk_messageTexts

    @property
    def get_box_messageTexts(self):
        """
        """

        return self.__box_messageTexts

    # TODO: setter 메서드 set_box_messageTexts 필요시 사용 예정 (2025.09.16 minjae)
    # @get_box_messageTexts.setter
    # def set_box_messageTexts(self, box_messageTexts):
    #     """
    #     """

    #     self.__box_messageTexts = box_messageTexts


    @property
    def get_isValid(self):   
        """
        """

        return self.__isValid

    # TODO: setter 메서드 set_isValid 필요시 사용 예정 (2025.09.15 minjae)
    # @get_isValid.setter
    # def set_isValid(self, isValid):  
    #     """
    #     """

    #     self.__isValid = isValid

    @property
    def get_valid_targets(self):   
        """
        """

        return self.__valid_targets

    # TODO: setter 메서드 set_valid_targets 필요시 사용 예정 (2025.09.15 minjae)
    # @get_valid_targets.setter
    # def set_valid_targets(self, valid_targets):   
    #     """
    #     """

    #     self.__valid_targets = valid_targets

    # 마스터 데이터 초기 셋팅
    async def initSettingAsync(self, valid_targets):
        """
        """

        try:
            logger.log_write(logger._info, '[테스트] 마스터 데이터 초기 셋팅', 'Start!')

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

            logger.log_write(logger._info, '[테스트] 마스터 데이터 초기 셋팅 결과', 'OK!') 
        
        except Exception as e:     
            error_msg = str(e)     
            logger.log_write(logger._error, "[테스트] 오류", error_msg)     

    # TODO: 추후 필요시 마스터 데이터 유효성 검사 메서드 isValidator 로직 수정 예정 (2025.09.02 minjae)
    # 웹서버로 부터 받아온 마스터 데이터 유효성 검사
    # 참고 URL - https://chatgpt.com/c/68017acc-672c-8010-8649-7fa39f17d834
    def isValidator(self):
        """
        """

        # master_datas = None   # 마스터 데이터 담는 Dictionary 객체 
        master_datas = self.get_master_datas     # 마스터 데이터 담는 Dictionary 객체 
        valid_targets = self.get_valid_targets   # 마스터 데이터 유효성 검사 대상 리스트

        try:
            logger.log_write(logger._info, '[테스트] 마스터 데이터 유효성 검사 대상 리스트', valid_targets)
            logger.log_write(logger._info, '[테스트] 마스터 데이터 유효성 검사', 'Start!')

            if None is master_datas:   # 마스터 데이터 담는 Dictionary 객체가 None일 경우 
                raise Exception("마스터 데이터 로드 실패!")

            # TODO: Dictionary 객체 master_datas를 for문으로 루핑하기 위해 items() 메서드 사용 구현 (2025.09.02 minjae)
            # 참고 URL - https://docs.python.org/ko/3.13/tutorial/datastructures.html#looping-techniques 
            for parent_key, parent_value in master_datas.items():
                # logger.log_write(logger._info, '[테스트] master_datas', f'key: {key} / value: {value}')
                master_data = parent_value
                for child_key, child_value in master_data.items():
                    if child_key in valid_targets:   # 유효성 검사 대상 키들만 확인
                        logger.log_write(logger._info, '[테스트] master_data', f'key: {child_key} / value: {child_value}')
                        # 파이썬 함수 len 사용하여 문자열, 리스트 객체 길이 구하기
                        # 참고 URL - https://wikidocs.net/215513            
                        if (None is child_value or EnumValidator.NOT_EXISTENCE.value >= len(child_value)):   # child_value 값이 존재하지 않거나(None) 길이가 0보다 작거나 같은 경우 
                            logger.log_write(logger._error, '[테스트] 마스터 데이터 유효성 검사 결과', 'Fail!')
                            return False   # 마스터 데이터 유효성 검사 오류 

            logger.log_write(logger._info, '[테스트] 마스터 데이터 유효성 검사 결과', 'OK!')
            return True   # 마스터 데이터 유효성 검사 성공 
        
        except Exception as e:     
            error_msg = str(e)     
            logger.log_write(logger._error, "[테스트] 오류", error_msg)     
            return False   # 마스터 데이터 유효성 검사 오류 
                
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