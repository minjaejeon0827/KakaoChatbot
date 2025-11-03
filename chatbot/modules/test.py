from modules import chatbot_logger

def _testDebug(msg: str) -> None:
    """
    Description: 로그 테스트 함수

    Parameters: 
        msg (str): 로그 메시지

    Returns: 없음.
    """
    chatbot_logger.debug(msg)