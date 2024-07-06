from langchain_core.prompts import PromptTemplate
from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores.oraclevs import OracleVS
from dotenv import load_dotenv
import ast
from collections import defaultdict
import database

load_dotenv()
def prompt_create(city, date, date2, number, question):
    db = database.Database()
    db.set_vector_store()
    retriever = db.get_retriever()

    llm = ChatUpstage()

    template = """Create an hourly travel plan based on the following information and prompt.
        travel destination: {city}, first day: {date}, last day: {date2}, number of people: {number} 
        Prompt: {question}
        Recommend the places based on these if related: {context}

        The output should be a list of 3-tuples: [(X, Y, Z), (X1, Y1, Z1), ...].
        The first element is a date with the summary of its day. (for example, XXXX-XX-XX (Day 1: 출발 및 XX 도착))
        Do not restrict yourself with the title generation.
        The second element is a time.
        The third element is a place.
        The content should be in Korean.
        DO NOT ANSWER OTHER THAN THE LIST OF 3-TUPLES. FOLLOW THE OUTPUT FORMAT.
            """

    prompt_template = PromptTemplate.from_template(template)

    # date 형식에 따라 입력 형식 바꿀 수 있음

    while(True):
        chain = prompt_template | llm | StrOutputParser()
        response = chain.invoke({"context": retriever, "question": question, "city": city, "date": date, "date2": date2, "number": number})
        try:
            if not isinstance(ast.literal_eval(response), list):
                continue
            break
        except:
            continue

    tbl = ast.literal_eval(response)
    result = defaultdict(list)
    for t in tbl:
        key = t[0]
        value = (t[1], t[2])
        result[key].append(value)

    transformed_list = [(key, value) for key, value in result.items()]

    return transformed_list

# prompt_create("부산", "2024-07-06", "2024-07-09", 1, "여유로운 여행을 원해")