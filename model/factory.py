import os
from abc import ABC
from abc import abstractmethod
from langchain_community.chat_models.tongyi import ChatTongyi, BaseChatModel
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings
from typing import Optional
from utils.config_handler import rag_conf


# 从环境变量读取百炼平台 API Key 和自定义端点
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
DASHSCOPE_API_BASE = os.getenv("DASHSCOPE_API_BASE")
# dashscope SDK 也识别 DASHSCOPE_HTTP_BASE_URL，兼容设置
if DASHSCOPE_API_BASE and not os.getenv("DASHSCOPE_HTTP_BASE_URL"):
    os.environ["DASHSCOPE_HTTP_BASE_URL"] = DASHSCOPE_API_BASE


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(
            model=rag_conf["chat_model_name"],
            dashscope_api_key=DASHSCOPE_API_KEY,
        )


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(
            model=rag_conf["embedding_model_name"],
            dashscope_api_key=DASHSCOPE_API_KEY,
        )


chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()
