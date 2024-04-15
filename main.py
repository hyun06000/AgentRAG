from pydantic import BaseModel
from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI
from langchain.agents import LLMSingleActionAgent
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.tools import StructuredTool
from langchain.agents import AgentExecutor
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory


from tools.retrieval_tool import retrieval_vector_db_tool
from tools.conversation_tools import conversation_tool_with_search_master
from utils.customization import KORCustomPromptTemplate
from prompts.master.template import KOR_TEMPLATE

from dotenv import load_dotenv
load_dotenv()


class Item(BaseModel):
    text: str = None


master = FastAPI()

tools = [
    StructuredTool.from_function(retrieval_vector_db_tool),
    StructuredTool.from_function(conversation_tool_with_search_master),
]
tool_names = [tool.name for tool in tools]

prompt = KORCustomPromptTemplate(
    template=KOR_TEMPLATE,
    tools=tools,
    input_variables=["input", "intermediate_steps", "chat_history"]
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
memory = ConversationBufferWindowMemory(k=8, memory_key="chat_history")
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,    
)


@master.get("/")
async def hello():
    return {"hello":"It's me"}


@master.post("/prompt/")
async def read_root(message:Item):
    
    ai_answer = agent_executor.run({"input": f"{message.text}"},)

    return {"ai_answer": ai_answer}
