import torch
import torch.nn as nn

class AtlasSLM(nn.Module):
    """
    SLM dédié à la structuration et au mapping de données.
    Architecture: Encoder Transformer ultra-léger.
    """
    def __init__(self, vocab_size=5000, embed_dim=128, num_heads=4, num_layers=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.pos_encoder = nn.Parameter(torch.zeros(1, 512, embed_dim))
        
        encoder_layer = nn.TransformerEncoderLayer(d_model=embed_dim, nhead=num_heads, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Têtes spécifiques aux rôles d'ATLAS
        self.tagger = nn.Linear(embed_dim, 50)  # Sortie pour 50 catégories de tags
        self.mapper = nn.Linear(embed_dim, embed_dim) # Espace latent pour le mapping

    def forward(self, x):
        x = self.embedding(x) + self.pos_encoder[:, :x.size(1), :]
        x = self.transformer(x)
        pooled = x.mean(dim=1) # Global Average Pooling
        return self.tagger(pooled), self.mapper(pooled)
