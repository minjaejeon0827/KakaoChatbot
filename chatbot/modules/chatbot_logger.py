"""
* 챗봇 커스텀 로그 기록 모듈
"""

# 1. 공통 모듈 먼저 import 처리
from commons import chatbot_helper   # 챗봇 전용 도움말 텍스트

# 2. 나머지 모듈 import 처리
import inspect
import os   # 상위 호출자 파일 이름 구하는 용도
from datetime import datetime
from zoneinfo import ZoneInfo    # 대한민국 표준시 포맷 변환 용도

"""
* 로그 레벨 종류 
|   Level   |   Value   |   When to use
|   DEBUG   |     10    | (주로 문제 해결을 할때 필요한) 자세한 정보. - 개발 과정에서 오류 원인 파악하고자 할 때 사용
|   INFO    |     20    | 작업이 정상적으로 작동하고 있다는 메시지. 
|  WARNING  |     30    | 예상하지 못한 일이 발생하거나, 발생 가능한 문제점을 명시. (e.g 'disk space low') 작업은 정상적으로 진행.
|   ERROR   |     40    | 프로그램이 함수를 실행하지 못 할 정도의 심각한 문제.
| CRICTICAL |     50    | 프로그램이 동작할 수 없을 정도의 심각한 문제. 
""" 

_debug = 'DEBUG'
_info = 'INFO'
_warning = 'WARNING'
_error = 'ERROR'
_crictical = 'CRICTICAL'

kst = None   # ZoneInfo 클래스 전역변수(global) 객체 (시간대는 변경되지 않으므로)

def _callerInfo():
    """
    Description: 상위 호출자 파일 이름 (file_name), 함수 이름 (function_name), 라인 번호 (lineno) 가져오기

    Parameters: 없음.

    Returns: 
        file_name (str): 상위 호출자 파일 이름
        function_name (str): 함수 이름

        lineno (int): 라인 번호
    """

    # 상위 호출자 파일명 가져오기 
    # 참고 URL - https://docs.python.org/ko/3.8/library/inspect.html
    # 참고 2 URL - https://louky0714.tistory.com/144
    # 참고 3 URL - https://wikidocs.net/3717    
    frame = inspect.currentframe().f_back.f_back.f_back   # 3단계 위 상위 호출자 정보 가져오기
    file_name = os.path.basename(frame.f_code.co_filename)
    function_name = frame.f_code.co_name
    lineno = frame.f_lineno

    return file_name, function_name, lineno

def _formatTime():
    """
    Description: 현재 날짜 및 시간을 대한민국 표준시 포맷된 문자열로 가져오기

    Parameters: 없음.

    Returns: 
        datetime.now(kst).strftime(chatbot_helper._datefmt) (str): 현재 날짜 및 시간을 대한민국 표준시로 포맷된 문자열
    """
        
    global kst
 
    if None is kst:   # 전역변수(global) 객체(kst)에 할당된 값이 존재하지 않은 경우
        # zoneinfo 파이썬 라이브러리 사용하여 로그 출력시 대한민국 표준시로 출력 기능 구현 (2025.06.13 minjae)
        # 참고 URL - https://docs.python.org/ko/3.9/library/zoneinfo.html#module-zoneinfo
        # 참고 2 URL - https://wikidocs.net/236273
        # 참고 3 URL - https://chatgpt.com/c/684b79a8-8c20-8010-9d14-41ab28f12747
        kst = ZoneInfo("Asia/Seoul")   # 대한민국 표준시로 설정할 수 있도록 ZoneInfo 클래스 전역변수(global) 객체 kst 생성 
        current_frame = inspect.currentframe()   # 현재 실행 중인 프레임 의미
        file_name = os.path.basename(current_frame.f_code.co_filename)
        function_name = current_frame.f_code.co_name
        lineno = current_frame.f_lineno        
        print("[%s] [%s] [%s | %s - L%s]: %s" %(_info, datetime.now(kst).strftime(chatbot_helper._datefmt), file_name, function_name, lineno, "[테스트] ZoneInfo 클래스 전역변수(global) 객체 kst - 생성 완료!"))   # 현재 시간 새로 생성 및 반환

    # 현재 날짜와 시간을 특정 포맷으로 변환하기 구현 (2025.03.27 minjae)
    # 참고 URL - https://wikidocs.net/269063
    return datetime.now(kst).strftime(chatbot_helper._datefmt)   # 매번 현재 시간 새로 생성 및 반환 
 
def _log_write(log_level, msg):
    """
    Description: 
        레벨별 로그 기록 출력 
        공통 로그 출력 함수 기능 구현 (2025.09.22 minjae) 
        참고 URL - https://chatgpt.com/c/6847d34f-9700-8010-92fb-2d063eff183a

    Parameters: 
        log_level (str): 로그 레벨
        msg (str): 로그 메시지

    Returns: 없음.
    """

    time_stamp = _formatTime()
    file_name, function_name, lineno = _callerInfo()
    print("[%s] [%s] [%s | %s - L%s]: %s" %(log_level, time_stamp, file_name, function_name, lineno, msg))

def debug(msg):
    """
    Description: DEBUG 로그 기록 출력 

    Parameters: 
        msg (str): 로그 메시지 

    Returns: 없음.     
    """

    _log_write(_debug, msg)

def info(msg):
    """
    Description: INFO 로그 기록 출력

    Parameters: 
        msg (str): 로그 메시지

    Returns: 없음.
    """

    _log_write(_info, msg)

def warning(msg):
    """
    Description: WARNING 로그 기록 출력

    Parameters: 
        msg (str): 로그 메시지

    Returns: 없음.
    """

    _log_write(_warning, msg)

def error(msg):
    """
    Description: ERROR 로그 기록 출력

    Parameters: 
        msg (str): 로그 메시지

    Returns: 없음.
    """

    _log_write(_error, msg)

def crictical(msg):
    """
    Description: CRICTICAL 로그 기록 출력

    Parameters: 
        msg (str): 로그 메시지

    Returns: 없음.
    """

    _log_write(_crictical, msg)