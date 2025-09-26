"""
# 로그 레벨 종류 
|   Level   |   Value   |   When to use
|   DEBUG   |     10    | (주로 문제 해결을 할때 필요한) 자세한 정보. - 개발 과정에서 오류 원인 파악하고자 할 때 사용
|   INFO    |     20    | 작업이 정상적으로 작동하고 있다는 메시지. 
|  WARNING  |     30    | 예상하지 못한 일이 발생하거나, 발생 가능한 문제점을 명시. (e.g 'disk space low') 작업은 정상적으로 진행.
|   ERROR   |     40    | 프로그램이 함수를 실행하지 못 할 정도의 심각한 문제.
| CRICTICAL |     50    | 프로그램이 동작할 수 없을 정도의 심각한 문제. 
"""

import inspect
import os         # 함수 log_write 호출한 상위 파일 이름 구해야 해서 패키지 "os" 불러오기
from datetime import datetime
# from enum import Enum 
from zoneinfo import ZoneInfo  # 로그 출력시 대한민국 표준시로 출력하기 위해 패키지 "zoneinfo" 불러오기 

# 로그 레벨
# Enum 열거형 구조체 클래스
# class LogLevel(Enum):
#     DEBUG = 'debug'
#     INFO = 'info'
#     WARNING = 'warning'
#     ERROR = 'error'
#     CRITICAL = 'critical'

# 로그 레벨 작성
_debug = 'DEBUG'
_info = 'INFO'
_warning = 'WARNING'
_error = 'ERROR'
_crictical = 'CRICTICAL'

kst = None   # ZoneInfo 클래스 싱글톤(single) 객체

# 상위 호출자 파일, 함수, 라인 정보 반환
def _get_caller_info():
    frame = inspect.currentframe().f_back.f_back.f_back   # 3단계 위 상위 호출자 의미 (f_back.f_back.f_back)
    file_name = os.path.basename(frame.f_code.co_filename)
    function_name = frame.f_code.co_name
    lineno = frame.f_lineno
    return file_name, function_name, lineno

