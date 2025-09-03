# app/services/embeddings_service.py
from transformers import AutoTokenizer, AutoModel
import torch

class EmbeddingsService:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)

    def chunk_text(self, text: str, max_tokens: int = 500):
        """Split text into chunks based on token length."""
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        chunks = []
        for i in range(0, len(tokens), max_tokens):
            chunk_tokens = tokens[i:i+max_tokens]
            chunk_text = self.tokenizer.decode(chunk_tokens)
            chunks.append(chunk_text)
        return chunks

    def embed_texts(self, texts: list[str]):
        """Generate embeddings for list of texts."""
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            model_output = self.model(**inputs)
        embeddings = model_output.last_hidden_state.mean(dim=1)  # simple mean pooling
        return embeddings.numpy().tolist()
