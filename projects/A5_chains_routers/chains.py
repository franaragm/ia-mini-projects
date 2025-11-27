from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda
from app.services.llm_client import llm_chain
from .prompts import (
    classifier_prompt,
    general_prompt,
    code_prompt,
    summary_prompt,
    math_prompt,
)
from .rag import rag_chain  # RAG como chain LCEL async

# ======================================================
# Inicialización del LLM y parser
# ======================================================

llm = llm_chain()
parser = StrOutputParser()

# ======================================================
# Definición de Chains LCEL
# Cada Chain:
# - Prompt → LLM → Parser
# - Se encapsula la salida en {"answer": ..., "chain_used": ...}
# ======================================================

classifier_chain = classifier_prompt | llm | parser

general_chain = (
    general_prompt
    | llm
    | parser
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "general_chain"})
)

code_chain = (
    code_prompt
    | llm
    | parser
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "code_chain"})
)

summary_chain = (
    summary_prompt
    | llm
    | parser
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "summary_chain"})
)

math_chain = (
    math_prompt
    | llm
    | parser
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "math_chain"})
)

rag_chain = (
    rag_chain
    | RunnableLambda(lambda x: {"answer": x, "chain_used": "rag_chain"})
)

# ======================================================
# Router LCEL profesional con RunnableBranch
# Evalúa el campo "intent" y ejecuta la chain correcta
# ======================================================

router_chain = RunnableBranch(
    (lambda x: "rag" in x["intent"], rag_chain),
    (lambda x: "code" in x["intent"], code_chain),
    (lambda x: "summary" in x["intent"], summary_chain),
    (lambda x: "math" in x["intent"], math_chain),
    general_chain,  # Default
)

# ======================================================
# Función principal async
# ======================================================

# Pipeline 100% declarativo:
# 1) Obtiene intención
# 2) Enruta dinámicamente usando RunnableBranch
# 3) Devuelve un diccionario consistente:
#     {
#         "intent": <intención>,
#         "chain_used": <nombre_chain>,
#         "answer": <respuesta>
#     }
async def run_router_chain(question: str):   
    # Ejecutar classifier (sync)
    intent = classifier_chain.invoke({"input": question}).strip().lower()

    # Ejecutar router de forma async
    answer_block = await router_chain.ainvoke(
        {"intent": intent, "input": question}
    )

    return {
        "intent": intent,
        "chain_used": answer_block["chain_used"],
        "answer": answer_block["answer"].strip(),
    }
