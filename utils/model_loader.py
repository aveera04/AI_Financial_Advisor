import os
from dotenv import load_dotenv
from typing import Literal, Optional, Any
from pydantic import BaseModel, Field
from utils.config_loader import load_config
from langchain_groq import ChatGroq
from logger.logger import get_logger

# Load environment variables first
load_dotenv()

# Setup logger
logger = get_logger("model_loader")

class ConfigLoader:
    def __init__(self):
        logger.info("Loading configuration")
        self.config = load_config()
    
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq_oss", "groq_oss_20b", "groq_lamma_8b_instant", "gemini_2.5_pro"] = "groq_oss"
    api_key: str = Field(..., description="API key for the model provider")  # Mandatory parameter
    api_key_source: Optional[str] = Field(default=None, description="Source of the API key")
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        self.config = ConfigLoader()
        # Validate that api_key is provided
        if not self.api_key:
            raise ValueError("API key is mandatory and cannot be empty")
    
    class Config:
        arbitrary_types_allowed = True
    
    def load_llm(self):
        """
        Load and return the LLM model with specified API key.
        """
        logger.info("Loading LLM model")
        logger.debug(f"Loading model from provider: {self.model_provider}")

        # Show both the source and masked key
        if self.api_key_source:
            logger.debug(f"Using API key from: {self.api_key_source}")
        logger.debug(f"API key value: {self.api_key[:8]}...{self.api_key[-4:] if len(self.api_key) > 12 else 'short_key'}")

        if self.model_provider in ["groq_oss", "groq_oss_20b", "groq_lamma_8b_instant", "gemini_2.5_pro"]:
            logger.debug(f"Loading LLM with config: {self.model_provider}")
            model_name = self.config["llm"][self.model_provider]["model_name"]
            logger.info(f"Using model: {model_name} with provided API key")
            llm = ChatGroq(model=model_name, api_key=self.api_key)
        # elif self.model_provider == "openai":
        #     logger.debug("Loading LLM from OpenAI")
        #     openai_api_key = os.getenv("OPENAI_API_KEY")
        #     model_name = self.config["llm"]["openai"]["model_name"]
        #     logger.info(f"Using OpenAI model: {model_name}")
        #     llm = ChatOpenAI(model_name="o4-mini", api_key=openai_api_key)
        else:
            error_msg = f"Unsupported model provider: {self.model_provider}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        return llm
    
    @classmethod
    def from_env_key(cls, model_provider: str, env_key_name: str):
        """
        Convenience method to create ModelLoader using environment variable.
        
        Usage:
            loader = ModelLoader.from_env_key("groq_oss", "GROQ_API_KEY")
            loader = ModelLoader.from_env_key("groq_search_20b", "GROQ_API_KEY_2")
        """
        api_key = os.getenv(env_key_name)
        if not api_key:
            raise ValueError(f"Environment variable {env_key_name} is not set")
        
        logger.info(f"Creating ModelLoader with API key from: {env_key_name}")
        # Pass the environment variable name as source
        return cls(
            model_provider=model_provider, 
            api_key=api_key,
            api_key_source=env_key_name  # Track the source
        )
    
    def get_model_info(self) -> dict:
        """
        Get model information including provider, model name, and API key source.
        """
        if not self.config:
            self.config = ConfigLoader()
            
        model_config = self.config["llm"][self.model_provider]
        
        return {
            "provider": model_config.get("provider", "Unknown"),
            "model_name": model_config.get("model_name", "Unknown"),
            "api_key_source": self.api_key_source or "Direct",
            "model_provider": self.model_provider
        }