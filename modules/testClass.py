"""
* 테스트 클래스 구현 모듈 (module)

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

* 4. 패키지 (package), 모듈 (module)
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

# 9. 클래스

# 9.3. 클래스와의 첫 만남
# 9.3.1. 클래스 정의 문법
# class ClassName:
#     <statement-1>
#     .
#     .
#     .
#     <statement-N>

# 9.3.2. 클래스 객체
# class MyClass:
#     """A simple example class"""
#     i = 12345

#     def __init__(self):
#         self.data = []

#     def f(self):
#         return 'hello world'

# x = MyClass()

# class Complex:
#     def __init__(self, realpart, imagpart):
#         self.r = realpart
#         self.i = imagpart

# x = Complex(3.0, -4.5)
# print(x.r, x.i)

# 9.3.3. 인스턴스 객체
# x.counter = 1
# while x.counter < 10:
#     x.counter = x.counter * 2
# print(x.counter)
# del x.counter

# 9.3.4. 메서드 객체
# x.f()

# xf = x.f
# while True:
#     print(xf())

# 9.3.5. 클래스와 인스턴스 변수
# class Dog:

#     kind = 'canine'         # 모든 인스턴스가 공유하는 클래스 변수

#     def __init__(self, name):
#         self.name = name    # 각 인스턴스에 고유한 인스턴스 변수

# d = Dog('Fido')
# e = Dog('Buddy')
# print(d.kind)                  # 모든 인스턴스가 공유하는 변수
# 'canine'
# print(e.kind)                  # 모든 인스턴스가 공유하는 변수
# 'canine'
# print(d.name)                  # d 만의 변수
# 'Fido'
# print(e.name)                  # e 만의 변수
# 'Buddy'

# case: 클래스 잘못된 설계 예시
# class Dog:

#     tricks = []             # 클래스 변수의 잘못된 사용

#     def __init__(self, name):
#         self.name = name

#     def add_trick(self, trick):
#         self.tricks.append(trick)

# d = Dog('Fido')
# e = Dog('Buddy')
# d.add_trick('roll over')
# e.add_trick('play dead')
# d.tricks                # 예기치 않게 모든 인스턴스가 공유합니다
# ['roll over', 'play dead']

# case: 클래스 올바른 설계 예시
# class Dog:

#     def __init__(self, name):
#         self.name = name
#         self.tricks = []    # 각 인스턴스마다 새 빈 리스트를 만듭니다

#     def add_trick(self, trick):
#         self.tricks.append(trick)

# d = Dog('Fido')
# e = Dog('Buddy')
# d.add_trick('roll over')
# e.add_trick('play dead')
# print(d.tricks)
# ['roll over']
# print(e.tricks)
# ['play dead']

# 9.4. 기타 주의사항들
# class Warehouse:
#    purpose = 'storage'
#    region = 'west'

# w1 = Warehouse()
# print(w1.purpose, w1.region)
# storage west
# w2 = Warehouse()
# w2.region = 'east'
# print(w2.purpose, w2.region)
# storage east

# 클래스 외부에서 정의된 함수
# def f1(self, x, y):
#     return min(x, x+y)

# class C:
#     f = f1

#     def g(self):
#         return 'hello world'

#     h = g

# class Bag:
#     def __init__(self):
#         self.data = []

#     def add(self, x):
#         self.data.append(x)

#     def addtwice(self, x):
#         self.add(x)
#         self.add(x)

# 9.5. 상속
# class DerivedClassName(BaseClassName):
#     <statement-1>
#     .
#     .
#     .
#     <statement-N>

# 이름 BaseClassName 은 파생 클래스 정의를 포함하는 스코프에서 접근할 수 있는 이름 공간에 정의되어 있어야 합니다. 
# 베이스 클래스(부모 클래스) 이름의 자리에 다른 임의의 표현식도 허락됩니다. 
# 예를 들어, 베이스 클래스(부모 클래스)가 다른 모듈에 정의되어 있을 때 유용합니다:
# case: 베이스 클래스(부모 클래스)(BaseClassName)가 다른 모듈(modname)에 설계된 경우 해당 베이스 클래스(부모 클래스) 상속 받는 예시
# class DerivedClassName(modname.BaseClassName):

# 9.5.1. 다중 상속
# 파이썬은 다중 상속의 형태도 지원합니다. 여러 개의 베이스 클래스(부모 클래스)를 갖는 클래스 정의는 이런 식입니다:
# class DerivedClassName(Base1, Base2, Base3):
#     <statement-1>
#     .
#     .
#     .
#     <statement-N>

# 9.6. 비공개 변수
# 객체 내부에서만 액세스할 수 있는 “비공개” 인스턴스 변수는 파이썬에 존재하지 않습니다. 
# 하지만, 대부분의 파이썬 코드에서 따르고 있는 규약이 있습니다: 
# 밑줄로 시작하는 이름은 (예를 들어, _spam) API의 공개적이지 않은 부분으로 취급되어야 합니다 
# (그것이 함수, 메서드, 데이터 멤버중 무엇이건 간에). 구현 상세이고 통보 없이 변경되는 대상으로 취급되어야 합니다.
# 클래스-비공개 멤버들의 올바른 사례가 있으므로 (즉 서브 클래스에서 정의된 이름들과의 충돌을 피하고자), 이름 뒤섞기 (name mangling) 라고 불리는 메커니즘에 대한 제한된 지원이 있습니다. 
# __spam 형태의 (최소 두 개의 밑줄로 시작하고, 최대 한 개의 밑줄로 끝납니다) 모든 식별자는 _classname__spam 로 텍스트 적으로 치환되는데, classname 은 현재 클래스 이름에서 앞에 오는 밑줄을 제거한 것입니다. 
# 이 뒤섞기는 클래스 정의에 등장하는 이상, 식별자의 문법적 위치와 무관하게 수행됩니다.

# class Mapping:
#     def __init__(self, iterable):
#         self.items_list = []
#         self.__update(iterable)

#     def update(self, iterable):
#         for item in iterable:
#             self.items_list.append(item)

#     __update = update   # 기존 update() 메서드의 비공개 사본

# class MappingSubclass(Mapping):

#     def update(self, keys, values):
#         # update() 에 새로운 서명을 제공하지만
#         # __init__() 를 망가뜨리진 않습니다
#         for item in zip(keys, values):
#             self.items_list.append(item)

# 9.7. 잡동사니
# 때로 몇몇 이름 붙은 데이터 항목들을 함께 묶어주는 파스칼의 “record” 나 C의 “struct” 와 유사한 데이터형을 갖는 것이 쓸모 있습니다. 
# 이 경우 dataclasses를 사용하는 것이 일반적인 방법입니다:
# from dataclasses import dataclass

# @dataclass
# class Employee:
#     name: str
#     dept: str
#     salary: int

# john = Employee('john', 'computer lab', 1000)
# print(john.dept)
# 'computer lab'
# print(john.salary)
# 1000

# 9.8. 이터레이터
# for element in [1, 2, 3]:
#     print(element)
# for element in (1, 2, 3):
#     print(element)
# for key in {'one':1, 'two':2}:
#     print(key)
# for char in "123":
#     print(char)
# for line in open("myfile.txt"):
#     print(line, end='')

# s = 'abc'
# it = iter(s)
# it
# <str_iterator object at 0x10c90e650>
# next(it)
# 'a'
# next(it)
# 'b'
# next(it)
# 'c'
# next(it)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#     next(it)
# StopIteration

# class Reverse:
#     """시퀀스를 역순으로 이터레이트하는 이터레이터."""
#     def __init__(self, data):
#         self.data = data
#         self.index = len(data)

#     def __iter__(self):
#         return self

#     def __next__(self):
#         if self.index == 0:
#             raise StopIteration
#         self.index = self.index - 1
#         return self.data[self.index]
    
# rev = Reverse('spam')
# iter(rev)
# <__main__.Reverse object at 0x00A1DB50>
# for char in rev:
#     print(char)
# m
# a
# p
# s

# 9.9. 제너레이터
# def reverse(data):
#     for index in range(len(data)-1, -1, -1):
#         yield data[index]

# for char in reverse('golf'):
#     print(char)
# f
# l
# o
# g

# 9.10. 제너레이터 표현식
# sum(i*i for i in range(10))                 # 제곱의 합
# 285

# xvec = [10, 20, 30]
# yvec = [7, 5, 3]
# sum(x*y for x,y in zip(xvec, yvec))         # 내적
# 260

# unique_words = set(word for line in page  for word in line.split())

# valedictorian = max((student.gpa, student.name) for student in graduates)

# data = 'golf'
# list(data[i] for i in range(len(data)-1, -1, -1))
# ['f', 'l', 'o', 'g']

# 1. 클래스는 왜 필요한가?
#     1. 계산기 프로그램을 만들며 클래스 알아보기
# 2. 클래스와 객체
# 3. 사칙 연산 클래스 만들기
#     1. 클래스를 어떻게 만들지 먼저 구상하기
#     2. 클래스 구조 만들기
#     3. 객체에 연산할 숫자 지정하기
#     4. 더하기 기능 만들기
#     5. 곱하기, 빼기, 나누기 기능 만들기
# 4. 생성자
# 5. 클래스의 상속
# 6. 메서드 오버라이딩
# 7. 클래스변수

# 1. 클래스는 왜 필요한가?
#     1. 계산기 프로그램을 만들며 클래스 알아보기

# calculator.py
# result = 0

# def add(num):
#     global result
#     result += num  # 결괏값(result)에 입력값(num) 더하기
#     return result  # 결괏값 리턴

# print(add(3))
# print(add(4))
# 출력 결과
# 3
# 7

# calculator2.py
# result1 = 0
# result2 = 0

# def add1(num):  # 계산기1
#     global result1
#     result1 += num
#     return result1

# def add2(num):  # 계산기2
#     global result2
#     result2 += num
#     return result2

# print(add1(3))
# print(add1(4))
# print(add2(3))
# print(add2(7))
# 출력 결과
# 3
# 7
# 3
# 10

# calculator3.py
# class Calculator:
#     def __init__(self):
#         self.result = 0

#     def add(self, num):
#         self.result += num
#         return self.result

# cal1 = Calculator()
# cal2 = Calculator()

# print(cal1.add(3))
# print(cal1.add(4))
# print(cal2.add(3))
# print(cal2.add(7))
# 출력 결과
# 3
# 7
# 3
# 10

# class Calculator:
#     def __init__(self):
#         self.result = 0

#     def add(self, num):
#         self.result += num
#         return self.result

#     def sub(self, num):
#         self.result -= num
#         return self.result

# 2. 클래스와 객체
# class Cookie:
#     pass

# a = Cookie()
# b = Cookie()

# 3. 사칙 연산 클래스 만들기
#     1. 클래스를 어떻게 만들지 먼저 구상하기
# a = FourCal()
# a.setdata(4, 2)
# a.add()
# 출력 결과
# 6
# a.mul()
# 출력 결과
# 8
# a.sub()
# 출력 결과
# 2
# a.div()
# 출력 결과
# 2

#     2. 클래스 구조 만들기
# class FourCal:
#     pass

# a = FourCal()
# type(a)
# <class '__main__.FourCal'>

#     3. 객체에 연산할 숫자 지정하기
# 파이썬 메서드의 첫 번째 매개변수 이름은 관례적으로 self를 사용한다.
# 객체의 메서드를 호출할 때 호출한 객체 자신이 전달되기 때문에 self라는 이름을 사용한 것이다.
# 물론 self말고 다른 이름을 사용해도 상관없다.
# a.setdata(4, 2)

# class FourCal:
#     def setdata(self, first, second):
#         self.first = first
#         self.second = second

# def 함수_이름(매개변수):
#     수행할_문장
#     ...

# def setdata(self, first, second):   # 메서드의 매개변수
#     self.first = first              # 메서드의 수행문
#     self.second = second            # 메서드의 수행문

# a = FourCal()
# a.setdata(4, 2)

# a = FourCal()
# FourCal.setdata(a, 4, 2)

# 위와 같이 ‘클래스명.메서드’ 형태로 호출할 때는 객체 a를 첫 번째 매개변수 self에 꼭 전달해야 한다. 
# 반면 다음처럼 ‘객체.메서드’ 형태로 호출할 때는 self를 반드시 생략해서 호출해야 한다.
# a = FourCal()
# a.setdata(4, 2)

# def setdata(self, first, second):   # 메서드의 매개변수
#     self.first = first              # 메서드의 수행문
#     self.second = second            # 메서드의 수행문

# self.first = 4
# self.second = 2

# self는 전달된 객체 a이므로 다시 다음과 같이 해석된다.
# a.first = 4
# a.second = 2

# a = FourCal()
# a.setdata(4, 2)
# a.first
# 출력 결과
# 4
# a.second
# 출력 결과
# 2

# a = FourCal()
# b = FourCal()

# a.setdata(4, 2)
# a.first
# 출력 결과
# 4

# b.setdata(3, 7)
# b.first
# 출력 결과
# 3

# a.first
# 출력 결과
# 4

# class FourCal:
#     def setdata(self, first, second):
#         self.first = first
#         self.second = second

#     4. 더하기 기능 만들기
# a = FourCal()
# a.setdata(4, 2)
# a.add()
# 출력 결과
# 6

# class FourCal:
#     def setdata(self, first, second):
#         self.first = first
#         self.second = second
#     def add(self):
#         result = self.first + self.second
#         return result

# a = FourCal()
# a.setdata(4, 2)
# a.add()
# 출력 결과
# 6

# def add(self):
#     result = self.first + self.second
#     return result

# result = self.first + self.second

# a.add()와 같이 a 객체에 의해 add 메서드가 수행되면 add 메서드의 self에는 객체 a가 자동으로 입력되므로 이 내용은 다음과 같이 해석된다.
# result = a.first + a.second

# a.first와 a.second는 add 메서드가 호출되기 전에 a.setdata(4, 2) 문장에서 a.first = 4, a.second = 2로 설정된다. 
# 따라서 위 문장은 다시 다음과 같이 해석된다.
# result = 4 + 2

# a.add()
# 출력 결과
# 6

#     5. 곱하기, 빼기, 나누기 기능 만들기
# class FourCal:
#     def setdata(self, first, second):
#         self.first = first
#         self.second = second
#     def add(self):
#         result = self.first + self.second
#         return result
#     def mul(self):
#         result = self.first * self.second
#         return result
#     def sub(self):
#         result = self.first - self.second
#         return result
#     def div(self):
#         result = self.first / self.second
#         return result

# a = FourCal()
# b = FourCal()
# a.setdata(4, 2)
# b.setdata(3, 8)
# a.add()
# # 출력 결과
# 6
# a.mul()
# 출력 결과
# 8
# a.sub()
# 출력 결과
# 2
# a.div()
# 출력 결과
# 2
# b.add()
# 출력 결과
# 11
# b.mul()
# 출력 결과
# 24
# b.sub()
# 출력 결과
# -5
# b.div()
# 출력 결과
# 0.375

# 4. 생성자
# a = FourCal()
# a.add()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "<stdin>", line 6, in add
# AttributeError: 'FourCal' object has no attribute 'first'

# FourCal 클래스의 인스턴스 a에 setdata 메서드를 수행하지 않고 add 메서드를 먼저 수행하면 ‘AttributeError: 'FourCal' object has no attribute 'first'’오류가 발생한다. 
# setdata 메서드를 수행해야 객체 a의 객체변수 first와 second가 생성되기 때문이다.
# 이렇게 객체에 first, second와 같은 초깃값을 설정해야 할 필요가 있을 때는 setdata와 같은 메서드를 호출하여 초깃값을 설정하기보다 생성자(constructor)를 구현하는 것이 안전한 방법이다.
# 생성자(constructor)란 객체가 생성될 때 자동으로 호출되는 메서드를 의미한다. 
# 파이썬 메서드명으로 __init__를 사용하면 이 메서드는 생성자가 된다.

# 다음과 같이 FourCal 클래스에 생성자(constructor)를 추가해 보자.
# __init__ 메서드의 init 앞뒤로 붙은 __는 밑줄(_) 2개를 붙여 쓴 것이다.

# class FourCal:
#     def __init__(self, first, second):
#         self.first = first
#         self.second = second
#     def setdata(self, first, second):
#         self.first = first
#         self.second = second
#     def add(self):
#         result = self.first + self.second
#         return result
#     def mul(self):
#         result = self.first * self.second
#         return result
#     def sub(self):
#         result = self.first - self.second
#         return result
#     def div(self):
#         result = self.first / self.second
#         return result

# 새롭게 추가된 생성자 __init__ 메서드만 따로 떼어 내서 살펴보자.

# def __init__(self, first, second):
#     self.first = first
#     self.second = second

# __init__ 메서드는 setdata 메서드와 이름만 다르고 모든 게 동일하다. 
# 단, 메서드 이름을 __init__로 했기 때문에 생성자로 인식되어 객체가 생성되는 시점에 자동으로 호출된다는 차이가 있다.
# 이제 다음처럼 a 객체를 생성해 보자.

# a = FourCal()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# TypeError: __init__() missing 2 required positional arguments: 'first' and 'second'

# a = FourCal()을 수행할 때 생성자 __init__가 호출되어 위와 같은 오류가 발생했다. 
# 오류가 발생한 이유는 생성자의 매개변수 first와 second에 해당하는 값이 전달되지 않았기 때문이다.
# 이 오류를 해결하려면 다음처럼 first와 second에 해당하는 값을 전달하여 객체를 생성해야 한다.

# a = FourCal(4, 2)
# 위와 같이 수행하면 __init__ 메서드의 매개변수에는 각각 다음과 같은 값이 전달된다.

# __init__ 메서드도 다른 메서드와 마찬가지로 첫 번째 매개변수 self에 생성되는 객체가 자동으로 전달된다는 점을 기억하자.
# 따라서 __init__ 메서드가 호출되면 setdata 메서드를 호출했을 때와 마찬가지로 first와 second라는 객체변수가 생성될 것이다.
# 다음과 같이 객체변수의 값을 확인해 보자.

# a = FourCal(4, 2)
# a.first
# 출력 결과
# 4
# a.second
# 출력 결과
# 2

# a = FourCal(4, 2)
# a.add()
# 출력 결과
# 6
# a.div()
# 출력 결과
# 2.0

# 5. 클래스의 상속
# 앞에서 FourCal 클래스는 이미 만들어 놓았으므로 FourCal 클래스를 상속하는 MoreFourCal 클래스는 다음과 같이 간단하게 만들 수 있다.
# class MoreFourCal(FourCal):
#     pass

# 클래스를 상속하기 위해서는 다음처럼 클래스 이름 뒤 괄호 안에 상속할 클래스 이름을 넣어주면 된다.
# class 클래스_이름(상속할_클래스_이름)

# MoreFourCal 클래스는 FourCal 클래스를 상속했으므로 FourCal 클래스의 모든 기능을 사용할 수 있다.
# a = MoreFourCal(4, 2)
# a.add()
# 출력 결과
# 6
# a.mul()
# 출력 결과
# 8
# a.sub()
# 출력 결과
# 2
# a.div()
# 출력 결과
# 2

# 이제 원래 목적인 a^b을 계산하는 MoreFourCal 클래스를 만들어 보자.
# class MoreFourCal(FourCal):
#     def pow(self):
#         result = self.first ** self.second
#         return result

# pass 문장은 삭제하고 위와 같이 두 수의 거듭제곱을 구할 수 있는 pow 메서드를 추가했다. 
# 그리고 다음과 같이 pow 메서드를 수행해 보자.
# a = MoreFourCal(4, 2)
# a.pow()
# 출력 결과
# 16
# a.add()
# 출력 결과
# 6

# MoreFourCal 클래스로 만든 a 객체에 값 4와 2를 지정한 후 pow 메서드를 호출하면 4의 2제곱인 16을 리턴하는 것을 확인할 수 있다. 
# 상속받은 기능인 add 메서드도 잘 동작한다.

# 상속은 MoreFourCal 클래스처럼 기존 클래스(FourCal)는 그대로 놔둔 채 클래스의 기능을 확장할 때 주로 사용한다.

# 6. 메서드 오버라이딩
# a = FourCal(4, 0)
# a.div()
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#     result = self.first / self.second
# ZeroDivisionError: division by zero

# FourCal 클래스의 객체 a에 값 4와 0을 지정하고 div 메서드를 호출하면 4를 0으로 나누려고 하므로 ZeroDivisionError 오류가 발생한다. 
# 0으로 나눌 때 오류가 아닌 값 0을 리턴받고 싶다면 어떻게 해야 할까?
# 다음과 같이 FourCal 클래스를 상속하는 SafeFourCal 클래스를 만들어 보자.

# class SafeFourCal(FourCal):
#     def div(self):
#         if self.second == 0:  # 나누는 값이 0인 경우 0을 리턴하도록 수정
#             return 0
#         else:
#             return self.first / self.second

# FourCal 클래스에 있는 div 메서드를 동일한 이름으로 다시 작성했다. 
# 이렇게 부모 클래스(상속한 클래스)에 있는 메서드를 동일한 이름으로 다시 만드는 것을 메서드 오버라이딩(method overriding)이라고 한다. 
# 이렇게 메서드를 오버라이딩하면 부모 클래스의 메서드 대신 오버라이딩한 메서드가 호출된다.
# SafeFourCal 클래스에 오버라이딩한 div 메서드는 나누는 값이 0인 경우에는 0을 리턴하도록 수정했다. 
# 이제 다시 앞에서 수행한 예제를 FourCal 클래스 대신 SafeFourCal 클래스를 사용하여 수행해 보자.

# a = SafeFourCal(4, 0)
# a.div()
# 출력 결과
# 0

# FourCal 클래스와 달리 ZeroDivisionError가 발생하지 않고 의도한 대로 0이 리턴되는 것을 확인할 수 있다.

# 7. 클래스변수
# class Family:
#     lastname = "김"

# Family 클래스에 선언한 lastname이 바로 클래스변수이다. 
# 클래스변수는 클래스 안에 함수를 선언하는 것과 마찬가지로 클래스 안에 변수를 선언하여 생성한다.
# 이제 Family 클래스를 다음과 같이 사용해 보자.

# Family.lastname
# 김

# 클래스변수는 위 예와 같이 클래스_이름.클래스변수로 사용할 수 있다.
# 또는 다음과 같이 Family 클래스로 만든 객체를 이용해도 클래스변수를 사용할 수 있다.

# a = Family()
# b = Family()
# a.lastname
# 김
# b.lastname
# 김

# 만약 Family 클래스의 lastname을 "박"이라는 문자열로 바꾸면 어떻게 될까? 다음과 같이 확인해 보자.
# Family.lastname = "박"
# a.lastname
# 박
# b.lastname
# 박

# 클래스변수의 값을 변경했더니 클래스로 만든 객체의 lastname 값도 모두 변경된다는 것을 확인할 수 있다. 
# 즉, 클래스변수는 객체변수와 달리 클래스로 만든 모든 객체에 공유된다는 특징이 있다.
# 클래스변수를 가장 늦게 설명하는 이유는 클래스에서 객체변수가 클래스변수보다 훨씬 중요하기 때문이다. 
# 실무에서 프로그래밍할 때도 클래스변수보다 객체변수를 사용하는 비율이 훨씬 높다.

# 클래스변수와 동일한 이름의 객체변수를 생성하면?
# 위의 예제에서 a.lastname을 다음처럼 변경하면 어떻게 될까?

# a.lastname = "최"
# a.lastname
# 최

# 이렇게 하면 Family 클래스의 lastname이 바뀌는 것이 아니라 a 객체에 lastname이라는 객체변수가 새롭게 생성된다. 
# 즉, 객체변수는 클래스변수와 동일한 이름으로 생성할 수 있다.
# a.lastname 객체변수를 생성하더라도 Family 클래스의 lastname과는 상관없다는 것을 다음과 같이 확인할 수 있다.

# Family.lastname
# 박
# b.lastname
# 박

# Family 클래스의 lastname 값은 변하지 않았다.