from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.prompts import age_template, sql_template, answer_template


def age_extract_chain(model) -> str:
    return age_template() | model | StrOutputParser()


def sql_chain(model) -> str:
    return (
        {"question": age_extract_chain(model)}
        | sql_template()
        | model
        | StrOutputParser()
    )


def percentile_chain(model, database) -> str:
    return (
        {
            "question": RunnablePassthrough(),
            "query": sql_chain(model),
        }
        | RunnablePassthrough.assign(
            response=lambda x: database.sql(
                x["query"][x["query"].find(r"SELECT") : len(x["query"]) - 1]
            ).fetchone()
        )
        | answer_template()
        | model
        | StrOutputParser()
    )
