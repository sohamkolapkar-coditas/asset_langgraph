from langchain_groq import ChatGroq
from app.config.env import settings
from app.utils.constants.llm import ModelName

llm_model = ChatGroq(
    model=ModelName.META.value, api_key=settings.GROQ_API_KEY, temperature=0.5
)
