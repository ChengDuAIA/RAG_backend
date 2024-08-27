from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from flask_pydantic import validate

app = Flask(__name__)

# 用于存储Graph的数据
graphs = {}

class CreateGraphModel(BaseModel):
    graphKey: str
    documentUrl: list

class UpdateGraphModel(BaseModel):
    graphKey: str
    documentUrl: list

class ChatCompletionModel(BaseModel):
    graphKey: str
    msg: str

@app.route('/v1/rag/createGraph', methods=['POST'])
@validate()
def create_graph(body: CreateGraphModel):
    graph_key = body.graphKey
    document_urls = body.documentUrl
    
    graphs[graph_key] = {
        "documentUrls": document_urls
    }
    
    return jsonify({"message": f"Graph with key {graph_key} created successfully"}), 201

@app.route('/v1/rag/updateGraph', methods=['POST'])
@validate()
def update_graph(body: UpdateGraphModel):
    graph_key = body.graphKey
    document_urls = body.documentUrl
    
    if graph_key not in graphs:
        return jsonify({"error": "Graph not found"}), 404
    
    graphs[graph_key]["documentUrls"] = document_urls
    
    return jsonify({"message": f"Graph with key {graph_key} updated successfully"}), 200

@app.route('/v1/rag/chatCompletion', methods=['POST'])
@validate()
def chat_completion(body: ChatCompletionModel):
    graph_key = body.graphKey
    msg = body.msg
    
    if graph_key not in graphs:
        return jsonify({"error": "Graph not found"}), 404
    
    # 这里你可以添加实际的对话逻辑处理，下面是一个简单的模拟响应
    response = f"You said: {msg}. This response is based on the graph with key {graph_key}."
    
    return jsonify({"response": response}), 200

if __name__ == '__main__':
    app.run(debug=True)