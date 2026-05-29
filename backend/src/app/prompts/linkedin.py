from langchain.prompts import ChatPromptTemplate

linkedin_prompt = ChatPromptTemplate.from_messages([
    ("system", """Eres un experto en contenido para LinkedIn.
Escribe posts profesionales de entre 150 y 300 palabras.
Tono profesional pero cercano. Añade hashtags relevantes al final."""),
    ("human", """Escribe un post de LinkedIn sobre: {topic}
Audiencia: {audience}
Tono: {tone}
Idioma: {language}
{company_context}"""),
])