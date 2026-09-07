"""
* 챗봇 커스텀 로거 유틸 (util)
코드 리뷰 참고 URL - https://chatgpt.com/c/68f9886c-6080-8320-9657-836cde5674f8
"""

# 1. 먼저 공통 모듈 (module) import
from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트

# 2. 나머지 모듈 (module) import 
import inspect
import os   # 상위 호출자 파일명 구하는 용도
from datetime import datetime
from zoneinfo import ZoneInfo    # 대한민국 표준시 포맷 변환 용도

"""
* 로그 레벨 종류 
|   Level   |   Value   |   When to use
|   DEBUG   |     10    | (주로 문제 해결을 할때 필요한) 자세한 정보. - 개발 과정에서 오류 원인 파악하고자 할 때 사용
|   INFO    |     20    | 작업이 정상적으로 작동하고 있다는 메시지. 
|  WARNING  |     30    | 예상하지 못한 일이 발생하거나, 발생 가능한 문제점을 명시. (e.g 'disk space low') 작업은 정상적으로 진행.
|   ERROR   |     40    | 프로그램이 함수를 실행하지 못 할 정도의 심각한 문제.
|  CRITICAL |     50    | 프로그램이 동작할 수 없을 정도의 심각한 문제. 
""" 

DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'
ERROR = 'ERROR'
CRITICAL = 'CRITICAL'

_kst = None   # ZoneInfo 클래스 전역변수 객체 (global) 

def _initZoneInfo() -> None:
    """
    Description: ZoneInfo 클래스 전역변수 객체 (global) _kst 초기화 (1회만 실행)
                 한국 표준 시간대 ("Asia/Seoul") 변경되지 않기 때문에 1회만 실행.

    Parameters: 없음.

    Returns: 없음.
    """

    global _kst
 
    if None is _kst:   # 전역변수 객체 (global) _kst 할당된 값이 존재하지 않은 경우
        # zoneinfo 파이썬 라이브러리 사용하여 로그 출력시 대한민국 표준시로 출력 (2025.06.13 minjae)
        # 참고 URL - https://docs.python.org/ko/3.9/library/zoneinfo.html#module-zoneinfo
        # 참고 2 URL - https://wikidocs.net/236273
        # 참고 3 URL - https://chatgpt.com/c/684b79a8-8c20-8010-9d14-41ab28f12747
        _kst = ZoneInfo("Asia/Seoul")   # 대한민국 표준시로 설정할 수 있도록 ZoneInfo 클래스 전역변수 객체 (global) _kst 생성
        current_frame = inspect.currentframe()   # 현재 실행 중인 프레임 의미
        file_name = os.path.basename(current_frame.f_code.co_filename)
        function_name = current_frame.f_code.co_name
        lineno = current_frame.f_lineno        
        print("[%s] [%s] [%s | %s - L%d]: %s" %(INFO, datetime.now(_kst).strftime(chatbot_helper._datefmt), file_name, function_name, lineno, "[테스트] ZoneInfo 클래스 전역변수 객체 (global) _kst - 생성 완료!"))   # 현재 시간 새로 생성 및 반환

