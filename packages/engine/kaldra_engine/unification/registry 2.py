"""
Module Registry for KALDRA v3.0.

Central registry for all KALDRA modules, enabling plug-and-play architecture.
"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


@dataclass
class ModuleInfo:
    """Information about a registered module."""
    name: str
    module: Any
    version: str
    description: str
    dependencies: List[str] = field(default_factory=list)


class ModuleRegistry:
    """
    Central registry for all KALDRA modules.
    
    Enables dynamic module loading and plug-and-play architecture.
    """
    
    def __init__(self):
        self._modules: Dict[str, ModuleInfo] = {}
        self._initialized = False
    
    def register(
        self,
        name: str,
        module: Any,
        version: str = "2.9",
        description: str = "",
        dependencies: Optional[List[str]] = None
    ) -> None:
        """
        Register a module in the registry.
        
        Args:
            name: Module name (e.g., "archetypes", "kindra")
            module: The module instance
            version: Module version
            description: Module description
            dependencies: List of module names this depends on
        """
        self._modules[name] = ModuleInfo(
            name=name,
            module=module,
            version=version,
            description=description,
            dependencies=dependencies or []
        )
    
    def get(self, name: str) -> Any:
        """
        Get a registered module.
        
        Args:
            name: Module name
            
        Returns:
            The module instance
            
        Raises:
            KeyError: If module not found
        """
        if name not in self._modules:
            raise KeyError(f"Module '{name}' not registered")
        return self._modules[name].module
    
    def get_info(self, name: str) -> ModuleInfo:
        """Get module information."""
        if name not in self._modules:
            raise KeyError(f"Module '{name}' not registered")
        return self._modules[name]
    
    def list_modules(self) -> List[str]:
        """List all registered module names."""
        return list(self._modules.keys())
    
    def has_module(self, name: str) -> bool:
        """Check if a module is registered."""
        return name in self._modules
    
    def unregister(self, name: str) -> None:
        """Unregister a module."""
        if name in self._modules:
            del self._modules[name]
    
    def clear(self) -> None:
        """Clear all registered modules."""
        self._modules.clear()
        self._initialized = False
    
    def is_initialized(self) -> bool:
        """Check if registry has been initialized with modules."""
        return self._initialized
    
    def mark_initialized(self) -> None:
        """Mark registry as initialized."""
        self._initialized = True
    
    def __repr__(self) -> str:
        return f"ModuleRegistry(modules={len(self._modules)}, initialized={self._initialized})"


# Global registry instance
_global_registry = ModuleRegistry()


def get_global_registry() -> ModuleRegistry:
    """Get the global module registry instance."""
    return _global_registry
