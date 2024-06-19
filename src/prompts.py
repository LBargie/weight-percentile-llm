from langchain_core.prompts import ChatPromptTemplate


SQL_PROMPT = """
    You are a DuckDB expert. Given an input question, create a syntactically correct DuckDB SQL query to run.
    You have access to a function called "lms_percentile" in the database. 
    The first value supplied to the function is the value for weight given in the question, followed by the L value, then M value and finally S value from the table.
    Use the age value given in the question to filter the Age column in the database. Do not convert the age value in the SQL query.
    Use the table information below to create the query:
    
    CREATE TABLE boys (
        "Age" BIGINT, 
        "L" DOUBLE PRECISION, 
        "M" DOUBLE PRECISION, 
        "S" DOUBLE PRECISION, 
        )

        /*
    3 rows from weights table:
        Age     L       M       S       
        0       0.3487  3.3464  0.14602 
        1       0.3127  3.3174  0.14693
        2       0.3029  3.337   0.14676
        */

    CREATE TABLE girls (
                "Age" BIGINT, 
                "L" DOUBLE PRECISION, 
                "M" DOUBLE PRECISION, 
                "S" DOUBLE PRECISION
        )

        /*
    3 rows from llm_table table:
        Age     L       M       S
        0       0.3809  3.2322  0.14171
        1       0.3259  3.1957  0.14578
        2       0.3101  3.2104  0.14637
        */
            
    Question: {question}
    SQLQuery: "Only return the generated SQl query"
"""

SQL_SYS = "Given an input question, convert it to a SQL query. No pre-amble."

EXTRACT = """Convert the age value in the question to days. 
Re-write the input question replacing the age with the converted age value. 
If 'newborn' or 'just born' or similar is mentioned in the question then assume the age is 0.
If you cannot convert the age from the question then say so.

Question: {question}
"""

AGE_SYS = """You are a helpful assistant designed to extract age data from input questions. No pre-amble.
"""

ANSWER_SYS = "Given an input question and SQL response, convert it to a natural language answer. No pre-amble."

ANSWER_PROMPT = """
Based on the table schema below, question, sql query, and sql response, write a natural language response:
CREATE TABLE boys (
        "Age" BIGINT, 
        "L" DOUBLE PRECISION, 
        "M" DOUBLE PRECISION, 
        "S" DOUBLE PRECISION, 
)

/*
3 rows from weights table:
Age     L       M       S       
0       0.3487  3.3464  0.14602 
1       0.3127  3.3174  0.14693
2       0.3029  3.337   0.14676
*/

CREATE TABLE girls (
        "Age" BIGINT, 
        "L" DOUBLE PRECISION, 
        "M" DOUBLE PRECISION, 
        "S" DOUBLE PRECISION
)

/*
3 rows from llm_table table:
Age     L       M       S
0       0.3809  3.2322  0.14171
1       0.3259  3.1957  0.14578
2       0.3101  3.2104  0.14637
*/

Question: {question}
SQL Query: {query}
SQL Response: {response}

Answer: "Answer to the question"
"""


def age_template() -> str:
    return ChatPromptTemplate.from_messages(
        [
            ("system", AGE_SYS),
            ("human", EXTRACT),
        ]
    )


def sql_template() -> str:
    return ChatPromptTemplate.from_messages(
        [
            ("system", SQL_SYS),
            ("human", SQL_PROMPT),
        ]
    )


def answer_template() -> str:
    return ChatPromptTemplate.from_messages(
        [
            ("system", ANSWER_SYS),
            ("human", ANSWER_PROMPT),
        ]
    )
