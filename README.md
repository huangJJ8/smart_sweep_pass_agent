# 智扫通 · Smart Customer-Service Agent

> 基于 **LangChain / LangGraph + ReAct Agent + RAG** 的扫地机器人智能客服，支持多工具调用、
> 中间件控制、动态提示词切换与流式对话。

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white">
  <img alt="LangGraph" src="https://img.shields.io/badge/LangGraph-ReAct-1C3C3C">
  <img alt="RAG" src="https://img.shields.io/badge/RAG-ChromaDB-FF6F00">
  <img alt="Qwen" src="https://img.shields.io/badge/LLM-Qwen3--Max-615CED">
  <img alt="Streamlit" src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white">
</p>

**English summary** — A customer-service agent for robot vacuums built on LangGraph's ReAct
loop, with RAG over a product knowledge base (ChromaDB + Qwen embeddings), 7 tools, and a
**middleware layer** that controls the agent runtime: tool-call monitoring, model-call logging,
dynamic prompt switching and log redaction. The middleware is the interesting part — it shows
how an agent runtime can be *observed and steered*, not just prompted.

---

## 🧩 项目架构

```text
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

---

## ✨ 核心特性

| 特性 | 说明 |
| --- | --- |
| **ReAct Agent** | 基于 LangGraph `create_agent`，思考-行动-观察循环 |
| **RAG 检索增强** | ChromaDB 向量存储 + 通义千问 Embedding，支持 PDF/TXT/CSV 知识库 |
| **多工具调用** | 7 个工具：RAG 检索、天气查询、用户定位、ID 获取、月份、外部数据、报告上下文 |
| **动态提示词切换** | 中间件根据上下文自动在「普通对话」和「报告生成」提示词间切换 |
| **流式输出** | Streamlit 前端实时流式显示 Agent 回复 |
| **中间件体系** | 工具调用监控 → 模型调用日志 → 动态提示词注入 |
| **日志脱敏** | 自动过滤 API Key、手机号、邮箱等敏感信息 |
| **MD5 去重** | 知识库文件 MD5 校验，避免重复向量化 |

---

## 🔌 中间件：让 Agent Runtime 可观测、可干预

这是本项目最值得深挖的部分。中间件挂在 Agent 执行链路上，**不改业务代码**就能：

```text
工具调用发生
     │
     ├─► ① 工具调用监控   记录调用了哪个工具、入参、耗时、成功/失败
     │
     ├─► ② 模型调用日志   记录每轮 LLM 请求与响应（含 token 用量）
     │
     └─► ③ 动态提示词注入 检测到「报告」意图 → 切换到 report_prompt.txt
```

配套的日志脱敏过滤器保证了：即使把整个日志文件交给外部排障，也不会泄露 API Key
和用户隐私字段。

---

## 🛠️ 工具一览

> ⚠️ **请注意：带「模拟」标记的工具是本项目的 Demo 替身**，用于在无外部依赖的情况下
> 完整演示 Agent 的多工具编排能力。它们**不是**真实的生产接口。

| 工具函数 | 功能 | 类型 |
| --- | --- | --- |
| `rag_summarize` | 从向量知识库中检索扫地机器人相关参考资料 | ✅ 真实（ChromaDB 检索） |
| `fetch_external_data` | 检索用户指定月份的机器人使用记录 | ⚠️ 模拟（读取仓库内 CSV） |
| `fill_context_for_report` | 触发报告生成场景的动态上下文注入 | ✅ 真实（提示词切换） |
| `get_weather` | 获取指定城市天气信息 | ⚠️ 模拟（返回模拟天气数据） |
| `get_user_location` | 获取用户所在城市 | ⚠️ 模拟（返回随机城市） |
| `get_user_id` | 获取当前用户 ID | ⚠️ 模拟（返回随机用户 ID） |
| `get_current_month` | 获取当前月份 | ⚠️ 模拟（返回随机月份） |

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- 通义千问 / DashScope API Key（环境变量 `DASHSCOPE_API_KEY`）

### 安装依赖

```bash
pip install streamlit langchain langchain-community langchain-chroma langgraph \
            langchain-text-splitters pypdf pyyaml
```

### 配置

```bash
export DASHSCOPE_API_KEY="sk-xxxxxxxxxxxxxxxx"
```

（可选）修改模型配置 `config/rag.yml`：

```yaml
chat_model_name: qwen3-max                  # 对话模型
embedding_model_name: text-embedding-v4     # 向量化模型
```

### 初始化知识库

```bash
python -c "from rag.vector_store import VectorStoreService; VectorStoreService().load_document()"
```

### 启动服务

```bash
streamlit run app.py
```

浏览器访问 `http://localhost:8501` 即可开始对话。

### 命令行测试（无需 Streamlit）

```bash
python agent/react_agent.py
```

---

## 📊 工作流程

```text
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

---

## 🏭 生产化扩展（Production Extension）

当前项目用 Mock 工具演示完整的工具编排链路。真实落地时，工具层的演进路径是：

```text
Mock Tool（当前）
   ↓
HTTP API Tool       调用真实业务接口（带鉴权 / 重试 / 超时）
   ↓
MCP Tool            以 MCP Server 形式暴露，供任意 Agent 复用
   ↓
Database Tool       只读、白名单的受控查询
   ↓
Enterprise Service  接入企业级服务，带权限、审计与限流
```

每一步都只需要替换 `agent/tools/` 下的实现，**Agent 的编排逻辑无需改动**——这正是
把「工具定义」与「Agent 循环」分离的价值所在。

---

## 🔧 技术栈

| 组件 | 技术选型 |
| --- | --- |
| LLM | 通义千问 Qwen3-Max (DashScope) |
| Embedding | text-embedding-v4 (DashScope) |
| Agent 框架 | LangGraph `create_agent` (ReAct) |
| 向量数据库 | ChromaDB |
| 前端 | Streamlit |
| 配置管理 | YAML |
| 日志 | Python logging + 敏感信息脱敏 |

---

## 📝 License

仅供学习参考，请勿用于商业用途。
