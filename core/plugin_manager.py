"""
CHARLOTTE MVP - Plugin Manager

Simplified plugin system for MVP.
Supports static plugin registration and execution.
"""

import importlib
import sys
from pathlib import Path
from typing import Any, Dict, Tuple, Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Plugin Registry: task_name -> (category, module_name)
PLUGIN_REGISTRY: Dict[str, Tuple[str, str]] = {
    "vuln_scan": ("plugins", "vuln_scanner"),
}

# Aliases for common tasks
ALIASES: Dict[str, str] = {
    "scan": "vuln_scan",
    "vulnerability_scan": "vuln_scan",
}

def load_plugins() -> None:
    """Load and display available plugins"""
    print("\n[*] CHARLOTTE Plugin System")
    print("\n[*] Available Plugins:")
    
    for task, (category, module) in PLUGIN_REGISTRY.items():
        print(f"  • {task:20s} → {category}.{module}")
    
    print("\n[✓] Plugin system ready\n")

def _load_plugin_module(category: str, module_name: str):
    """Load a plugin module dynamically"""
    try:
        # Try direct import first
        module_path = f"{category}.{module_name}"
        return importlib.import_module(module_path)
    except ImportError:
        # Try from plugins directory
        try:
            module_path = f"plugins.{module_name}"
            return importlib.import_module(module_path)
        except ImportError as e:
            raise ModuleNotFoundError(
                f"Plugin not found: {category}.{module_name}\n"
                f"Error: {e}"
            )

def run_plugin(task: str, args: Optional[Dict] = None) -> Any:
    """Execute a plugin by task name"""
    # Resolve aliases
    resolved_task = ALIASES.get(task, task)
    
    if resolved_task not in PLUGIN_REGISTRY:
        return f"[!] Unknown plugin: {task}"
    
    category, module_name = PLUGIN_REGISTRY[resolved_task]
    
    try:
        # Load plugin module
        plugin_module = _load_plugin_module(category, module_name)
        
        # Execute plugin
        if hasattr(plugin_module, "run_plugin"):
            return plugin_module.run_plugin(args)
        elif hasattr(plugin_module, "run"):
            return plugin_module.run(args)
        else:
            return f"[!] Plugin {module_name} has no run() or run_plugin() function"
    
    except Exception as e:
        return f"[!] Plugin execution failed: {e}"

if __name__ == "__main__":
    # Test the plugin system
    load_plugins()
