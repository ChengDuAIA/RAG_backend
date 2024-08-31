## 简介

本项目演示了如何使用 `GraphRAG` 进行对话生成，并结合了多种 GPT 模型的调用。用户可以通过该项目实现简单的交互式对话体验。

## 先决条件

在开始之前，请确保你已经安装了以下依赖项：

- Python 3.10.6
- 依赖库，可以通过 `requirements.txt` 文件来安装

## 安装依赖

请在项目的根目录下运行以下命令来安装所需的依赖项：

```sh
pip install -r requirements.txt
```

## 配置环境变量

请在运行项目之前，设置以下环境变量：

- `OPENAI_BASE_URL`: OpenAI 接口的基础 URL
- `OPENAI_API_KEY`: 你的 OpenAI API 密钥

你可以在代码中直接设置这些环境变量：
demo里面暂时写死了(不安全，以后会改)

```python
import os

os.environ["OPENAI_BASE_URL"] = "https://fast.chat.t4wefan.pub/v1"
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
```

记得将 `your_openai_api_key` 替换为你的实际 API 密钥。

## 运行 Demo

1. 请确保在 `working_dir` 目录下有一些初始数据文件，例如 `tests/mock_data.txt`。
2. 运行 `demo.py`：

```sh
python demo.py
```

## 使用方法

程序启动后，会提示你输入对话内容。你可以根据提示输入问题或指令，系统会生成相应的回复。

输入 "exit" 可以退出程序。

示例：

```sh
input：你好
AI：你好！请问有什么我可以帮助你的吗？
```