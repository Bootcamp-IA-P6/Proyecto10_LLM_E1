from langchain.prompts import ChatPromptTemplate

instagram_prompt = ChatPromptTemplate.from_messages([
    ("system", """Eres un experto en contenido para Instagram.
Escribe captions creativos y atractivos con emojis.
Incluye hasta 30 hashtags relevantes al final."""),
    ("human", """Escribe un caption de Instagram sobre: {topic}
Audiencia: {audience}
Tono: {tone}
Idioma: {language}
{company_context}"""),
])