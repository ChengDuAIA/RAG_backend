from flask import Flask, request, jsonify

app = Flask(__name__)

# 用于存储Graph的数据
graphs = {}

@app.route('/v1/rag/createGraph', methods=['POST'])
def create_graph():
    data = request.get_json()
    graph_key = data.get('graphKey')
    document_urls = data.get('documentUrl')
    
    if not graph_key or not document_urls:
        return jsonify({"error": "graphKey and documentUrl are required"}), 400
    
    graphs[graph_key] = {
        "documentUrls": document_urls
    }
    
    return jsonify({"message": f"Graph with key {graph_key} created successfully"}), 201

@app.route('/v1/rag/updateGraph', methods=['POST'])
def update_graph():
    data = request.get_json()
    graph_key = data.get('graphKey')
    document_urls = data.get('documentUrl')
    
    if not graph_key or not document_urls:
        return jsonify({"error": "graphKey and documentUrl are required"}), 400

    if graph_key not in graphs:
        return jsonify({"error": "Graph not found"}), 404
    
    graphs[graph_key]["documentUrls"] = document_urls
    
    return jsonify({"message": f"Graph with key {graph_key} updated successfully"}), 200

@app.route('/v1/rag/chatCompletion', methods=['POST'])
def chat_completion():
    data = request.get_json()
    graph_key = data.get('graphKey')
    msg = data.get('msg')
    
    if not graph_key or not msg:
        return jsonify({"error": "graphKey and msg are required"}), 400

    if graph_key not in graphs:
        return jsonify({"error": "Graph not found"}), 404
    
    # 这里你可以添加实际的对话逻辑处理，下面是一个简单的模拟响应
    response = f"You said: {msg}. This response is based on the graph with key {graph_key}."
    
    return jsonify({"response": response}), 200

if __name__ == '__main__':
    app.run(debug=True)