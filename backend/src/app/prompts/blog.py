from langchain.prompts import ChatPromptTemplate

blog_prompt = ChatPromptTemplate.from_messages([
    ("system", """Eres un experto redactor de contenido para blogs.
Escribe artículos optimizados para SEO, bien estructurados con H2 y H3,
con una llamada a la acción al final. Longitud aproximada: 500 palabras."""),
    ("human", """Escribe un artículo de blog sobre: {topic}
Audiencia: {audience}
Tono: {tone}
Idioma: {language}
{company_context}"""),
])