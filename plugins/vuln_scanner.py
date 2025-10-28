"""
CHARLOTTE MVP - Vulnerability Scanner Plugin

Basic pattern-based vulnerability scanner.
Detects common security issues in code files.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any

# Vulnerability patterns
VULN_PATTERNS = {
    "SQL Injection": [
        (r"execute\s*\(\s*['\"].*%.*['\"]\s*%", "String formatting in SQL query"),
        (r"execute\s*\(\s*.*\+.*\)", "String concatenation in SQL query"),
        (r"\.format\s*\(.*SELECT", "String formatting with SELECT"),
    ],
    "XSS": [
        (r"innerHTML\s*=\s*[^;]+(?!sanitize)", "Potential XSS via innerHTML"),
        (r"document\.write\s*\(", "Unsafe document.write usage"),
        (r"eval\s*\(", "Dangerous eval() usage"),
    ],
    "Command Injection": [
        (r"os\.system\s*\(.*\+", "Command injection via os.system"),
        (r"subprocess\..*shell\s*=\s*True", "Shell injection risk"),
        (r"exec\s*\(.*input", "Executing user input"),
    ],
    "Path Traversal": [
        (r"open\s*\(.*input.*\)", "User input in file path"),
        (r"os\.path\.join\s*\(.*request\.", "Request data in path"),
    ],
    "Hardcoded Secrets": [
        (r"password\s*=\s*['\"][^'\"]+['\"](?!\{)", "Hardcoded password"),
        (r"api[_-]?key\s*=\s*['\"][^'\"]+['\"](?!\{)", "Hardcoded API key"),
        (r"secret\s*=\s*['\"][^'\"]+['\"](?!\{)", "Hardcoded secret"),
        (r"token\s*=\s*['\"][^'\"]{20,}['\"](?!\{)", "Hardcoded token"),
    ],
}

# File extensions to scan
SCANNABLE_EXTENSIONS = {
    ".py", ".js", ".java", ".php", ".rb", ".go",
    ".c", ".cpp", ".h", ".cs", ".ts", ".jsx", ".tsx"
}

def scan_file(file_path: Path) -> List[Dict[str, Any]]:
    """Scan a single file for vulnerabilities"""
    findings = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        for vuln_type, patterns in VULN_PATTERNS.items():
            for pattern, description in patterns:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        findings.append({
                            "file": str(file_path),
                            "line": line_num,
                            "type": vuln_type,
                            "description": description,
                            "code": line.strip(),
                            "severity": get_severity(vuln_type)
                        })
    
    except Exception as e:
        pass  # Skip files that can't be read
    
    return findings

def get_severity(vuln_type: str) -> str:
    """Get severity level for vulnerability type"""
    high_severity = {"SQL Injection", "Command Injection", "XSS"}
    medium_severity = {"Path Traversal"}
    
    if vuln_type in high_severity:
        return "HIGH"
    elif vuln_type in medium_severity:
        return "MEDIUM"
    else:
        return "LOW"

def scan_directory(path: Path, max_files: int = 1000) -> List[Dict[str, Any]]:
    """Recursively scan directory for vulnerabilities"""
    all_findings = []
    files_scanned = 0
    
    for root, dirs, files in os.walk(path):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if d not in {
            'node_modules', '.git', '__pycache__', 'venv', 'env',
            '.venv', 'dist', 'build', 'target'
        }]
        
        for file in files:
            if files_scanned >= max_files:
                break
            
            file_path = Path(root) / file
            
            # Check extension
            if file_path.suffix.lower() in SCANNABLE_EXTENSIONS:
                findings = scan_file(file_path)
                all_findings.extend(findings)
                files_scanned += 1
        
        if files_scanned >= max_files:
            break
    
    return all_findings, files_scanned

def format_results(findings: List[Dict[str, Any]], files_scanned: int) -> str:
    """Format scan results for display"""
    if not findings:
        return f"\n[✓] No vulnerabilities found ({files_scanned} files scanned)\n"
    
    # Group by severity
    by_severity = {"HIGH": [], "MEDIUM": [], "LOW": []}
    for f in findings:
        by_severity[f["severity"]].append(f)
    
    result = f"\n{'='*70}\n"
    result += f"Vulnerability Scan Results\n"
    result += f"{'='*70}\n"
    result += f"Files Scanned: {files_scanned}\n"
    result += f"Issues Found: {len(findings)}\n"
    result += f"  • HIGH:   {len(by_severity['HIGH'])}\n"
    result += f"  • MEDIUM: {len(by_severity['MEDIUM'])}\n"
    result += f"  • LOW:    {len(by_severity['LOW'])}\n"
    result += f"{'='*70}\n"
    
    # Display findings by severity
    for severity in ["HIGH", "MEDIUM", "LOW"]:
        items = by_severity[severity]
        if not items:
            continue
        
        result += f"\n{severity} Severity Issues ({len(items)}):  \n"
        result += "-" * 70 + "\n"
        
        for i, finding in enumerate(items, 1):
            result += f"\n{i}. {finding['type']}\n"
            result += f"   File: {finding['file']}:{finding['line']}\n"
            result += f"   Issue: {finding['description']}\n"
            result += f"   Code: {finding['code'][:100]}\n"
    
    result += f"\n{'='*70}\n"
    return result

def run_plugin(args=None):
    """Plugin entry point"""
    if args is None:
        args = {}
    
    scan_path = args.get("path", ".")
    max_files = args.get("max_files", 1000)
    
    path = Path(scan_path).resolve()
    
    if not path.exists():
        return f"[!] Path not found: {scan_path}"
    
    print(f"[*] Scanning: {path}")
    
    if path.is_file():
        findings = scan_file(path)
        files_scanned = 1
    else:
        findings, files_scanned = scan_directory(path, max_files=max_files)
    
    return format_results(findings, files_scanned)

if __name__ == "__main__":
    # Test
    result = run_plugin({"path": "."})
    print(result)
