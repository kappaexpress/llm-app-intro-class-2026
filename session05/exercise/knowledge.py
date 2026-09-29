"""資料の読み込みと検索。1つの関数を順番に追える書き方にする。"""
import sqlite3
from settings import BASE_DIR, DATABASE


def read_documents():
    # ファイル名順に読み、## 見出しごとに分割する。
    chunks = []
    for path in sorted((BASE_DIR / 'data').glob('*.md')):
        title = path.stem
        heading = '本文'
        lines = []
        for line in path.read_text(encoding='utf-8').splitlines():
            if line.startswith('# '):
                title = line[2:]
            elif line.startswith('## '):
                add_chunk(chunks, path.name, title, heading, lines)
                heading = line[3:]
                lines = []
            else:
                lines.append(line)
        add_chunk(chunks, path.name, title, heading, lines)
    if len(chunks) > 100:
        raise ValueError('教材では資料を100断片以内にしてください。')
    return chunks


def add_chunk(chunks, source, title, heading, lines):
    body = '\n'.join(lines).strip()
    if body:
        # 巨大な段落は見出しを追加して人が分割する。途中で黙って切らない。
        if len(body) > 1000:
            raise ValueError(source + ': 1つの見出しの本文は1000文字以内にしてください。')
        chunks.append({'source': source, 'title': title, 'heading': heading, 'body': body})


def init_documents():
    chunks = read_documents()  # 失敗する場合、元のDBを変更する前に止まる。
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS chunks (
        id INTEGER PRIMARY KEY, source TEXT, title TEXT, heading TEXT, body TEXT,
        embedding TEXT, embedding_model TEXT
    )''')
    # data/ が原本。再登録時に削除した資料も反映し、古いベクトルも消す。
    cursor.execute('DELETE FROM chunks')
    for number, chunk in enumerate(chunks, start=1):
        cursor.execute(
            'INSERT INTO chunks (id, source, title, heading, body) VALUES (?, ?, ?, ?, ?)',
            (number, chunk['source'], chunk['title'], chunk['heading'], chunk['body']),
        )
    conn.commit()
    conn.close()
    return len(chunks)


def all_chunks():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, source, title, heading, body FROM chunks ORDER BY id')
    rows = cursor.fetchall()
    conn.close()
    chunks = []
    for row in rows:
        chunks.append({'id': row[0], 'source': row[1], 'title': row[2],
                       'heading': row[3], 'body': row[4]})
    return chunks


def search_keyword(search_text, top_k):
    # 日本語の形態素解析を省く。検索欄に「SQLite 保存」と空白区切りで入力する。
    words = search_text.lower().split()
    results = []
    for chunk in all_chunks():
        text = (chunk['title'] + ' ' + chunk['heading'] + ' ' + chunk['body']).lower()
        score = 0
        # TODO: 単語ごとの一致件数を加算する
        # for word in words:
        #     if word in text:
        #         score += 1
        raise NotImplementedError('TODO: 単語ごとの一致件数を加算する')
        if score > 0:
            chunk['score'] = score
            results.append(chunk)
    results.sort(key=get_score, reverse=True)
    return results[:top_k]


def get_score(chunk):
    return chunk['score']