def _get_formatted_time():
    """
    Description: 현재 날짜 및 시간을 대한민국 표준시 포맷된 문자열로 가져오기

    Parameters: 없음.

    Returns: 
    str: 현재 날짜 및 시간을 대한민국 표준시로 포맷된 문자열 (datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S"))
    """
        
    global kst

    # TODO: 아래 지역변수 time_stamp의 경우 시간의 특성상 계속 변경되어야 하고 현재 시간을 가져와야 하므로 싱글톤(singleton) 객체로 구현 안 함. (2025.09.22 minjae)
    # 참고 URL - https://claude.ai/chat/5418150a-6630-430b-9131-3d71be7246d3
    # time_stamp = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")   # 매번 현재 시간을 새로 생성하여 반환
 
    if None is kst:   # 싱글톤(single) 객체(kst)에 할당된 값이 존재하지 않은 경우
        # TODO: zoneinfo 파이썬 라이브러리 사용하여 로그 출력시 대한민국 표준시로 출력 기능 구현 (2025.06.13 minjae)
        # 참고 URL - https://docs.python.org/ko/3.9/library/zoneinfo.html#module-zoneinfo
        # 참고 2 URL - https://wikidocs.net/236273
        # 참고 3 URL - https://chatgpt.com/c/684b79a8-8c20-8010-9d14-41ab28f12747
        kst = ZoneInfo("Asia/Seoul")   # 대한민국 표준시로 설정할 수 있도록 ZoneInfo 클래스 싱글톤(single) 객체 kst 생성 
        current_frame = inspect.currentframe()   # 현재 실행 중인 프레임 의미
        file_name = os.path.basename(current_frame.f_code.co_filename)
        function_name = current_frame.f_code.co_name
        lineno = current_frame.f_lineno        
        print("[%s] [%s] [%s | %s - L%s]: %s" %(_info, datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S"), file_name, function_name, lineno, "[테스트] ZoneInfo 클래스 싱글톤(single) 객체 kst - 생성 완료!"))   # 매번 현재 시간을 새로 생성하여 반환

    # TODO : 현재 날짜와 시간을 특정 포맷으로 변환하기 구현 (2025.03.27 minjae)
    # 참고 URL - https://wikidocs.net/269063
    return datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")   # 매번 현재 시간을 새로 생성하여 반환   


# 공통 로그 작성 함수 (챗봇, OpenAI)
# 참고 URL - https://chatgpt.com/c/6847d34f-9700-8010-92fb-2d063eff183a
def _test_log_write(log_type, log_level, msg, botRes):
    time_stamp = _get_formatted_time()
    file_name, function_name, lineno = _get_caller_info()
    print("[%s] [%s] [%s] [%s | %s - L%s]: %s - %s" %(log_type, log_level, time_stamp, file_name, function_name, lineno, msg, botRes))


# 아마존 웹서비스(AWS) 람다 함수(Lambda Funtion) 챗봇 로그 작성 
# def log_write(log_level, msg, botRes):
#     _test_log_write("Chatbot", log_level, msg, botRes)   # 챗봇 로그 기록

# 아마존 웹서비스(AWS) 람다 함수(Lambda Funtion) OpenAI 로그 작성 
def openAI_log_write(log_level, msg, botRes):
    _test_log_write("OpenAI", log_level, msg, botRes)   # OpenAI 로그 기록


def _log_write(log_level, msg):
    """
    Description: 레벨별 로그 기록 출력 

    Parameters: 
    log_level (str): 로그 레벨
    msg (str): 로그 메시지

    Returns: 없음.
    """

    time_stamp = _get_formatted_time()
    file_name, function_name, lineno = _get_caller_info()
    print("[%s] [%s] [%s | %s - L%s]: %s" %(log_level, time_stamp, file_name, function_name, lineno, msg))


# TODO: 아래처럼 오류 메시지 발생하여 print 함수 호출문 전달인자 수정 (2025.09.19 minjae) 
# 오류 메시지: [ERROR] TypeError: not enough arguments for format string Traceback (most recent call last):
# (기존) print("[%s] [%s] [%s | %s - L%s]: %s - %s" %(_debug, time_stamp, file_name, function_name, lineno, msg))
# (변경) print("[%s] [%s] [%s | %s - L%s]: %s" %(_debug, time_stamp, file_name, function_name, lineno, msg))
def debug(msg):
    _log_write(_debug, msg)
    # time_stamp = _get_formatted_time()
    # file_name, function_name, lineno = _get_caller_info()
    # print("[%s] [%s] [%s | %s - L%s]: %s" %(_debug, time_stamp, file_name, function_name, lineno, msg))

def info(msg):
    _log_write(_info, msg)
    # time_stamp = _get_formatted_time()
    # file_name, function_name, lineno = _get_caller_info()
    # print("[%s] [%s] [%s | %s - L%s]: %s" %(_info, time_stamp, file_name, function_name, lineno, msg))

def warning(msg):
    _log_write(_warning, msg)
    # time_stamp = _get_formatted_time()
    # file_name, function_name, lineno = _get_caller_info()
    # print("[%s] [%s] [%s | %s - L%s]: %s" %(_warning, time_stamp, file_name, function_name, lineno, msg))

def error(msg):
    _log_write(_error, msg)
    # time_stamp = _get_formatted_time()
    # file_name, function_name, lineno = _get_caller_info()
    # print("[%s] [%s] [%s | %s - L%s]: %s" %(_error, time_stamp, file_name, function_name, lineno, msg))

def crictical(msg):
    _log_write(_crictical, msg)
    # time_stamp = _get_formatted_time()
    # file_name, function_name, lineno = _get_caller_info()
    # print("[%s] [%s] [%s | %s - L%s]: %s" %(_crictical, time_stamp, file_name, function_name, lineno, msg))


# 상위 호출자 파일, 함수, 라인 정보 반환
# def _get_caller_info():
#     # 현재 함수 log_write 호출하는 상위 파일명 가져오기 
#     # 참고 URL - https://docs.python.org/ko/3.8/library/inspect.html
# 	# 참고 2 URL - https://louky0714.tistory.com/144
#     # 참고 3 URL - https://wikidocs.net/3717
#     current_filepath = inspect.currentframe().f_back.f_code.co_filename
#     current_filename = os.path.basename(current_filepath)

#     # 현재 함수 log_write 호출하는 상위 함수명 가져오기
#     # 참고 URL - https://docs.python.org/ko/3.8/library/inspect.html
#     # 참고 2 URL - https://louky0714.tistory.com/144    
#     current_function_name = inspect.currentframe().f_back.f_code.co_name

#     # 현재 함수 log_write 호출하는 상위 파일 라인번호(라인위치) 가져오기 
#     # 참고 URL - https://docs.python.org/ko/3.8/library/inspect.html
#     current_lineno = inspect.currentframe().f_back.f_lineno

#     return current_filename, current_function_name, current_lineno