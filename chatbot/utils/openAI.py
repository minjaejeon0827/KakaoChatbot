# [openai 전용 모듈] openai==1.77.0

# 터미널창에 Langchain 라이브러리 설치 명령어 입력 및 엔터  
# pip install "pydantic>=2.5.2,<3.0.0" langchain-community langchain-openai chromadb

# TODO: AWS Lambda Funtion 실행시 아래와 같은 오류 메시지 출력되어 파이썬 numpy 패키지 버전 변경함. (2025.05.16 minjae)
#       (기존) numpy==2.2.5 (pip uninstall numpy) -> (변경) numpy==1.26.2 (pip install numpy==1.26.2)
# 오류 메시지
# module 'faiss' has no attribute 'IndexFlatL2'
# ImportError: numpy.core.multiarray failed to import During handling of the above exception, another exception occurred:
# File "/var/lang/lib/python3.11/site-packages/langchain_community/vectorstores/faiss.py", line 1001, in __from
# index = faiss.IndexFlatL2(len(embeddings[0]))
# 참고 URL - https://chatgpt.com/c/682a8cdd-1f78-8010-ae2f-3c84f0284d2f

# TODO: langchain_community.vectorstores 패키지에 속한 클래스 Chroma 사용시 
#       아래와 같은 오류 메시지 출력되어 오류 원인 파악 필요 (2025.05.15 minjae)
# 오류 메시지 
# [91mYour system has an unsupported version of sqlite3. Chroma requires sqlite3 >= 3.35.0.[0m
# [94mPlease visit https://docs.trychroma.com/troubleshooting#sqlite to learn how to upgrade.[0m
# 참고 URL - https://wikidocs.net/5327
# 참고 2 URL - https://docs.trychroma.com/troubleshooting
# 참고 3 URL - https://docs.trychroma.com/updates/troubleshooting#sqlite

# TODO: 아래와 같은 경고 메시지 출력시 아래와 주석친 터미널 명령어 순차적으로 실행 필요. (2025.05.14 minjae)
# 경고 메시지 - WARNING: There was an error checking the latest version of pip. 
# 참고 URL - https://chatgpt.com/c/682421ae-e1bc-8010-bf07-4f715ca75ab1
# python -m pip install --upgrade pip (pip 자체 업그레이드 시도)
# ping pypi.org (인터넷 연결 확인)

import asyncio
import os   # 파일 존재 여부 확인 및 답변 결과를 텍스트 파일로 저장할 때 경로 생성해야 해서 패키지 "os" 불러오기
# import gc   # 가비지 컬렉션(Garbage Collection)

from modules import chatbot_logger   # 폴더 "modules" -> 챗봇 로그 작성 모듈 
from commons import chatbot_helper   # 폴더 "commons" -> 챗봇 전용 도움말 텍스트 

from openai import OpenAI   # OPENAI 패키지 openai 불러오기 (ChatGPT, DALLE.2 사용)

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# TODO: AWS Lambda Funtion 실행시 아래와 같은 오류 메시지 출력되어 변경함. (2025.05.16 minjae)
#       (기존) from langchain.embeddings import OpenAIEmbeddings -> (변경) from langchain_community.embeddings import OpenAIEmbeddings
# 오류 메시지 
# /var/task/modules/openAI.py:30: LangChainDeprecationWarning: Importing OpenAIEmbeddings from langchain.embeddings is deprecated. Please replace deprecated imports:
# >> from langchain.embeddings import OpenAIEmbeddings
# with new imports of:
# >> from langchain_community.embeddings import OpenAIEmbeddings
# You can use the langchain cli to **automatically** upgrade many imports. Please see documentation here <https://python.langchain.com/docs/versions/v0_2/>
# from langchain.embeddings import OpenAIEmbeddings
# from langchain_community.embeddings import OpenAIEmbeddings

# TODO: AWS Lambda Funtion 실행시 아래와 같은 오류 메시지 출력되어 변경함. (2025.05.14 minjae)
#       (기존) from langchain.document_loaders import TextLoader -> (변경) from langchain_community.document_loaders import TextLoader
# 오류 메시지 
# /var/task/modules/openAI.py:20: LangChainDeprecationWarning: Importing TextLoader from langchain.document_loaders is deprecated. Please replace deprecated imports:
# >> from langchain.document_loaders import TextLoader
# with new imports of:
# >> from langchain_community.document_loaders import TextLoader
# from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from utils.log import logger   # 챗봇 전역 로그 객체 (logger)