def _callerInfo() -> tuple[str, str, int]:
    """
    Description: 상위 호출자 파일명 (file_name), 함수명 (function_name), 라인 번호 (lineno) 가져오기
                 튜플 (tuple) 객체 사용하여 값 반환
                 참고 URL - https://dojang.io/mod/page/view.php?id=2340
                 참고 2 URL - https://wikidocs.net/3133
                 참고 3 URL - https://wikidocs.net/92538

    Parameters: 없음.

    Returns: file_name - 상위 호출자 파일명
             function_name - 함수명
             lineno - 라인 번호
    """

    # 상위 호출자 파일명, 함수명, 라인 번호 가져오기
    # 참고 URL - https://docs.python.org/ko/3.8/library/inspect.html
    # 참고 2 URL - https://louky0714.tistory.com/144
    # 참고 3 URL - https://wikidocs.net/3717
    # 참고 4 URL - https://visit-my.blog/2024/02/11/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%98%84%EC%9E%AC-%ED%95%A8%EC%88%98-%EC%9D%B4%EB%A6%84%EA%B3%BC-%ED%98%B8%EC%B6%9C%ED%95%9C-%ED%95%A8%EC%88%98-%EC%9D%B4%EB%A6%84-%ED%99%95%EC%9D%B8-%ED%95%98%EA%B8%B0/
    # 참고 5 URL - https://dev.to/atifwattoo/inspectstack-in-python-with-examples-l4m
    # frame = inspect.currentframe().f_back.f_back.f_back   # 3단계 위 상위 호출자 정보 가져오기
    stack = inspect.stack()   # 현재 stack 전체 가져오기

    # stack 구조 예시 (인덱스 번호 기준): [3]번째 프레임이 상위 호출자이다.
    # stack[0] _callerInfo
    # stack[1] _logWrite
    # stack[2] debug / info / warning / error / critical
    # stack[3] [2]번 함수들을 직접 호출한 상위 호출자

    # 그리디 알고리즘 (Greedy Algorithm) - 탐욕법이라고 불리며, 현재 상황에서 지금 당장 좋은 것만 고르는 방법이다.
    # 참고 URL - https://youtu.be/5OYlS2QQMPA?si=LzCRpZvGmEXI5Ean
    # 참고 2 URL - https://youtu.be/_TG0hVYJ6D8?si=j85mnzUabJeClsoQ

    for frame_info in stack:   # 호출 stack 역순으로 순회 및 chatbot_logger.py 모듈 (module) 밖 상위 호출자 자동 탐색.
        module = inspect.getmodule(frame_info.frame)   # 해당 프레임 객체가 (frame_info.frame) 어느 모듈 (module)에서 생성되었는지 추적
        file_name = os.path.basename(frame_info.filename)   # 상위 호출자 함수가 속한 파일 이름
        cur_file_name = os.path.basename(__file__)   # 현재 실행 중인 함수 (_callerInfo) 코드가 속한 파일 이름 변수 (속성 - Attribute) (chatbot_logger.py)

        # [테스트] [오류 케이스] chatbot_logger.py 모듈 (module) 밖 상위 호출자 찾기 불가!
        # module = None
        # cur_file_name = os.path.basename(__file__)   # 현재 실행 중인 함수 (_callerInfo) 코드가 속한 파일 이름 변수 (속성 - Attribute) (chatbot_logger.py)
        # file_name = cur_file_name  # 상위 호출자 함수가 속한 파일 이름 == 현재 실행 중인 함수 (_callerInfo) 코드가 속한 파일 이름
        
        # 파이썬 __name__ 변수 (속성 - Attribute) - 현재 모듈 (module)의 이름을 담고 있는 내장 변수 (속성 - Attribute)
        # 참고 URL - https://docs.python.org/ko/3.7/reference/import.html?highlight=__name__#__name__
        # 참고 2 URL - https://wikidocs.net/195615
        
        # ***** 핵심 조건 *****
        # (1) module 값 존재하고 module 이름 (module.__name__) chatbot_logger 아님
        # (2) module 값 None 이고 파일명 chatbot_logger.py 아님
        if (module and module.__name__ != __name__) or (None is module and file_name != cur_file_name):   # chatbot_logger.py 내부 호출 건너띄기.
            return (
                file_name,
                frame_info.function,
                frame_info.lineno
            )

    return ("unknown_file", "unknown_function", -1)  # chatbot_logger.py 모듈 (module) 밖 상위 호출자 찾기 불가!

def _formatTime() -> str:
    """
    Description: 현재 날짜 및 시간을 대한민국 표준시 포맷된 문자열로 가져오기

    Parameters: 없음.

    Returns: datetime.now(_kst).strftime(chatbot_helper._datefmt) - 현재 날짜 및 시간을 대한민국 표준시로 포맷된 문자열
    """
        
    global _kst

    _initZoneInfo()
 
    # 현재 날짜와 시간을 특정 포맷으로 변환 (2025.03.27 minjae)
    # 참고 URL - https://wikidocs.net/269063
    return datetime.now(_kst).strftime(chatbot_helper._datefmt)   # 매번 현재 시간 새로 생성 및 반환
 
