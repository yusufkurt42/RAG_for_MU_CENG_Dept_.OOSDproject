"""Component factory for creating pipeline stages."""

from typing import TYPE_CHECKING
from typing import Dict, List, Any
from ..detector import Intent, RuleIntentDetector
if TYPE_CHECKING:
    from ..writer import HeuristicQueryWriter
from ..retriever import SimpleRetriever, KeywordIndex, CacheRetriever
from ..reranker import PhraseAwareReranker
from ..answer import TemplateAnswerAgent
from ..model import ChunkStore
from ..utility import ChunkStoreLoader, JsonConfigLoader
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
    def create_retriever(config_path: str, chunk_path: str = "") -> SimpleRetriever:
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
        k = retriever_config.get("k", 10)
        use_cache = retriever_config.get("use_cache", False)

        if use_cache:
            cache_file = retriever_config.get("cache_file", "resources/cache.json")
            return CacheRetriever(index, k, cache_file)
        
        return SimpleRetriever(index, k)
    
    @staticmethod
    def create_reranker(config_path: str) -> PhraseAwareReranker:
        """Create reranker from configuration."""
        # For now, just return default reranker
        # Could read boost value from config
        return PhraseAwareReranker()
    
    @staticmethod
    def create_answer_agent(config_path: str, chunk_path: str = "") -> TemplateAnswerAgent:
        """Create answer agent from configuration."""
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
