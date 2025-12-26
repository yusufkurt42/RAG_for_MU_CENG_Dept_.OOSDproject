"""Component factory for creating pipeline stages."""

from typing import TYPE_CHECKING
from typing import Dict, List, Any
from ..detector import Intent, RuleIntentDetector
if TYPE_CHECKING:
    from ..writer import HeuristicQueryWriter
from ..retriever import SimpleRetriever, KeywordIndex
from ..reranker import PhraseAwareReranker
from ..answer import TemplateAnswerAgent
from ..model import ChunkStore
from ..utility import ChunkStoreLoader, JsonConfigLoader
from ..embedding import DeterministicHashEmbeddingProvider, HashEmbeddingConfig
from ..retriever import VectorRetriever, VectorIndex
from ..retriever.vector_retriever import VectorRetrieverConfig
import os
import json


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

        retriever_config = master_config.get("retriever", {})
        rtype = retriever_config.get("type", "keyword")
        k = retriever_config.get("k", 10)

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
    def create_reranker(config_path: str) -> PhraseAwareReranker:
        """Create reranker from configuration."""
        # For now, just return default reranker
        # Could read boost value from config
        return PhraseAwareReranker()
    
    @staticmethod
    def create_answer_agent(config_path: str, chunk_path: str = "") -> Any:
        """Create answer agent from configuration."""
        master_config = JsonConfigLoader.load_and_parse(config_path)
        
        # Check for answer agent config
        agent_config = master_config.get("answer_agent", {})
        agent_type = agent_config.get("type", "template")
        
        if agent_type == "gemini":
            from ..llm.gemini_llm import GeminiLLM
            from ..answer.gemini_answer_agent import GeminiAnswerAgent
            import os
            
            llm_config = master_config.get("llm", {})
            api_key_env = llm_config.get("api_key_env_var", "GEMINI_API_KEY")
            api_key = os.environ.get(api_key_env)
            
            if not api_key:
                raise ValueError(f"Gemini API key not found in environment variable: {api_key_env}")
                
            model_name = llm_config.get("model_name", "gemini-pro")
            llm = GeminiLLM(api_key=api_key, model_name=model_name)
            return GeminiAnswerAgent(llm)
            
        elif agent_type == "ollama":
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
