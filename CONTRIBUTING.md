# Contributing to CHARLOTTE MVP

Thank you for your interest in contributing to CHARLOTTE!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch: `git checkout -b feature/amazing-feature`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m 'Add amazing feature'`
7. Push: `git push origin feature/amazing-feature`
8. Open a Pull Request

## Development Setup

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/charlotte-mvp.git
cd charlotte-mvp

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

## Code Style

- Follow PEP 8
- Use type hints where possible
- Add docstrings to functions and classes
- Keep functions focused and modular

## Plugin Development

### Creating a New Plugin

1. Create file in `plugins/` directory
2. Implement `run_plugin(args=None)` function
3. Register in `core/plugin_manager.py`
4. Add tests

### Plugin Template

```python
"""
Plugin Description
"""

def run_plugin(args=None):
    """Plugin entry point
    
    Args:
        args: Optional dict of arguments
    
    Returns:
        str or dict: Plugin result
    """
    if args is None:
        args = {}
    
    # Your plugin logic here
    
    return {"status": "ok", "data": "result"}
```

## Testing

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Add integration tests for plugins

## Documentation

- Update README.md for new features
- Add docstrings to code
- Include usage examples

## Pull Request Guidelines

- Clear description of changes
- Reference any related issues
- Include tests
- Update documentation
- Keep PRs focused and atomic

## Questions?

Open an issue for:
- Bug reports
- Feature requests
- Questions
- Discussions

Thank you for contributing! 🎉
