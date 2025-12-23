@staticmethod
    def create_reranker(config_path: str) -> 'Reranker': # Return type ipucunu Protocol olarak güncelledik
        """Create reranker from configuration."""
        
        # 1. Config dosyasını yükle
        master_config = JsonConfigLoader.load_and_parse(config_path)
        reranker_config = master_config.get("reranker", {})
        
        # 2. Reranker tipini al (Varsayılan: phrase)
        reranker_type = reranker_config.get("type", "phrase")
        
        # 3. İlgili sınıfı döndür (Polymorphism)
        if reranker_type == "jaccard":
            from ..reranker import JaccardReranker # Import ettiğinden emin ol
            return JaccardReranker()
            
        elif reranker_type == "phrase" or reranker_type == "simple":
            from ..reranker import PhraseAwareReranker
            return PhraseAwareReranker()
            
        else:
            raise ValueError(f"Unknown reranker type: {reranker_type}")
