from pydantic import BaseModel
from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI
from langchain.agents import LLMSingleActionAgent
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.tools import StructuredTool
from langchain.agents import AgentExecutor
from langchain.chains import LLMChain


from tools.request_tools import request_tool
from tools.conversation_tools import conversation_tool_with_article_parser
from utils.customization import KORCustomPromptTemplate
from prompts.article_parser.template import KOR_TEMPLATE

from dotenv import load_dotenv
load_dotenv()



class Item(BaseModel):
    text: str = None


article_parser = FastAPI()


tools = [
    StructuredTool.from_function(request_tool),
]
tool_names = [tool.name for tool in tools]

prompt = KORCustomPromptTemplate(
    template=KOR_TEMPLATE,
    tools=tools,
    input_variables=["input", "intermediate_steps"]
)
llm = ChatOpenAI(temperature=0, model="gpt-4-turbo-preview")
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True
)
agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=JSONAgentOutputParser(),
    stop=["\nObservation:", "\n- 관측"],
    allowed_tools=tool_names,
    return_intermediate_steps=False,
)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,    
)


@article_parser.post("/prompt/")
async def read_root(message:Item):
    
    ai_answer = agent_executor.run({"input": f"{message.text}"},)

    return {"ai_answer": ai_answer}
