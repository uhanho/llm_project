from langchain_core.prompts import PromptTemplate
from langchain_upstage import ChatUpstage
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

def schedule_prompt(city, date, date2, number, prompt, context):
    load_dotenv()
    llm = ChatUpstage()

    template = """Create a travel plan based on the following information and prompt. Please, response in Korean:
            travel destination: {city}, first day: {date}, last day: {date2}, number of people: {number} 
            Prompt: {prompt}
            You have these candidates to choose from: {context}
            """

    # test
    city = "샌프란시스코"
    date = "2024-07-06"
    date2 = "2024-07-12"
    number = 1
    prompt = "여유로운 여행을 원해"

    prompt_template = PromptTemplate.from_template(template)

    # date 형식에 따라 입력 형식 바꿀 수 있음

    chain = prompt_template | llm | StrOutputParser()
    response = chain.invoke({"city": city, "date": date, "date2": date2, "number": number, "prompt": prompt, "context": context})
    print(response)