import httpx
import asyncio
import time

doc_names = ['a_demo', 'b_demo', 'c_demo', 'd_demo']
server_url = "http://localhost:5000/v1/rag/graph"

async def fetch(client, doc):
    # print(f"query doc {doc}")
    data = {
        "query": "这篇文档讲的是什么",
        "doc_name": doc
    }
    response = await client.post(server_url, json=data)
    result = response.json()
    print(result)
    return result

async def main():
    async with httpx.AsyncClient() as client:
        tasks = [fetch(client, doc) for doc in doc_name]
        results = await asyncio.gather(*tasks)
        return results

start_time = time.time()

doc_name = []

for i in range(100):
    doc_name.extend(doc_names)

asyncio.run(main())

end_time = time.time()
print(f"Total time: {end_time - start_time} seconds")
