import os
print("loading......")
from llm_utils import *

from nano_graphrag import GraphRAG, QueryParam


global_graph_dir = 'graphs'


class gpt_callings:
    sync_gpt_calling = sync_gpt_calling
    gpt_4o_mini = gpt_4o_mini_calling
    gpt_4o = gpt_4o_calling
    gpt_4t = gpt_4t_calling
    def adv_txt2json(txt,model="gpt-4o-mini"):
        return adv_txt2json(txt,model)

def init_vdb(doc_name):
    working_dir = os.path.join(global_graph_dir,doc_name)
    graph_func = GraphRAG(working_dir,
                        best_model_func=gpt_callings.gpt_4o_mini,
                        cheap_model_func=gpt_callings.gpt_4o_mini,
                        convert_response_to_json_func=gpt_callings.adv_txt2json,
                        )
    return graph_func


def check_vdb(doc_name):
    working_dir = os.path.join(global_graph_dir,doc_name)
    print("checking database......")
    for file in os.listdir(working_dir):
        if file.endswith(".json"):
            path = os.path.join(working_dir,file)
            print("find file:",path)
            with open(path,"r",encoding="utf-8") as f:
                correct_json = gpt_callings.adv_txt2json(f.read())
            with open(path,"w",encoding="utf-8") as f:
                f.write(json.dumps(correct_json,indent=4))


def query_vdb(query,vdb):

    query_result:str = vdb.query(query,)

    if query_result.startswith("Sorry, I'm not able to provide"):
        return {
            "status": "failed",
            "result": query_result
        }
    else:
        return {
            "status": "success",
            "result": query_result
        }

def create_vdb(doc_name,doc_content):
    working_dir = os.path.join(global_graph_dir,doc_name)

    vdb = init_vdb(doc_name)

    vdb.insert(doc_content)
    return vdb


if __name__ == "__main__":

    from tqdm import tqdm

    doc_list = os.listdir("selected_mds")
    for doc in tqdm(doc_list):

        if os.path.exists(os.path.join(global_graph_dir,doc.split(".")[0])):
            check_vdb(doc.split(".")[0])

        doc_name = doc.split(".")[0]
        doc_content = ""
        with open("selected_mds/"+doc,"r",encoding="utf-8") as f:
            doc_content = f.read()
        print(f"creating vdb for {doc_name}......")
        create_vdb(doc_name,doc_content)
    
    # with open("水文仪器安全要求.md","r",encoding="utf-8") as f:
    #     doc_content = f.read()
    # create_vdb("test",doc_content)