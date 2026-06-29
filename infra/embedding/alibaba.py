from sentence_transformers import SentenceTransformer

if __name__ == "__main__":
    model = SentenceTransformer(
        "Qwen/Qwen3-Embedding-0.6B",
        trust_remote_code=True
    )
    embeddings = model.encode(
        [
            "人工智能正在改变世界",
            "向量数据库"
        ],
        normalize_embeddings=True
    )
    print(embeddings.shape)
