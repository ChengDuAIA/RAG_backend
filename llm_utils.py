import os
import logging
from openai import AsyncOpenAI,OpenAI

import asyncio
import logging
import json

from typing import Any, Dict, List, Optional, Union

import re

from nano_graphrag.base import BaseKVStorage
from nano_graphrag._utils import compute_args_hash

logging.basicConfig(level=logging.WARNING)
logging.getLogger("nano-graphrag").setLevel(logging.INFO)


os.environ["OPENAI_BASE_URL"] = "https://fast.chat.t4wefan.pub/v1"
os.environ["OPENAI_API_KEY"] = "sk-FnmZsLXWhIBnyf3EDb0e8cA14e7143Ca9002Cc6b7a3d367b"

async def gpt_4o_calling(
    prompt, system_prompt=None, history_messages=[], **kwargs
) -> str:

    MODEL = "gpt-4o-2024-08-06"

    openai_async_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # Get the cached response if having-------------------
    hashing_kv: BaseKVStorage = kwargs.pop("hashing_kv", None)
    messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})
    if hashing_kv is not None:
        args_hash = compute_args_hash(MODEL, messages)
        if_cache_return = await hashing_kv.get_by_id(args_hash)
        if if_cache_return is not None:
            return if_cache_return["return"]
    # -----------------------------------------------------

    response = await openai_async_client.chat.completions.create(
        model=MODEL, messages=messages, **kwargs
    )

    # Cache the response if having-------------------
    if hashing_kv is not None:
        await hashing_kv.upsert(
            {args_hash: {"return": response.choices[0].message.content, "model": MODEL}}
        )
    # -----------------------------------------------------
    return response.choices[0].message.content

async def gpt_4t_calling(
    prompt, system_prompt=None, history_messages=[], **kwargs
) -> str:

    MODEL = "gpt-4-turbo-2024-04-09"

    openai_async_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # Get the cached response if having-------------------
    hashing_kv: BaseKVStorage = kwargs.pop("hashing_kv", None)
    messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})
    if hashing_kv is not None:
        args_hash = compute_args_hash(MODEL, messages)
        if_cache_return = await hashing_kv.get_by_id(args_hash)
        if if_cache_return is not None:
            return if_cache_return["return"]
    # -----------------------------------------------------

    response = await openai_async_client.chat.completions.create(
        model=MODEL, messages=messages, **kwargs
    )

    # Cache the response if having-------------------
    if hashing_kv is not None:
        await hashing_kv.upsert(
            {args_hash: {"return": response.choices[0].message.content, "model": MODEL}}
        )
    # -----------------------------------------------------
    return response.choices[0].message.content

def sync_gpt_calling(model="gpt-4-turbo-2024-04-09",
    prompt="", system_prompt=None, history_messages=[], **kwargs
) -> str:

    MODEL = model

    openai_async_client = OpenAI()
    messages = history_messages
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    response = openai_async_client.chat.completions.create(
        model=MODEL, messages=messages, **kwargs
    )

    return response.choices[0].message.content

def sync_gpt_stream_print(model="gpt-4-turbo-2024-04-09",
    prompt="", system_prompt=None, history_messages=[], **kwargs
) -> str:

    MODEL = model

    openai_async_client = OpenAI()
    messages = history_messages
    
    response = openai_async_client.chat.completions.create(
        model=MODEL, messages=messages, stream=True,**kwargs
    )

    return response


async def gpt_4o_mini_calling(
    prompt, system_prompt=None, history_messages=[], **kwargs
) -> str:

    MODEL = "gpt-4o-mini-2024-07-18"

    openai_async_client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    # Get the cached response if having-------------------
    hashing_kv: BaseKVStorage = kwargs.pop("hashing_kv", None)
    messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})
    if hashing_kv is not None:
        args_hash = compute_args_hash(MODEL, messages)
        if_cache_return = await hashing_kv.get_by_id(args_hash)
        if if_cache_return is not None:
            return if_cache_return["return"]
    # -----------------------------------------------------

    response = await openai_async_client.chat.completions.create(
        model=MODEL, messages=messages, **kwargs
    )

    # Cache the response if having-------------------
    if hashing_kv is not None:
        await hashing_kv.upsert(
            {args_hash: {"return": response.choices[0].message.content, "model": MODEL}}
        )
    # -----------------------------------------------------
    return response.choices[0].message.content

def txt2json(txt):
    input_string = txt

    with open("txt2json_prompt.md", "r", encoding="utf-8") as f:
        system_prompt = f.read()

    
    # 调用 OpenAI 的 GPT-3.5 模型来处理输入字符串
    response = OpenAI.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_string}
            
        ]
    )
    
    
    # 提取生成的文本内容
    json_string = response.choices[0].text.strip()
    
    # 尝试解析生成的文本以确保其是有效的JSON
    try:
        parsed = json.loads(json_string)
    except:
        response = OpenAI.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": input_string}
            
        ]
    )
    
    # 返回格式良好的JSON字符串
    return parsed


def custom_locate_json_string_body_from_string(content: str) -> Union[str, None]:
    """Locate the JSON string body from a string"""
    maybe_json_str = re.search(r"{.*}", content, re.DOTALL)
    if maybe_json_str is not None:
        return maybe_json_str.group(0)
    else:
        return None

def adv_txt2json(response: str) -> dict:
    json_str = custom_locate_json_string_body_from_string(response)
    assert json_str is not None, f"Unable to parse JSON from response: {response}"
    try:
        data = json.loads(json_str)
        return data
    except json.JSONDecodeError as e:

        print(f"Failed to parse JSON: {json_str},retrying using GPT...")

        for i in range(3):
            try:
                data = txt2json(response)
                return data
                
            except Exception as e:
                if i < 3 :
                    print(f"Failed to parse JSON: {e}, retrying...")
                else:
                    raise e
        raise e