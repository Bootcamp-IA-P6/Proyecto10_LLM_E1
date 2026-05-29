from langchain.prompts import ChatPromptTemplate

twitter_prompt = ChatPromptTemplate.from_messages([
    ("system", """Eres un experto en Twitter/X.
Crea hilos de 5 tweets impactantes, cada uno de máximo 280 caracteres.
Usa hashtags relevantes y emojis. Numera cada tweet (1/5, 2/5, etc.)."""),
    ("human", """Crea un hilo de Twitter sobre: {topic}
Audiencia: {audience}
Tono: {tone}
Idioma: {language}
{company_context}"""),
])