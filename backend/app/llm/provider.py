from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import os
import logging
from app.core.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, messages: List[Dict[str, str]], **kwargs) -> str:
        pass

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        return await self.complete(messages, **kwargs)

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        self.api_key = api_key
        self.model = model
        self.client = None
        if api_key and api_key != "mock-key":
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=api_key)
                logger.info(f"OpenAI client initialized with model {model}")
            except ImportError:
                logger.warning("OpenAI package not installed. Running in mock mode.")
        else:
            logger.warning("OpenAI API key not set. Running in mock mode.")
    
    async def complete(self, messages: List[Dict[str, str]], **kwargs) -> str:
        if self.client:
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    **kwargs
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"OpenAI API error: {e}. Falling back to mock.")
        
        return f"OpenAI (MOCK: {self.model}) response to: {messages[-1]['content'][:50]}..."

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.api_key = api_key
        self.model = model
        self.client = None
        if api_key and api_key != "mock-key":
            try:
                from anthropic import AsyncAnthropic
                self.client = AsyncAnthropic(api_key=api_key)
                logger.info(f"Anthropic client initialized with model {model}")
            except ImportError:
                logger.warning("Anthropic package not installed. Running in mock mode.")
        else:
            logger.warning("Anthropic API key not set. Running in mock mode.")
    
    async def complete(self, messages: List[Dict[str, str]], **kwargs) -> str:
        if self.client:
            try:
                system_msg = ""
                user_messages = []
                for m in messages:
                    if m["role"] == "system":
                        system_msg = m["content"]
                    else:
                        user_messages.append(m)
                
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    system=system_msg,
                    messages=user_messages,
                    **kwargs
                )
                return response.content[0].text
            except Exception as e:
                logger.error(f"Anthropic API error: {e}. Falling back to mock.")

        return f"Anthropic (MOCK: {self.model}) response to: {messages[-1]['content'][:50]}..."

def get_llm_provider(provider_name: Optional[str] = None, **kwargs) -> LLMProvider:
    if not provider_name:
        provider_name = os.getenv("LLM_PROVIDER", "openai")
    
    if provider_name.lower() == "openai":
        api_key = settings.OPENAI_API_KEY
        return OpenAIProvider(api_key=api_key, **kwargs)
    elif provider_name.lower() == "anthropic":
        api_key = settings.ANTHROPIC_API_KEY
        return AnthropicProvider(api_key=api_key, **kwargs)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")
