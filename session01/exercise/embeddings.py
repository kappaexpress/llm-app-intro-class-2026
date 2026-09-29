"""意味検索。デモでは手作りの数値を使い、APIの精度とは比較しない。"""
import json
import math
import sqlite3
from settings import DEMO_MODE, DATABASE, EMBEDDING_MODEL
from llm import make_client
from knowledge import all_chunks, get_score


def embedding_name():
    if DEMO_MODE:
        return 'demo-word-count-v1'
    return EMBEDDING_MODEL


def embed(text):
    if DEMO_MODE:
        # 数値の流れを見るためだけの疑似ベクトル。意味を理解しない。
        vector = []
        for word in ['sqlite', '保存', 'fetch', '提出', 'api', 'キー', 'css', 'sql']:
            vector.append(float(text.lower().count(word)))
        return vector
    client = make_client()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def cosine_similarity(a, b):
    if len(a) != len(b):
        raise ValueError('ベクトルの長さが違います。再作成してください。')
    dot = 0.0
    a_size = 0.0
    b_size = 0.0
    # BEGIN EXERCISE cosine
    for i in range(len(a)):
        dot += a[i] * b[i]
        a_size += a[i] * a[i]
        b_size += b[i] * b[i]
    # END EXERCISE cosine
    if a_size == 0 or b_size == 0:
        return 0.0
    return dot / (math.sqrt(a_size) * math.sqrt(b_size))


def build_embeddings():
    # 全件成功してからDBを更新し、途中失敗で半分だけの状態にしない。
    values = []
    for chunk in all_chunks():
        text = chunk['title'] + '\n' + chunk['heading'] + '\n' + chunk['body']
        vector = embed(text)
        values.append((json.dumps(vector), embedding_name(), chunk['id']))
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.executemany('UPDATE chunks SET embedding = ?, embedding_model = ? WHERE id = ?', values)
    conn.commit()
    conn.close()
    return len(values)


def search_vector(question, top_k):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, embedding, embedding_model FROM chunks ORDER BY id')
    rows = cursor.fetchall()
    conn.close()
    vectors = {}
    for row in rows:
        if row[1] is None or row[2] != embedding_name():
            raise ValueError('このモードのベクトルがありません。python build_index.py を実行してください。')
        vectors[row[0]] = json.loads(row[1])
    if not rows:
        return []
    query_vector = embed(question)
    results = []
    for chunk in all_chunks():
        chunk['score'] = cosine_similarity(query_vector, vectors[chunk['id']])
        if chunk['score'] > 0:
            results.append(chunk)
    results.sort(key=get_score, reverse=True)
    # 類似度は正答確率ではない。関連がない上位結果も評価で見つける。
    return results[:top_k]
