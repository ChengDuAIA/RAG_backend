from nano_graphrag import GraphRAG, QueryParam

import requests


def make_vdb(vdb_id:str,doc_urls:list):
    graph_func = GraphRAG(working_dir="vdbs/"+vdb_id)

    for url in doc_urls:
        try:
            file_bin = requests.get(url).content
            

        except:
            print("Error in downloading the file from url: ", url)
            raise Exception("Error in downloading the file from url: ", url)

    with open("./book.txt") as f:
        graph_func.insert(f.read())

    # Perform global graphrag search
    print(graph_func.query("What are the top themes in this story?"))

    # Perform local graphrag search (I think is better and more scalable one)
    print(graph_func.query("What are the top themes in this story?", param=QueryParam(mode="local")))