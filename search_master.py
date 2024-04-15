from pydantic import BaseModel
from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI
from langchain.agents import LLMSingleActionAgent
from langchain.agents.output_parsers import JSONAgentOutputParser
from langchain.tools import StructuredTool
from langchain.agents import AgentExecutor
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory


from tools.conversation_tools import conversation_tool_with_article_researcher
from tools.retrieval_tool import upsert_vector_db_tool
from utils.customization import KORCustomPromptTemplate
from prompts.search_master.template import KOR_TEMPLATE

from dotenv import load_dotenv
load_dotenv()


class Item(BaseModel):
    text: str = None


search_master = FastAPI()


tools = [
    StructuredTool.from_function(conversation_tool_with_article_researcher),
    StructuredTool.from_function(upsert_vector_db_tool),
    
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
memory = ConversationBufferWindowMemory(k=4, memory_key="chat_history")
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=memory,
    handle_parsing_errors=True,    
)


@search_master.post("/prompt/")
async def read_root(message:Item):
    
    ai_answer = agent_executor.run({"input": f"{message.text}"},)

    return {"ai_answer": ai_answer}
