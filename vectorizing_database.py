import pandas as pd
from sentence_transformers import SentenceTransformer
import json

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')
df = pd.read_csv('articles_database.csv')
df['text'] = df['text'].astype(str).str.replace('\n', ' ', regex=False).str.replace('\r', '', regex=False)
embeddings = model.encode(df['text'].tolist(), show_progress_bar=True, normalize_embeddings=True)
df['vector'] = embeddings.tolist()
df.to_json('database_with_vectors.json', orient='records', force_ascii=False)
