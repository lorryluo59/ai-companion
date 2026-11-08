# AI智能伴侣

一个基于 **Streamlit** 和 **DeepSeek API** 构建的 AI 情感陪伴聊天应用。用户可以自定义伴侣昵称与性格，与 AI 进行流式对话，并将聊天记录保存在本地。

## 功能特点

- 🤖 基于 DeepSeek 大语言模型进行对话
- 💬 支持流式输出，回复实时显示
- 🎭 可自定义伴侣昵称和性格
- 🗂️ 自动保存聊天会话
- 📜 支持新建、切换和删除历史会话
- 🔐 API Key 通过本地 `.env` 文件管理，不写入源码
- 🎨 使用 Streamlit 构建简洁的聊天界面

## 技术栈

- Python 3.9+
- Streamlit
- OpenAI Python SDK（兼容 DeepSeek API）
- DeepSeek Chat API
- JSON 本地会话存储

## 项目结构

```text
AI智能伴侣/
├── .vscode/
│   └── settings.json      # VS Code 环境变量配置
├── sessions/              # 本地聊天记录（不会提交到 Git）
├── .env                   # API Key 等本地配置（不会提交到 Git）
├── .gitignore
├── chat.py                # Streamlit 主程序
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
python3 -m pip install streamlit openai
```

### 2. 配置 DeepSeek API

在项目根目录创建 `.env` 文件：

```dotenv
DEEPSEEK_API_KEY=your_deepseek_api_key
DEEPSEEK_MODEL=deepseek-chat
```

> 请勿将 `.env` 文件提交到 GitHub。项目已在 `.gitignore` 中排除该文件。

### 3. 加载环境变量并启动

在终端中执行：

```bash
set -a
source .env
set +a
streamlit run chat.py
```

如果使用 VS Code，也可以通过项目内的 `.vscode/settings.json` 自动加载 `.env`。

启动后访问：

```text
http://localhost:8501
```

## 使用方法

1. 在左侧控制面板设置伴侣昵称和性格。
2. 在底部输入框中输入消息并发送。
3. AI 会以流式方式返回符合所设置性格的回复。
4. 点击“新建会话”创建新的聊天记录。
5. 在“历史会话”中加载或删除现有会话。

## 数据存储

聊天记录会以 JSON 格式保存在 `sessions/` 目录中。该目录已加入 `.gitignore`，不会提交到远程仓库。

## 安全说明

- API Key 仅保存在本地 `.env` 文件中。
- 不要将 `.env`、聊天记录或包含密钥的截图上传到公开仓库。
- 如果 API Key 意外泄露，请立即前往 DeepSeek 控制台撤销并生成新 Key。

## 许可证

本项目暂未指定开源许可证。
