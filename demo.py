import os
print("loading......")
from llm_utils import *

import asyncio

os.environ["OPENAI_BASE_URL"] = "https://fast.chat.t4wefan.pub/v1"
os.environ["OPENAI_API_KEY"] = "sk-FnmZsLXWhIBnyf3EDb0e8cA14e7143Ca9002Cc6b7a3d367b"


from nano_graphrag import GraphRAG, QueryParam


class gpt_callings:
    sync_gpt_calling = sync_gpt_calling
    gpt_4o_mini = gpt_4o_mini_calling
    gpt_4o = gpt_4o_calling
    gpt_4t = gpt_4t_calling
    def adv_txt2json(txt,model="gpt-4o-mini"):
        return adv_txt2json(txt,model)


working_dir ="./d_demo"

if not os.path.exists(working_dir):
    init_run = True
else:
    init_run = False

if init_run:
    graph_func = GraphRAG(working_dir,
                        best_model_func=gpt_callings.gpt_4o,
                        cheap_model_func=gpt_callings.gpt_4o_mini,
                        convert_response_to_json_func=gpt_callings.adv_txt2json)


    with open("tests/mock_data.txt","r", encoding="utf-8") as f:
        graph_func.insert(f.read())


    print("checking database......")
    for file in os.listdir(working_dir):
        if file.endswith(".json"):
            path = os.path.join(working_dir,file)
            print("find file:",path)
            with open(path,"r") as f:
                correct_json = gpt_callings.adv_txt2json(f.read())
            with open(path,"w") as f:
                f.write(json.dumps(correct_json,indent=4))

else:
    print("checking database......")
    for file in os.listdir(working_dir):
        if file.endswith(".json"):
            path = os.path.join(working_dir,file)
            print("find file:",path)
            with open(path,"r") as f:
                correct_json = gpt_callings.adv_txt2json(f.read())
            with open(path,"w") as f:
                f.write(json.dumps(correct_json,indent=4))
    

    
graph_func = GraphRAG(working_dir,
                        best_model_func=gpt_callings.gpt_4o,
                        cheap_model_func=gpt_callings.gpt_4o_mini,
                        convert_response_to_json_func=gpt_callings.adv_txt2json)




print("===========================================================")
print("load done,start chat")
print("===========================================================")

general_history = []

while True:
    query = str(input("input："))

    general_history.append({
        "role": "user",
        "content": query
    })

    if query == "exit":
        print("exit")
        exit()


    info_str = graph_func.query(query)
    if not info_str.startswith("Sorry, I'm not able to provide"):

        general_history.append({
            "role": "system",
            "content": info_str
        })
        print("Successfully find info in database")
        # event_loop = asyncio.get_event_loop()
        
    
    print("genearting response......")
    gpt_response = sync_gpt_stream_print(model="gpt-4o",prompt=query,history_messages=general_history)

    current_response = ""

    print("AI：", end="",flush=True)
    for chunk in gpt_response:
        
        try:
            chunk_txt = chunk.choices[0].delta.content
            current_response = current_response + chunk_txt
            print(chunk_txt, end="",flush=True)
        except:
            break
    print("")    

    general_history.append({
        "role": "assistant",
        "content": current_response
    })

