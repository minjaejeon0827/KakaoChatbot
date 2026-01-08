"""
* 아마존 웹서비스 람다 함수 (AWS Lambda Function) -> 임시 로그 텍스트 파일 처리 유틸 (util)
코드 리뷰 참고 URL - https://chatgpt.com/c/691e9f6e-3940-832a-afda-92c53ae4b49a
"""

from utils.log import logger   # 챗봇 전역 로그 객체 (logger)

import os                      # 폴더/파일 처리

def create_tmp_file(file_path: str) -> None:
    """
    Description: 임시 로그 텍스트 파일 없으면 새로 생성

    Parameters: file_path - 임시 로그 텍스트 파일 상대 경로 - (예시) '/tmp/user_id-1b2bfc8caf85a5dff8fadd1bf4cc70125b533fea7b665d0cdb0fb493a135e94b4d_chatbot.txt'

    Returns: 없음.
    """

    dir_name = None   # 해당 파일 상위 폴더 경로

    try:
        dir_name = os.path.dirname(file_path)

        if dir_name and False == os.path.exists(dir_name):   # 해당 폴더 존재하지 않는 경우
            os.makedirs(dir_name, exist_ok=True)   # 폴더 생성 / exist_ok=True - 이미 만드려는 폴더가 존재할 경우 exist_ok 인수 사용해서 건너뛰기
            
        if False == os.path.exists(file_path):   # 해당 파일 존재하지 않는 경우
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("")
            logger.info(f"[테스트] 임시 로그 텍스트 파일 생성 완료: {file_path}")
        else: logger.info(f"[테스트] 임시 로그 텍스트 파일 존재함! file_path - {file_path}")

    except Exception as e:
        logger.critical(f"[테스트] 시스템 오류 - {str(e)}", exc_info=True)
        raise

def write_tmp_file(file_path: str, msg: str) -> None:
    """
    Description: 임시 로그 기록

    Parameters: file_path - 임시 로그 텍스트 파일 상대 경로 - (예시) '/tmp/user_id-1b2bfc8caf85a5dff8fadd1bf4cc70125b533fea7b665d0cdb0fb493a135e94b4d_chatbot.txt'
                msg - 로그 메시지

    Returns: 없음.
    """

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            logger.info(f"[테스트] 임시 로그 텍스트 파일 file_path - ({file_path}) / 로그 메시지 기록 - {msg}")
            f.write(msg)
    except Exception as e:
        logger.critical(f"[테스트] 시스템 오류 - {str(e)}", exc_info=True)
        raise

def read_tmp_file(file_path: str) -> str:
    """
    Description: 임시 로그 읽기

    Parameters: file_path - 임시 로그 텍스트 파일 상대 경로 - (예시) '/tmp/user_id-1b2bfc8caf85a5dff8fadd1bf4cc70125b533fea7b665d0cdb0fb493a135e94b4d_chatbot.txt' 

    Returns: 없음.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        logger.error(f"[테스트] 파일 찾기 오류 - {str(e)}", exc_info=True)
        return ""
    except Exception as e:
        logger.critical(f"[테스트] 시스템 오류 - {str(e)}", exc_info=True)
        return ""

"""
*** 참고 ***
*** 파이썬 문서 ***
* Type Hints
참고 URL - https://docs.python.org/ko/3.14/library/typing.html
참고 2 URL - https://peps.python.org/pep-0484/
참고 3 URL - https://devpouch.tistory.com/189
참고 4 URL - https://supermemi.tistory.com/entry/Python-3-%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%97%90%EC%84%9C-%EC%9D%98%EB%AF%B8%EB%8A%94-%EB%AC%B4%EC%97%87%EC%9D%BC%EA%B9%8C-%EC%A3%BC%EC%84%9D

* Type Hints class Any
참고 URL - https://docs.python.org/ko/3.9/library/typing.html#the-any-type

* Union Type
참고 URL - https://docs.python.org/ko/3.11/library/stdtypes.html#types-union

* non-default value parameter (필수 매개변수), default value parameter (기본값 매개변수)
non-default value parameter - 함수를 호출할 때 반드시 값을 전달해야 하는 매개변수
default value parameter - 함수를 호출할 때 값을 전달하지 않으면 미리 설정된 기본값을 사용하는 매개변수
참고 URL - https://docs.python.org/ko/3/glossary.html#term-parameter
참고 2 URL - https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects
참고 3 URL - https://fierycoding.tistory.com/58
참고 4 URL - https://claude.ai/chat/e9803e84-1f2c-4fff-9f22-3603392000ad

* ValueError
참고 URL - https://docs.python.org/ko/3.13/library/exceptions.html#ValueError

* raise ValueError()
참고 URL - https://docs.python.org/ko/3/tutorial/errors.html#raising-exceptions

* os
참고 URL - https://docs.python.org/3/library/os.html

* open
참고 URL - https://docs.python.org/ko/3.13/library/functions.html#open
"""