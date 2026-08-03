# 🤖 智扫通 — 智能客服 Agent 系统

基于 **LangChain / LangGraph + ReAct Agent + RAG** 架构的扫地/扫拖机器人智能客服，支持多工具调用、动态提示词切换和流式对话。

> 📺 本仓库为 B 站课程《AI大模型RAG与Agent智能体开发项目实战课程》配套代码。
>
> 🎓 讲师：小曹老师 · [B站主页](https://space.bilibili.com/1032221418) · [课程地址](https://www.bilibili.com/video/BV1yjz5BLEoY)

---

## 🧩 项目架构

```
zst_agent-master/
├── app.py                      # 🚀 Streamlit Web 入口
├── agent/
│   ├── react_agent.py          # ReAct Agent 核心（基于 LangGraph create_agent）
│   └── tools/
│       ├── agent_tools.py      # 🧰 工具定义（7 个工具）
│       └── middleware.py       # 🔌 中间件（监控/日志/动态提示词切换）
├── model/
│   └── factory.py              # 🏭 模型工厂（通义千问 + DashScope Embedding）
├── rag/
│   ├── vector_store.py         # 📚 ChromaDB 向量存储 + 文档加载
│   └── rag_service.py          # 🔍 RAG 检索增强生成服务
├── config/
│   ├── rag.yml                 # 模型配置
│   ├── chroma.yml              # 向量库 & 分片配置
│   ├── prompts.yml             # 提示词文件路径
│   └── agent.yml               # Agent 外部数据路径
├── prompts/
│   ├── main_prompt.txt         # 主对话系统提示词
│   ├── rag_summarize.txt       # RAG 摘要提示词
│   └── report_prompt.txt       # 报告生成提示词（动态切换）
├── data/
│   ├── 扫地机器人100问.pdf      # 知识库文档
│   ├── 扫地机器人100问2.txt
│   ├── 扫拖一体机器人100问.txt
│   ├── 故障排除.txt
│   ├── 维护保养.txt
│   ├── 选购指南.txt
│   └── external/
│       └── records.csv         # 用户使用记录（模拟外部数据）
└── utils/
    ├── config_handler.py       # YAML 配置加载
    ├── prompt_loader.py        # 提示词文件加载
    ├── file_handler.py         # 文件处理（MD5 / 文档加载器）
    ├── logger_handler.py       # 日志系统（含脱敏过滤器）
    ├── path_tools.py           # 路径工具
    └── chain_debug.py          # Chain 调试工具
```

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| **ReAct Agent** | 基于 LangGraph `create_agent`，思考-行动-观察循环 |
| **RAG 检索增强** | ChromaDB 向量存储 + 通义千问 Embedding，支持 PDF/TXT/CSV 知识库 |
| **多工具调用** | 7 个工具：RAG 检索、天气查询、用户定位、ID 获取、月份、外部数据、报告上下文 |
| **动态提示词切换** | 中间件根据上下文自动在「普通对话」和「报告生成」提示词间切换 |
| **流式输出** | Streamlit 前端实时流式显示 Agent 回复 |
| **中间件体系** | 工具调用监控 → 模型调用日志 → 动态提示词注入 |
| **日志脱敏** | 自动过滤 API Key、手机号、邮箱等敏感信息 |
| **MD5 去重** | 知识库文件 MD5 校验，避免重复向量化 |

## 🛠️ 工具一览

| 工具函数 | 功能 |
|----------|------|
| `rag_summarize` | 从向量知识库中检索扫地机器人相关参考资料 |
| `get_weather` | 获取指定城市天气信息 |
| `get_user_location` | 获取用户所在城市 |
| `get_user_id` | 获取当前用户 ID |
| `get_current_month` | 获取当前月份 |
| `fetch_external_data` | 检索用户指定月份的机器人使用记录 |
| `fill_context_for_report` | 触发报告生成场景的动态上下文注入 |

## 🚀 快速开始

### 环境要求

- Python 3.10+
- 通义千问 / DashScope API Key（需配置环境变量 `DASHSCOPE_API_KEY`）

### 安装依赖

```bash
pip install streamlit langchain langchain-community langchain-chroma langgraph langchain-text-splitters pypdf pyyaml
```

### 配置

1. 设置 API Key：
   ```bash
   export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
   ```

2. （可选）修改模型配置：[config/rag.yml](config/rag.yml)
   ```yaml
   chat_model_name: qwen3-max          # 对话模型
   embedding_model_name: text-embedding-v4  # 向量化模型
   ```

3. （可选）修改向量库配置：[config/chroma.yml](config/chroma.yml)

### 初始化知识库

首次运行前需要加载知识库文档到 ChromaDB：

```bash
python -c "from rag.vector_store import VectorStoreService; VectorStoreService().load_document()"
```

### 启动服务

```bash
streamlit run app.py
```

浏览器访问 `http://localhost:8501` 即可开始对话。

## 🧪 命令行测试

也可以直接在终端测试 Agent（无需启动 Streamlit）：

```bash
python agent/react_agent.py
```

## 📊 工作流程

```
用户提问 → Streamlit UI
    ↓
ReactAgent.execute_stream()
    ↓
LangGraph Agent (ReAct 循环)
    ├── 思考 (LLM 推理)
    ├── 选择工具调用
    │   ├── rag_summarize    → ChromaDB 向量检索 → LLM 生成回答
    │   ├── get_weather      → 返回模拟天气数据
    │   ├── get_user_location → 返回随机城市
    │   ├── get_user_id      → 返回随机用户ID
    │   ├── get_current_month → 返回随机月份
    │   ├── fetch_external_data → 读取外部CSV数据
    │   └── fill_context_for_report → 触发提示词切换
    ├── 观察 (工具结果)
    └── 输出最终回答
    ↓
流式返回 → Streamlit 界面显示
```

## 🔧 技术栈

| 组件 | 技术选型 |
|------|----------|
| LLM | 通义千问 Qwen3-Max (DashScope) |
| Embedding | text-embedding-v4 (DashScope) |
| Agent 框架 | LangGraph `create_agent` (ReAct) |
| 向量数据库 | ChromaDB |
| 前端 | Streamlit |
| 配置管理 | YAML |
| 日志 | Python logging + 敏感信息脱敏 |

## 📝 License

仅供学习参考，请勿用于商业用途。

---

> 💡 更多 AI Agent 开发技巧，欢迎关注 [小曹老师 B站主页](https://space.bilibili.com/1032221418)！
