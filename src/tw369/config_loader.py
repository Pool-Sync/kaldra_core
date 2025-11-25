"""
TW369 Configuration Loader

Loads and validates TW369 engine configuration files against the schema.
"""

import json
from pathlib import Path

try:
    import jsonschema
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


class TW369ConfigLoader:
    """
    Loads TW369 engine configuration with optional schema validation.
    
    If jsonschema is installed, validates configuration files against 
    tw369_config_schema.json. Otherwise, performs basic structure validation.
    """
    
    def __init__(self, schema_path="schema/tw369/tw369_config_schema.json"):
        """
        Initialize config loader with schema.
        
        Args:
            schema_path: Path to TW369 config schema file
        """
        self.schema_path = Path(schema_path)
        if self.schema_path.exists():
            self.schema = json.loads(self.schema_path.read_text())
        else:
            self.schema = None
    
    def _basic_validate(self, cfg):
        """
        Basic validation without jsonschema.
        
        Checks for required fields.
        """
        required = ["enabled", "max_time_steps", "default_step_size"]
        for field in required:
            if field not in cfg:
                raise ValueError(f"Missing required field: {field}")
    
    def load(self, path):
        """
        Load and validate configuration file.
        
        Args:
            path: Path to configuration JSON file
            
        Returns:
            Validated configuration dict
            
        Raises:
            ValueError: If config is invalid
            FileNotFoundError: If config file doesn't exist
        """
        cfg = json.loads(Path(path).read_text())
        
        if HAS_JSONSCHEMA and self.schema:
            jsonschema.validate(cfg, self.schema)
        else:
            self._basic_validate(cfg)
        
        return cfg

