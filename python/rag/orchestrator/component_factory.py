"""Component factory for creating pipeline stages."""

from typing import TYPE_CHECKING
from typing import Dict, List, Any
from ..detector import Intent, RuleIntentDetector
if TYPE_CHECKING:
    from ..writer import HeuristicQueryWriter
from ..retriever import SimpleRetriever, KeywordIndex
from ..reranker.reranker import Reranker, PhraseAwareReranker, JaccardReranker
from ..retriever import SimpleRetriever, KeywordIndex, CacheRetriever
from ..reranker import PhraseAwareReranker
from ..answer import TemplateAnswerAgent
from ..model import ChunkStore
from ..utility import ChunkStoreLoader, JsonConfigLoader
from ..embedding import DeterministicHashEmbeddingProvider, HashEmbeddingConfig
from ..retriever import VectorRetriever, VectorIndex
from ..retriever.vector_retriever import VectorRetrieverConfig
import os
import json
from ..policy import PolicyRerouter, KeywordPolicyRerouter


class ComponentFactory:

    """Factory for creating pipeline components."""
    
    @staticmethod
    def _get_config_section(master_config: Dict[str, Any], section_key: str) -> Dict[str, Any]:
        """Get a configuration section."""
        if section_key not in master_config:
            raise ValueError(f"Master config is missing section: {section_key}")
        return master_config[section_key]
    
    @staticmethod
    def create_chunk_store(config_path: str) -> ChunkStore:
        """Create chunk store from configuration."""
        master_config = JsonConfigLoader.load_and_parse(config_path)
        data_config = ComponentFactory._get_config_section(master_config, "data_paths")
        chunk_path = data_config.get("chunk_file_path")
        
        if not chunk_path:
            raise ValueError("Config error: 'chunk_file_path' is missing in 'data_paths' section")
        
        return ChunkStoreLoader.load(chunk_path)
    
    @staticmethod
    def create_intent_detector(config_path: str) -> RuleIntentDetector:
        """Create intent detector from configuration."""
        master_config = JsonConfigLoader.load_and_parse(config_path)
        config = ComponentFactory._get_config_section(master_config, "intent_detector")
        
        detector_type = config.get("type", "rule")
        if detector_type != "rule":
            raise ValueError(f"Unsupported IntentDetector type: {detector_type}")
        
        # Extract rules
        raw_rules = config.get("rules", {})
        intent_rules = {}
        for intent_name, keywords in raw_rules.items():
            intent = Intent[intent_name.upper()]
            intent_rules[intent] = keywords
        
        # Extract priority
        priority = config.get("priority", [])
        
        return RuleIntentDetector(intent_rules, priority)
    
    @staticmethod
    def create_query_writer(config_path: str) -> 'HeuristicQueryWriter':
        from ..writer import HeuristicQueryWriter
        """Create query writer from configuration."""
        master_config = JsonConfigLoader.load_and_parse(config_path)
        config = ComponentFactory._get_config_section(master_config, "query_writer")
        
        stopwords = config.get("stopwords", [])
        suffix_list = config.get("suffix_list", [])
        max_terms = config.get("max_terms", 10)
        
        # Extract boosters
        raw_boosters = config.get("boosters", {})
        boosters = {}
        for intent_name, terms in raw_boosters.items():
            intent = Intent[intent_name.upper()]
            boosters[intent] = terms
        
        return HeuristicQueryWriter(stopwords, boosters, suffix_list, max_terms)
    
    @staticmethod
    def create_retriever(config_path: str, chunk_path: str = ""):
        """Create retriever from configuration."""
        master_config = JsonConfigLoader.load_and_parse(config_path)


        # Get chunk store
        if not chunk_path:
            data_config = ComponentFactory._get_config_section(master_config, "data_paths")
            chunk_path = data_config.__getitem__("chunk_file_path")


        chunk_store = ChunkStoreLoader.load(chunk_path)


        # Build keyword index
        index = KeywordIndex()
        index.build_from_chunks(chunk_store.get_all_chunks())

        # Get retriever config
        retriever_config = master_config.get("retriever", {})
        rtype = retriever_config.get("type", "keyword")
        k = retriever_config.get("k", 10)

        use_cache = retriever_config.get("use_cache", False)

        if use_cache:
            cache_file = retriever_config.get("cache_file", "resources/cache.json")
            return CacheRetriever(index, k, cache_file)
        if rtype == "keyword":
            data_cfg = master_config.get("data_paths", {})
            index_path = data_cfg.get("index_file_path")
            print(f"DEBUG keyword index source = {'file' if (index_path and os.path.exists(index_path)) else 'rebuild'}")


            index = KeywordIndex()

            if index_path and os.path.exists(index_path):
                with open(index_path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                index = KeywordIndex.load_from_dict(raw)
                # IMPORTANT: map chunk_id -> Chunk so SimpleRetriever can work
                index.attach_chunks(chunk_store.get_all_chunks())
            else:
                index.build_from_chunks(chunk_store.get_all_chunks())

            return SimpleRetriever(index, k)
        
        if rtype == "vector":
            # Embedding config (optional)
            emb_cfg_raw = master_config.get("embedding", {})
            dim = emb_cfg_raw.get("dim", 64)
            salt = emb_cfg_raw.get("salt", "miniRAG-v1")

            embedder = DeterministicHashEmbeddingProvider(HashEmbeddingConfig(dim=dim, salt=salt))

            # Build vector index over all chunks
            vindex = VectorIndex()
            chunks = chunk_store.get_all_chunks()
            vectors = embedder.embed_texts([c.text for c in chunks])
            vindex.add_many([(c.id, v) for c, v in zip(chunks, vectors)])

            # IMPORTANT: apply k from config
            return VectorRetriever(
                chunk_store=chunk_store,
                index=vindex,
                embedder=embedder,
                cfg=VectorRetrieverConfig(k=k),
            )


        raise ValueError(f"Unsupported Retriever type: {rtype}")
    
    @staticmethod
    def create_reranker(config_path: str) -> Reranker:
        """Create reranker instance from configuration.

        Supported types (case-insensitive):
        - "phrase", "phrase_aware", "simple": returns PhraseAwareReranker
        - "jaccard": returns JaccardReranker

        Raises ValueError for unsupported types.
        """
        master_config = JsonConfigLoader.load_and_parse(config_path)
        # Use a default empty dict if not present so we can provide a sensible default
        reranker_cfg = master_config.get("reranker", {}) or {}

        rtype = str(reranker_cfg.get("type", "phrase")).lower()

        if rtype in ("phrase", "phrase_aware", "simple"):
            rr = PhraseAwareReranker()
            # Optional: allow overriding boost from config
            if "phrase_boost" in reranker_cfg:
                try:
                    rr.PHRASE_BOOST = float(reranker_cfg["phrase_boost"])
                except Exception:
                    # ignore invalid value and keep default
                    pass
            return rr

        if rtype in ("jaccard", "jaccard_similarity"):
            return JaccardReranker()

        raise ValueError(f"Unsupported Reranker type: {rtype}")
    
    
    @staticmethod
    def create_answer_agent(config_path: str, chunk_path: str = "") -> Any:
        """Create answer agent from configuration."""
        master_config = JsonConfigLoader.load_and_parse(config_path)
        
        # Check for answer agent config
        agent_config = master_config.get("answer_agent", {})
        agent_type = agent_config.get("type", "template")
                    
        if agent_type == "ollama":
            from ..llm.ollama_llm import OllamaLLM
            from ..answer.ollama_answer_agent import OllamaAnswerAgent
            
            llm_config = master_config.get("llm", {})
            base_url = llm_config.get("base_url", "http://localhost:11434")
            model_name = llm_config.get("model_name", "llama3")
            
            llm = OllamaLLM(base_url=base_url, model_name=model_name)
            return OllamaAnswerAgent(llm)

        # Get chunk store
        if chunk_path:
            chunk_store = ChunkStoreLoader.load(chunk_path)
        else:
            chunk_store = ComponentFactory.create_chunk_store(config_path)
        
        return TemplateAnswerAgent(chunk_store)
    
    @staticmethod
    def create_policy_rerouter(config_path: str) -> KeywordPolicyRerouter:
        """Create policy rerouter from configuration."""
        master_config = JsonConfigLoader.load_and_parse(config_path)
        config = ComponentFactory._get_config_section(master_config, "policy")
        
        banned_keywords = config.get("banned_keywords", [])
        return KeywordPolicyRerouter(banned_keywords)
