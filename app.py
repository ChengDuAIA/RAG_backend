from flask import Flask, request, jsonify
import os

from rag_ops import *

os.environ["OPENAI_BASE_URL"] = "https://fast.chat.t4wefan.pub/v1"
os.environ["OPENAI_API_KEY"] = "sk-FnmZsLXWhIBnyf3EDb0e8cA14e7143Ca9002Cc6b7a3d367b"

app = Flask(__name__)

graphs_vdb = {}

# 用于存储Graph的数据
def get_graphs():
    graphs_list = os.listdir("graphs")
    return graphs_list 

graphs = get_graphs()
print(graphs)

@app.route('/v1/rag/graph', methods=['POST'])
def v1_rag_graph_query():
    print("received request")
    data = request.get_json()
    query = data.get('query')
    doc_name = data.get('doc_name')

    if not query or not doc_name:
        print(data)
        return jsonify({"error": "Missing query parameter"}), 400
    
    if doc_name not in graphs:
        return jsonify({"error": "Graph not found"}), 404
    
    # 开始处理
    
    check_vdb(doc_name)

    if doc_name not in graphs_vdb:
        graphs_vdb[doc_name] = init_vdb(doc_name)
    

    vdb = graphs_vdb[doc_name]

    result = query_vdb(query,vdb)
    return jsonify(result)


if __name__ == '__main__':
    app.run()