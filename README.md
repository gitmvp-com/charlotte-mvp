# 🧠 C.H.A.R.L.O.T.T.E. MVP

**Cybernetic Heuristic Assistant for Recon, Logic, Offensive Tactics, Triage & Exploitation**

A streamlined, fully operational MVP of the CHARLOTTE security framework focused on **code reasoning** and **vulnerability analysis**.

## 🎯 MVP Features

This MVP includes:

✅ **Code Reasoner** - AI-powered code analysis with masked token prediction
✅ **Vulnerability Scanner** - Basic vulnerability detection
✅ **Plugin System** - Modular plugin architecture
✅ **CVE Lookup** - Simple CVE database integration
✅ **CLI Interface** - Interactive command-line interface
✅ **Zero Configuration** - Works out of the box

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/gitmvp-com/charlotte-mvp.git
cd charlotte-mvp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run CHARLOTTE

```bash
# Start the CLI
python charlotte.py

# Or use the main module
python -m core.main
```

## 📖 Usage Examples

### Code Reasoner

```bash
# Analyze code with masked tokens
python -m core.code_reasoner guess "def [MASK](x, y): return x + y" --top-k 5

# Fill in missing code
python -m core.code_reasoner fill "import [MASK]; print([MASK])" --top-k 3

# Score options
python -m core.code_reasoner score "result = [MASK]" --options "True" "False" "None"
```

### Vulnerability Scanning

```bash
# Run from CLI menu
python charlotte.py
# Select: "🔍 Vulnerability Scan"
```

### CVE Lookup

```bash
# From CLI menu
python charlotte.py
# Select: "📊 CVE Lookup"
```

## 🗂️ Project Structure

```
charlotte-mvp/
├── core/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── config.py            # Configuration
│   ├── code_reasoner.py     # Code analysis engine
│   ├── plugin_manager.py    # Plugin system
│   └── cve_lookup.py        # CVE database
├── plugins/
│   ├── __init__.py
│   └── vuln_scanner.py      # Vulnerability scanner
├── data/
│   └── findings.json        # Scan results
├── charlotte.py             # Main entry point
├── requirements.txt         # Dependencies
└── README.md
```

## 🔧 Configuration

CHARLOTTE MVP works with zero configuration, but you can customize settings in `core/config.py`:

- **LLM Provider**: OpenAI, HuggingFace, or local
- **Model Selection**: Choose your preferred model
- **Scan Settings**: Adjust scan parameters

### Environment Variables (Optional)

```bash
# Create .env file
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4
```

## 🧩 Plugin System

CHARLOTTE uses a modular plugin architecture:

### Available Plugins

- **vuln_scanner** - Basic vulnerability detection
- **code_reasoner** - AI code analysis
- **cve_lookup** - CVE database queries

### Creating a Plugin

```python
# plugins/my_plugin.py

def run_plugin(args=None):
    """Plugin entry point"""
    if args is None:
        args = {}
    
    # Your plugin logic here
    result = {"status": "ok", "data": "result"}
    return result
```

Register in `core/plugin_manager.py`:

```python
PLUGIN_REGISTRY["my_task"] = ("plugins", "my_plugin")
```

## 📊 Code Reasoner

The Code Reasoner uses transformer models to analyze and predict code:

### Features

- **Masked Token Prediction**: Suggest code completions
- **Multi-Token Fill**: Complete multiple gaps
- **Option Scoring**: Rank multiple possibilities
- **Language Agnostic**: Works with Python, JavaScript, C, etc.

### Technical Details

- Model: `microsoft/codebert-base` (default)
- Supports custom models via HuggingFace
- CPU and GPU compatible
- Optimized for security code analysis

## 🛡️ Security Scanning

### Scan Types

1. **Pattern-based Detection**: Regex patterns for common vulnerabilities
2. **Code Analysis**: Static analysis for security issues
3. **CVE Matching**: Match against known vulnerabilities

### Supported Vulnerabilities

- SQL Injection
- XSS (Cross-Site Scripting)
- Command Injection
- Path Traversal
- Hardcoded Secrets
- Unsafe Deserialization

## 📈 Roadmap

### Completed in MVP ✅

- [x] Code Reasoner core functionality
- [x] Plugin system architecture
- [x] CLI interface
- [x] Basic vulnerability scanning
- [x] CVE lookup integration

### Future Enhancements 🚀

- [ ] Fine-tuned code reasoner model
- [ ] Advanced memory management
- [ ] GUI dashboard
- [ ] Automated patch generation
- [ ] Enhanced dataset building
- [ ] Integration with external tools (Burp, ZAP)
- [ ] Real-time monitoring
- [ ] Report generation

## 🤝 Contributing

Contributions are welcome! This MVP is designed to be:

- **Modular**: Easy to extend with new plugins
- **Clean**: Well-documented and maintainable
- **Testable**: Unit tests for core functionality

## 📄 License

Based on C.H.A.R.L.O.T.T.E. - AGPLv3 License

## 🔗 Links

- [Original Project](https://github.com/iaintheardofu/1)
- [Documentation](https://www.c-h-a-r-l-o-t-t-e.org/)

## 🎓 Status Checklist

### From Original Project

✅ **Code Reasoner** - Simplified and operational
⚠️ **Dataset for Code Reasoner** - Uses default HuggingFace models
⚠️ **Fine Tuning** - Planned for future
❌ **Memory Management** - Not in MVP scope
✅ **Module Code Check** - Basic implementation
⚠️ **Patch Checker** - Simplified version
❌ **Front End** - CLI only (GUI planned)
❌ **Temp Patch Creator** - Planned for future
✅ **Overall Architecture** - Clean, modular MVP

---

**Built with ❤️ for the security community**