# TODO: 필요시 아래 코드 가독성이 높은 함수 sum_of_even_numbers 참고해서 챗봇 프로그램 고도화 작업 진행 예정 (2025.08.08 minjae)
# def sum_of_even_numbers(numbers_list):
#   """
#   Calculate the sum of all even numbers in a given list.

#   Parameters:
#   numbers_list (list): A list of integers.

#   Returns:
#   int: The sum of all even numbers in the list.
#   """
#   even_numbers = [number for number in numbers_list if number % 2 == 0]
#   total_sum = sum(even_numbers)
#   return total_sum

# OpenAI API KEY
# 테스트용 카카오톡 챗봇 채팅방에서 
# ChatGPT와 통신하기 위해 OpenAI API 키 입력
# 1. 아마존 웹서비스(AWS) 함수 lambda_handler -> 환경변수로 저장한 OpenAI API 키 'OPENAI_API' 불러오기
# 2. 1번에서 불러온 OpenAI API 키 'OPENAI_API'를 인자로 전달하여 OpenAI 클래스 객체 client 선언 및 생성하기 
OPENAI_KEY = os.environ['OPENAI_API'] 
client = OpenAI(api_key=OPENAI_KEY)

def get_msgFromGPT(prompt: str) -> str:
    """
    Description: ChatGPT 텍스트 응답 메시지 가져오기

                 *** 참고 ***
                 모델: gpt-4o
                 목적: 대한민국 건설업 및 Autodesk 제품 기술지원 분야에 특화된 기술지원 챗봇 '상진' 구현
                 참고 URL: https://chatgpt.com/c/68945c67-48b4-8330-908f-a97f55a32433
                 참고 2 URL: https://chatgpt.com/c/68945c22-cb30-8333-9f04-a1b2f2ba7110
                 참고 3 URL: https://chatgpt.com/c/68bf6d7c-9148-8320-960c-41ae2a11cff8

    Parameters: prompt - 사용자 질문 내용 

    Returns: msg - ChatGPT 텍스트 응답 메시지
    """

    try:
        chatbot_logger.openAI_log_write(chatbot_logger._info, "[테스트] ChatGPT 텍스트 가져오기", 'Start!') 

        # TODO: 아래 주석친 코드 필요시 참고 (2025.08.27 minjae)    
        # raise Exception(chatbot_helper._error_title + 
        #                 '사유: ChatGPT 텍스트 가져오기 오류 발생!!!\n'+
        #                 '추가 문의 필요시\n'+
        #                 chatbot_helper._error_ssflex)   # 예외 발생시킴

        # TODO: 퍼플렉시티(Perplexity) AI 서비스 처럼 출처를 명확히 제시하여 정보의 신뢰성을 보장할 수 있도록 client.responses.create 함수 파라미터 instructions에 문구 추가 구현 (2025.09.09 minjae)
        # 참고 URL - https://yozm.wishket.com/magazine/detail/3001/
        # 참고 2 URL - https://chatgpt.com/c/68bf6d7c-9148-8320-960c-41ae2a11cff8
        # 참고 3 URL - https://chatgpt.com/c/68bfd1b9-254c-8323-957c-a13575993321
        # 참고 4 URL - https://chatgpt.com/c/68c0b68f-a974-8328-abdd-9359f1dea53f
        
        # TODO: ChatGPT API 호출 결과 답변 마지막 부분 텍스트(기술지원, 주의사항 등등...)가 잘리거나 짧게 나오는 현상 발생하여 
        #       client.responses.create 함수 파라미터 max_output_tokens 값 변경 (max_output_tokens=1500) 및 함수 파라미터 instructions에 문구 2차 추가 구현 (2025.09.09 minjae)
        # 참고 URL - https://platform.openai.com/docs/guides/reasoning
        # 참고 2 URL - https://chatgpt.com/c/68bfbbdd-d1dc-8321-bfce-8cb0abee01b4

        # TODO: ChatGPT API 함수 client.responses.create 호출시 파라미터 "instructions"에 아래 내용 추가 및 보완하기 (2025.09.12 minjae)
        # (예) 고객이 자세하게 알려달라고 해도 최대한 요약해서 답변하기 (토큰 과금 줄이기)
        # (예2) 대한민국 건축, 토목, 기계, 전기, 소방, 안전관리 또는 Autodesk 기술지원 외적으로 사용자가 질문하면 답변을 하지 못하도록 처리하기 
        # (예3) (예2)번과 같은 상황 발생시엔 model="gpt-3.5-turbo"로 답변하고 대한민국 건축, 토목, 기계, 전기, 소방, 안전관리 또는 Autodesk 기술지원 관련 질문시엔 model="gpt-5"로 답변하기 
        # 참고 URL - https://platform.openai.com/docs/quickstart
        # response = client.responses.create(model="gpt-5",
        response = client.responses.create(model="gpt-4o",
                                           instructions = ("안녕하세요. 기술지원 챗봇 '상진'입니다.\n"
                                                           "대한민국 건축, 토목, 기계, 전기, 소방, 안전관리 및\n"
                                                           "Autodesk 제품(AutoCAD, Revit, Navisworks Manage, InfraWorks, Civil3D, Dynamo 등) 관련 기술지원에 특화된 챗봇입니다.\n\n"
                                                           "【응답 원칙】\n"
                                                           "1) 모든 답변은 반드시 한국어로 제공해야 합니다.\n"
                                                           "2) 정중하고 친절한 말투를 사용해야 합니다.\n"
                                                           "3) 전문 용어는 필요 시 이해하기 쉽게 풀어서 설명해야 합니다.\n\n"
                                                           "【출처 제시 지침】\n"
                                                           "1) 모든 답변의 마지막에는 반드시 아래 네 가지 항목을 이 순서대로 포함해야 합니다:\n"
                                                           "   ① 웹문서 출처\n② 동영상 출처\n③ 기술지원\n④ 주의사항\n"
                                                           "   답변이 길어져 토큰이 부족할 경우, 본문 내용은 요약해도 되지만 네 가지 항목 ① 웹문서 출처\n② 동영상 출처\n③ 기술지원\n④ 주의사항\n 반드시 제시하세요.\n\n"
                                                           "2) 웹문서 출처와 동영상 출처는 반드시 답변 본문 내용에서 언급된 제품, 기술, 기관과 직접적으로 연결된 공식 URL만 제시하세요.\n"
                                                           "   - 예: Revit을 설명했다면 Autodesk 공식 문서와 Autodesk 공식 유튜브 채널.\n"
                                                           "   - 예: 세움터를 설명했다면 국토교통부 e-세움터 공식 사이트와 국토교통부 유튜브.\n"
                                                           "3) 답변과 직접 연결된 신뢰할 수 있는 공식 출처가 없으면 '출처 없음'이라고만 작성하세요.\n"
                                                           "4) 유효하지 않거나 존재하지 않는 URL은 절대 작성하지 마세요.\n"
                                                           "   - 존재하지 않는 경우 반드시 '출처 없음'으로만 작성하세요.\n"
                                                           "   - 임의로 추측하거나 가상의 URL을 만들어 제시하지 마세요.\n"
                                                           "5) 웹문서 출처와 동영상 출처는 실제 접근 가능한 공식 사이트/채널만 제시하세요.\n"
                                                           "6) URL은 반드시 **Markdown 하이퍼링크 형식**으로 작성하세요.\n"
                                                           "7) 가능하면 최소 2개 이상의 신뢰할 수 있는 공식 URL을 제시하세요.\n"
                                                           "   만약 신뢰할 수 있는 웹문서 출처와 동영상 출처가 1개만 있는 경우에는 1개만 제시해도 됩니다.\n"
                                                           "   - 예시 (최소 2개 이상):\n"
                                                           "     웹문서 출처:\n"
                                                           "     - [Autodesk 공식 문서] (https://help.autodesk.com)\n"
                                                           "     - [국토교통부 건축행정시스템] (https://www.eais.go.kr)\n"
                                                           "     동영상 출처:\n"
                                                           "     - [Autodesk 공식 유튜브] (https://www.youtube.com/user/Autodesk)\n"
                                                           "     - [국토교통부 공식 유튜브] (https://youtube.com/@korealand)\n"
                                                           "   - 예시 (1개만 가능할 경우):\n"
                                                           "     웹문서 출처:\n"
                                                           "     - [Autodesk 공식 문서] (https://help.autodesk.com)\n"
                                                           "     동영상 출처:\n"
                                                           "     - [Autodesk 공식 유튜브] (https://www.youtube.com/user/Autodesk)\n"
                                                           "8) 대한민국 건축, 토목, 기계, 전기, 소방, 안전관리 및\n"
                                                           "   Autodesk 제품(AutoCAD, Revit, Navisworks Manage, InfraWorks, Civil3D, Dynamo 등) 관련 질문을 사용자로 부터 받을 경우\n"
                                                           "   신뢰할 수 있는 웹문서 출처와 동영상 출처를 아래와 같이 기본적으로 **최소 2개 이상** 제시하세요.\n"
                                                           "   웹문서 출처:\n"
                                                           "   1. Autodesk와 같은 글로벌 공식 문서.\n"
                                                           "   2. 국내 기관 자료.\n"
                                                           "   2. 국내 기관 자료는 아래 우선순위를 따릅니다:\n"
                                                           "   - 우선순위 예시:\n"
                                                           "   ① 국토교통부 (예: e-세움터, 건축행정시스템 https://www.eais.go.kr)\n"
                                                           "   ② 한국건설기술연구원 (KICT, https://www.kict.re.kr)\n"
                                                           "   ③ 대한건설협회 (https://www.cak.or.kr)\n"
                                                           "   ④ 기타 공신력 있는 국내 건설 관련 기관\n"
                                                           "   동영상 출처:\n"
                                                           "   1. Autodesk와 같은 글로벌 공식 동영상.\n"
                                                           "   2. 국내 기관 공식 동영상.\n"
                                                           "   2. 국내 기관 공식 동영상은 아래 우선순위를 따릅니다:\n"
                                                           "   - 우선순위 예시:\n"
                                                           "   ① 국토교통부 공식 유튜브 (https://youtube.com/@korealand)\n"
                                                           "   ② 한국건설기술연구원 공식 유튜브 (https://youtube.com/@feelkict)\n"
                                                           "   ③ 대한건설협회 공식 유튜브 (건설 통통 TV, https://youtube.com/@tv-ml1gt)\n"
                                                           "   ④ 기타 공신력 있는 국내 건설 관련 기관\n"
                                                           "9) 기술지원은 항상 고정된 URL을 사용하세요.\n"
                                                           "   - 기술지원: [상상플렉스 커뮤니티] (https://www.ssflex.co.kr/community/open)\n\n"
                                                           "【불확실할 때 대응 지침】\n"
                                                           "1) 정확하지 않은 내용은 추측하거나 단정적으로 말하지 마세요.\n"
                                                           "2) 불확실함을 명확히 알리고, 추가로 필요한 조건이나 정보를 제시하세요.\n"
                                                           "3) 공식 자료나 참고 가능한 경로(URL 포함)를 안내하세요.\n\n"
                                                           "【마무리 형식】\n"
                                                           "웹문서 출처:\n"
                                                           "- [OOO] (https://...)\n"
                                                           "- [OOO] (https://...)  # 최소 2개 이상 권장, 단 1개만 가능할 경우 1개만 작성\n\n"
                                                           "동영상 출처:\n"
                                                           "- [OOO] (https://...)\n"
                                                           "- [OOO] (https://...)  # 최소 2개 이상 권장, 단 1개만 가능할 경우 1개만 작성\n\n"
                                                           "기술지원: [상상플렉스 커뮤니티] (https://www.ssflex.co.kr/community/open)\n\n"
                                                           "* 주의사항: 기술지원 챗봇은 실수를 할 수 있습니다. 응답을 반드시 다시 확인해 주세요.\n"),
                                           input=prompt,
                                           max_output_tokens=1500)  # 출력 토큰(생성할 응답의 최대 토큰 수) 상한 (기본값) 보통 512 -> 1500 증가 설정  
    
        chatbot_logger.openAI_log_write(chatbot_logger._info, "[테스트] ChatGPT 텍스트 response", response)

        msg = response.output_text
        return msg
        
    except Exception as e:
        chatbot_logger.openAI_log_write(chatbot_logger._error, "[테스트] 오류", str(e)) 
        raise

    # TODO: 아래 주석친 코드 필요시 참고 (2025.08.13 minjae)
    # response = client.responses.create(model="gpt-3.5-turbo", 
    #                                    instructions='You are a thoughtful assistant. Respond to all input in 300 words and answer in korea', 
    #                                    input=prompt)

    # TODO: ChatGPT API 메서드 create 파라미터 instructions에 아래처럼 값 할당 구현 "안녕하세요.😀\n기술지원 챗봇 '상진'이에요.\n항상 정중하고 친절하게 응답해주세요." (2025.08.07 minjae)
    # 참고 URL - https://platform.openai.com/docs/quickstart
    # 참고 2 URL - https://wikidocs.net/217882
    # 참고 3 URL - https://wikidocs.net/201617 
    # 참고 4 URL - https://chatgpt.com/c/68944e39-0068-832b-a425-eaa31a25b2ba
    # 참고 5 URL - https://chatgpt.com/c/68945c67-48b4-8330-908f-a97f55a32433
    # 참고 6 URL - https://chatgpt.com/c/68945c22-cb30-8333-9f04-a1b2f2ba7110
    # response = client.responses.create(model="gpt-4o", 
    #                                    instructions="안녕하세요.😀\n기술지원 챗봇 '상진'이에요.\n항상 정중하고 친절하게 응답해주세요.", 
    #                                    input=prompt)

    # TODO: ChatGPT API 메서드 create 파라미터 instructions에 아래처럼 값 할당 구현 (2025.08.12 minjae)
    # response = client.responses.create(model="gpt-4o",
    #                                    instructions=("안녕하세요.😀\n기술지원 챗봇 '상진'이에요.\n"
    #                                                  "건축, 토목, 기계, 전기, 소방, BIM(Revit, AutoCAD, Dynamo 등) 관련 질문에 전문적으로 응답합니다.\n"
    #                                                  "언제나 정중하고 친절한 말투로 대답해주세요.\n"
    #                                                  "전문 용어를 적절히 사용하되, 필요 시 쉽게 풀어서 설명해 주세요.\n"
    #                                                  "응답은 항상 한국어로 해 주세요."),
    #                                    input=prompt)

    # msg = response.output_text
    # return msg

