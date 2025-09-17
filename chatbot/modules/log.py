# * 파이썬 logging 모듈 사용하여 로그 기록하기 
# 참고 URL - https://docs.python.org/ko/3/library/logging.html
# 참고 2 URL - https://docs.python.org/ko/3/howto/logging.html#basic-logging-tutorial
# 참고 3 URL - https://docs.aws.amazon.com/ko_kr/lambda/latest/dg/python-logging.html
# 참고 4 URL - https://wikidocs.net/84432
# 참고 5 URL - https://wikidocs.net/123324
# 참고 6 URL - https://velog.io/@jeongpar/Python-Logging-%EC%82%AC%EC%9A%A9%EB%B2%95
# 참고 7 URL - https://aoc55.tistory.com/10

# * 파이썬 logging 모듈 사용하여 전역 로그 기능 구현하기 
# 참고 URL - https://chuun92.tistory.com/7
# 참고 2 URL - https://malwareanalysis.tistory.com/527
# 참고 3 URL - https://github.com/sungwook-practice/python_logging_logger.git
# 참고 4 URL - https://velog.io/@qlgks1/python-python-logging-%ED%95%B4%EB%B6%80


# 주의사항 - logging 라이브러리 사용할 경우 따로 싱글톤(singleton) 클래스 구현할 필요없다.
# Logger 자체가 Singleton 패턴 이다. 
# getLogger를 한다고 매번 새로운 instance가 return되는게 아니라 이미 그 이름으로 존재하는 Logger를 return한다.

# Log 싱글톤(singleton) 클래스
# Logger는 Singleton 패턴 이다. 
# getLogger를 한다고 매번 새로운 instance가 return되는게 아니라 이미 그 이름으로 존재하는 Logger를 return한다.
# 참고 URL - https://chuun92.tistory.com/7
# 참고 2 URL - https://malwareanalysis.tistory.com/527
# 참고 3 URL - https://github.com/sungwook-practice/python_logging_logger.git
# 참고 4 URL - https://velog.io/@qlgks1/python-python-logging-%ED%95%B4%EB%B6%80
class Log(object):
    logger = None


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
    
#     ----- def _log_write(self, log_type, log_level, content, botRes):
#         """
#         공통 로그 작성 함수
#         """
#         timestamp = self._get_formatted_time()
#         file_name, function_name, lineno = self._get_caller_info()
#         print(f"[{log_type}] [{log_level}] [{timestamp}] [{file_name} | {function_name} - L{lineno}]: {content} - {botRes}")

#     ----- def log_write(self, log_level, content, botRes):
#         """
#         챗봇 로그 작성
#         """
#         self._log_write("Chatbot", log_level, content, botRes)

#     ----- def openAI_log_write(self, log_level, content, botRes):
#         """
#         OpenAI 로그 작성
#         """
#         self._log_write("OpenAI", log_level, content, botRes)

#     # 싱글톤 인스턴스를 반환하는 팩토리 함수
#     ----- def get_logger():
#         """
#         Logger 싱글톤 인스턴스를 반환하는 팩토리 함수
#         """
#         return Logger()

#     # 기존 함수 호환성을 위한 래퍼 함수들
#     @staticmethod
#     ----- def log_write(log_level, content, botRes):
#         """
#         기존 코드 호환성을 위한 래퍼 함수
#         """
#         logger = Logger()
#         logger.log_write(log_level, content, botRes)

#     @staticmethod
#     ----- def openAI_log_write(log_level, content, botRes):
#         """
#         기존 코드 호환성을 위한 래퍼 함수
#         """
#         logger = Logger()
#         logger.openAI_log_write(log_level, content, botRes)




