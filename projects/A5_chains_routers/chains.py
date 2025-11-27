from langchain_core.output_parsers import StrOutputParser
from app.services.llm_client import llm_chain
from .prompts import (
    classifier_prompt,
    general_prompt,
    code_prompt,
    summary_prompt,
    math_prompt,
)
from .rag import rag_answer


llm = llm_chain() # Cliente LangChain para cadenas. LLM sincronizado para LCEL
parser = StrOutputParser() # Parser simple para cadenas, limita la salida a str limpio

# ======================================================
# 1) Chains LCEL
# ======================================================

classifier_chain = classifier_prompt | llm | parser
general_chain = general_prompt | llm | parser
code_chain = code_prompt | llm | parser
summary_chain = summary_prompt | llm | parser
math_chain = math_prompt | llm | parser


# ======================================================
# 2) Router manual usando LCEL
# ======================================================

async def run_router_chain(question: str):

    # Ejecutar classifier (sync)
    intent = classifier_chain.invoke({"input": question}).strip().lower()

    if "rag" in intent:
        answer = await rag_answer(question)
        chain_used = "rag_chain"

    elif "code" in intent:
        answer = code_chain.invoke({"input": question})
        chain_used = "code_chain"

    elif "summary" in intent:
        answer = summary_chain.invoke({"input": question})
        chain_used = "summary_chain"

    elif "math" in intent:
        answer = math_chain.invoke({"input": question})
        chain_used = "math_chain"

    else:
        answer = general_chain.invoke({"input": question})
        chain_used = "general_chain"

    return {
        "intent": intent,
        "chain_used": chain_used,
        "answer": answer.strip()
    }
