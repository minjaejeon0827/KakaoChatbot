from enum import Enum    # Enum 열거형 구조체

class EnumValidator(Enum):   # 명시적으로 Enum 클래스 상속
    """
    Description: 데이터 유효성 검사 Enum 열거형 구조체 클래스
                 참고 URL - https://docs.python.org/ko/3.9/library/enum.html#functional-api
                 참고 2 URL - https://wikidocs.net/105486

    Attributes: DATA_TYPE_MISMATCH (int) - 데이터 타입 불일치 (default: -2)
                VALIDATION_ERROR (int) - 데이터 유효성 검사 오류 (default: -1)
                NOT_EXISTENCE (int) - 데이터 존재 안 함. (default: 0)
                EXISTENCE (int) - 데이터 존재함. (default: 1)
    """
    DATA_TYPE_MISMATCH = -2   # 필요시 사용 예정
    VALIDATION_ERROR = -1
    NOT_EXISTENCE = 0
    EXISTENCE = 1

    @classmethod
    def to_str(_class, value) -> str:
        """
        Description: Enum 열거형 구조체 멤버변수 값을 사람이 읽기 쉬운 문자열로 변환

        Parameters: _class - 데이터 유효성 검사 Enum 열거형 구조체 클래스 (EnumValidator)
                    value - Enum 열거형 구조체 멤버변수 값

        Returns: 데이터 존재 여부 문자열 
        """
        
        return "데이터 존재함." if value == _class.EXISTENCE else "데이터 존재 안 함."