def get_img_urlFromDALLE(prompt: str) -> str:
    """
    Description: DALLE2 이미지 응답 URL 가져오기

    Parameters: prompt - 사용자 질문 내용

    Returns: img_url - DALLE2 이미지 응답 URL
    """

    response = client.images.generate(model="dall-e-3",
                                      prompt=prompt,
                                      size="1024x1024",
                                      quality="hd",
                                      n=1)

    img_url = response.data[0].url

    return img_url

def get_chunksFromText(file_path: str) -> list[str]:
    """
    Description: 텍스트 파일에 작성된 청크(chunk) 단위 텍스트 추출하기

                 *** 참고 ***
                 텍스트 파일에 작성된 청크(chunk) 단위 텍스트 추출
                 참고 URL - https://rudaks.tistory.com/entry/langchain-CharacterTextSplitter%E1%84%8B%E1%85%AA-RecursiveCharacterTextSplitter%E1%84%8B%E1%85%B4-%E1%84%8E%E1%85%A1%E1%84%8B%E1%85%B5
                 참고 2 URL - https://wikidocs.net/233998
                 참고 3 URL - https://wikidocs.net/231568
                 참고 4 URL - https://chatgpt.com/c/6811c621-90ec-8010-875b-a26b9ef09405

    Parameters: file_path - 텍스트 파일 상대 경로

    Returns: chunks - 청크(chunk) 단위 텍스트 리스트
    """
    
    if False == os.path.exists(file_path):   # 해당 경로에 텍스트 파일 존재 안 하는 경우
        chunks = []

    # 해당 경로에 PDF 파일 존재하는 경우 
    # 참고 URL - https://wikidocs.net/14304
    # 참고 2 URL - https://wikidocs.net/256287
    else:
        # 텍스트 파일 텍스트 추출
        loader = TextLoader(file_path)
        data = loader.load()

        text_splitter = CharacterTextSplitter(   # CharacterTextSplitter 클래스 객체 text_splitter 생성
            separator='\n',
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        
        chunks = text_splitter.split_text(data[0].page_content)   # 청크(chunk) 단위 텍스트 분할

        logger.log_write(logger._info, '[테스트] 청크(chunk) 단위 텍스트 분할: ', chunks)

    return chunks

def get_msgFromChunks(chunks: list[str], prompt: str) -> str:
    """
    Description: 텍스트 파일 청크(chunk) 단위 텍스트 리스트 기반 응답 메시지 가져오기

                 *** 참고 ***
                 텍스트 파일 청크(chunk) 단위 텍스트 리스트 기반 응답 메시지
                 참고 URL - https://wikidocs.net/234094
                 참고 2 URL - https://wikidocs.net/234014
                 참고 3 URL - https://chatgpt.com/c/6811e007-9a5c-8010-b023-700a286c2618
                 참고 4 URL - https://wikidocs.net/231568
                 참고 5 URL - https://wikidocs.net/233998

    Parameters: chunks - 청크(chunk) 단위 텍스트 리스트
                prompt - 사용자 질문 내용

    Returns: msg - 청크(chunk) 단위 텍스트 리스트 기반 응답 메시지
    """

    try:
        # TODO: 아래 주석친 if문 필요시 사용 예정 (2025.05.28 minjae) 
        # if not prompt:   # 질문을 입력하지 않은 경우 (공백 또는 null)
        #     return '질문을 다시 입력해주세요.'
        
        # 질문을 입력한 경우
        # 임베딩/ 시멘틱 인덱스 (API 요금 부과)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=OPENAI_KEY)

        # logger.log_write(logger._info, '[테스트] InMemoryVectorStore.from_texts: ', '시작')
        # vector_store = InMemoryVectorStore.from_texts(texts=chunks, embedding=embeddings)
        # # 정보 검색 도구(retriever)로 변환
        # retriever = vector_store.as_retriever(search_kwargs={"k": 1})   # k=1 로 설정(search_kwargs={"k": 1})하여 가장 유사한 단일 문서만 검색

        # TODO: FAISS 벡터 저장소(vector_store) 생성 기능 구현 (2025.05.19 minjae)
        # 참고 URL - https://python.langchain.com/docs/integrations/vectorstores/faiss/
        # 참고 2 URL - https://github.com/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/faiss.ipynb
        # 참고 3 URL - https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/faiss.ipynb
        # 참고 4 URL - https://wikidocs.net/234014
        # 참고 5 URL - https://www.youtube.com/watch?v=QeQaEIcaMow
        # 참고 6 URL - https://colab.research.google.com/github/corazzon/Mastering-NLP-from-Foundations-to-LLMs/blob/main/Chapter8_notebooks/Ch8_Setting_Up_LangChain_Configurations_and_Pipeline.ipynb#scrollTo=K9spKTF-L5Wc
        logger.log_write(logger._info, '[테스트] FAISS.from_texts', '시작')
        vector_store = FAISS.from_texts(chunks, embeddings)   # FAISS 벡터 저장소(vector_store) 생성
        # 정보 검색 도구(retriever)로 변환
        # retriever = vector_store.as_retriever(search_kwargs={"k": 1})   # k=1 로 설정(search_kwargs={"k": 1})하여 가장 유사한 단일 문서만 검색
        # score_threshold=0.8 로 설정(search_kwargs={"score_threshold": 0.8})하여 특정 임계값("score_threshold": 0.8}) 이상의 유사도를 가진 문서만 검색     
        # 참고 URL - https://teddylee777.github.io/langchain/rag-tutorial/
        # TODO: 아마존 웹서비스(AWS) 람다 함수(Lambda Function)에서 아래 코드 실행시 경고 메시지 "[WARNING] No relevant docs were retrieved using the relevance score threshold 0.8" 출력
        #       해당 경고 메시지의 의미는 아래 3가지와 같고, 필요시 코드 수정 예정 (2025.05.28 minjae)
        # 1. "No relevant docs were retrieved": 관련 문서를 찾지 못했다는 의미이다.
        # 2. "relevance score threshold 0.8": 검색 결과의 연관 점수(relevance score)가 0.8 이상이어야 유효한 문서로 간주된다는 설정이다.
        # 3. 즉, 검색된 문서들의 점수가 0.8보다 낮아서 모두 필터링되었고, 결과적으로 반환된 문서가 없었다는 경고이다.
        # 참고 URL - https://chatgpt.com/c/68365e3f-e6c4-8010-a95f-af0408b52857
        retriever = vector_store.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.8})
        # docs = vector_store.similarity_search(prompt, k=1)

        # RAG(검색증강생성) 기술이란?
        # 참고 URL - https://brunch.co.kr/@acc9b16b9f0f430/73
        # 참고 2 URL - https://aws.amazon.com/ko/what-is/retrieval-augmented-generation/

        # TODO: 함수 create_stuff_documents_chain, create_retrieval_chain 사용해서 사용자의 질문의 예상 답변 얻는 기능 구현 (2025.05.16 minjae)
        # 참고 URL - https://python.langchain.com/api_reference/core/prompts/langchain_core.prompts.chat.ChatPromptTemplate.html
        # 참고 2 URL - https://wikidocs.net/234020
        # 참고 3 URL - https://wikidocs.net/231328
        # 참고 4 URL - https://python.langchain.com/api_reference/langchain/chains/langchain.chains.retrieval.create_retrieval_chain.html
        # 참고 5 URL - https://chatgpt.com/c/6826c10a-1688-8010-b51c-c18d043d0967
        # 참고 6 URL - https://rudaks.tistory.com/entry/langchain-Langchain%EC%97%90%EC%84%9C-createretrievalchain-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0
        # 참고 7 URL - https://rudaks.tistory.com/entry/langchain-%EB%8C%80%ED%99%94%ED%98%95Conversational-RAG-%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%A7%8C%EB%93%A4%EA%B8%B0-1
        # 참고 8 URL - https://wikidocs.net/233346
        # 참고 9 URL - https://chatgpt.com/c/6826c10a-1688-8010-b51c-c18d043d0967
        # LLM 설정
        llm = ChatOpenAI(temperature=0,
                         openai_api_key=OPENAI_KEY,
                         max_tokens=2000,
                         model_name='gpt-3.5-turbo',
                         request_timeout=120)
            
        prompt_template = ChatPromptTemplate.from_template("다음 문서들을 참고하여 질문에 대답하세요:\n\n{context}\n\n질문: {input}")   # 프롬프트 템플릿
            
        stuff_chain = create_stuff_documents_chain(llm=llm, prompt=prompt_template)   # Stuff 방식 QA 체인 생성
        retrieval_chain = create_retrieval_chain(retriever=retriever, combine_docs_chain=stuff_chain)   # 검색 체인 생성 

        response = retrieval_chain.invoke({"input": prompt})   # 질문하기 (검색 수행)
        msg = response["answer"]   # 답변얻기

        # TODO: 아래 주석친 코드 필요시 참고 (2025.05.28 minjae)
        # 관련 문서 리스트 검색
        # 참고 URL - https://wikidocs.net/234016
        # 참고 2 URL - https://chatgpt.com/c/68365e3f-e6c4-8010-a95f-af0408b52857
        # docs = retriever.invoke(prompt)
         
        # if not docs:   # 관련 문서 리스트 존재하지 않는 경우
        #     msg = chatbot_helper._warningSSflex
         
        # else:   # 관련 문서 리스트 존재하는 경우
        #     response = retrieval_chain.invoke({"input": prompt})   # 질문하기 (검색 수행)
        #     msg = response["answer"]   # 답변얻기
        
        # logger.log_write(logger._info, '[테스트] 질문과 유사한 응답 메시지: ', msg) 

        return msg
    except Exception as e:   # 하위 코드 블록에서 예외가 발생해도 변수 e에다 넣고 아래 코드 실행됨
        # 테스트 오류 로그 기록
        logger.log_write(logger._error, "[테스트] 오류", str(e))   # str() 함수 사용해서 Exception 클래스 객체 e를 문자열로 변환 및 오류 메시지 변수 error_msg에 할당 (문자열로 변환 안할시 챗봇에서 스킬서버 오류 출력되면서 챗봇이 답변도 안하고 장시간 멈춤 상태 발생.) 
        raise    # raise로 함수 get_msgFromChunks의 현재 예외를 다시 발생시켜서 함수 get_msgFromChunks 호출한 상위 코드 블록으로 넘김

"""
*** 참고 ***
*** ChatGPT 문서 ***
* ChatGPT 텍스트 응답 메시지
참고 URL - https://github.com/openai/openai-python

* DALLE2 이미지 응답 URL
참고 URL - https://wikidocs.net/228931

*** 파이썬 문서 ***

*** 기타 문서 ***

"""