def _logWrite(level: str, msg: str) -> None:
    """
    Description: 레벨별 공통 로그 기록 출력
                 공통 로그 출력 함수 기능 구현 (2025.09.22 minjae)
                 참고 URL - https://chatgpt.com/c/6847d34f-9700-8010-92fb-2d063eff183a

    Parameters: level - 로그 레벨
                msg - 로그 메시지

    Returns: 없음.
    """

    time_stamp = _formatTime()
    (file_name, function_name, lineno) = _callerInfo()

    # 파이썬 문자열 포맷팅 (String Formatting)
    # 참고 URL - https://docs.python.org/ko/3/library/string.html#format-string-syntax
    # 참고 2 URL - https://wikidocs.net/78952
    # 참고 3 URL - https://wikidocs.net/13
    # 참고 4 URL - https://dojang.io/mod/page/view.php?id=2300
    # TODO: 오류 메시지 "/var/task/modules/chatbot_logger.py:170: SyntaxWarning: "is" with a literal. Did you mean "=="?" 출력되어 (기존) is 연산자 -> (변경) == 연산자 처리 완료 (2025.10.27 minjae)
    # if "unknown_file" is file_name or "unknown_function" is function_name or -1 is lineno:   # 상위 호출자 존재 안 하는 경우
    if "unknown_file" == file_name or "unknown_function" == function_name or -1 == lineno:   # 상위 호출자 존재 안 하는 경우
        print("[%s] [%s] [%s | %s - L(%d)]: %s" %(level, time_stamp, file_name, function_name, lineno, 'chatbot_logger.py 모듈 (module) 밖 상위 호출자 찾기 불가!'))
    else:   # 상위 호출자 존재 하는 경우
        print("[%s] [%s] [%s | %s - L%d]: %s" %(level, time_stamp, file_name, function_name, lineno, msg))

def debug(msg: str) -> None:
    """
    Description: DEBUG 로그 기록 출력

    Parameters: msg - 로그 메시지

    Returns: 없음.
    """

    _logWrite(DEBUG, msg)

def info(msg: str) -> None:
    """
    Description: INFO 로그 기록 출력

    Parameters: msg - 로그 메시지

    Returns: 없음.
    """

    _logWrite(INFO, msg)

def warning(msg: str) -> None:
    """
    Description: WARNING 로그 기록 출력

    Parameters: msg - 로그 메시지

    Returns: 없음.
    """

    _logWrite(WARNING, msg)

def error(msg: str) -> None:
    """
    Description: ERROR 로그 기록 출력

    Parameters: msg - 로그 메시지

    Returns: 없음.
    """

    _logWrite(ERROR, msg)

def critical(msg: str) -> None:
    """
    Description: CRITICAL 로그 기록 출력

    Parameters: msg - 로그 메시지

    Returns: 없음.
    """

    _logWrite(CRITICAL, msg)

"""
*** 참고 ***
*** 파이썬 문서 ***
* Type Hints
참고 URL - https://docs.python.org/ko/3.14/library/typing.html
참고 2 URL - https://peps.python.org/pep-0484/
참고 3 URL - https://devpouch.tistory.com/189
참고 4 URL - https://supermemi.tistory.com/entry/Python-3-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-%EC%9D%98%EB%AF%B8%EB%8A%94-%EB%AC%B4%EC%97%87%EC%9D%BC%EA%B9%8C-%EC%A3%BC%EC%84%9D

* 패키지, 모듈 (module)
참고 URL - https://docs.python.org/ko/3.13/tutorial/modules.html
참고 2 URL - https://wikidocs.net/1418
참고 3 URL - https://dojang.io/mod/page/view.php?id=2450
"""