# backend/rag/rag_engine.py
import os
from pathlib import Path
import numpy as np
import faiss
from .embedder import embed_text

class RagEngine:
    """
    Simple FAISS-backed RAG engine.
    Loads all .txt files from data/medical_docs and builds embeddings.
    """
    def __init__(self, docs_dir="../../data/medical_docs", dim: int = None):
        self.docs_dir = Path(docs_dir).resolve()
        self.documents = []
        self.ids = []
        self.embeddings = None
        self.index = None

        self._load_docs()
        if self.documents:
            # create embeddings for each document (list of lists)
            embs = [embed_text(d) for d in self.documents]
            import numpy as np
            self.embeddings = np.array(embs).astype("float32")
            dim = self.embeddings.shape[1]
            # create index
            self.index = faiss.IndexFlatL2(dim)
            self.index.add(self.embeddings)
        else:
            # empty index
            self.index = None

    def _load_docs(self):
        if not self.docs_dir.exists():
            raise FileNotFoundError(f"{self.docs_dir} does not exist.")
        for fname in sorted(os.listdir(self.docs_dir)):
            if fname.endswith(".txt"):
                path = self.docs_dir / fname
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                    self.documents.append(text)
                    self.ids.append(fname)

    def query(self, query_text: str, top_k: int = 3):
        """
        Returns list of top_k documents (as strings). If index not built, returns []
        """
        if self.index is None:
            return []
        q_emb = embed_text(query_text)
        import numpy as np
        q = np.array([q_emb]).astype("float32")
        distances, idxs = self.index.search(q, top_k)
        results = []
        for i in idxs[0]:
            if i < len(self.documents):
                results.append(self.documents[i])
        return results
