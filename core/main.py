#!/usr/bin/env python3
"""
CHARLOTTE MVP - Main CLI Interface

Simplified, fully operational command-line interface for CHARLOTTE.
Focuses on code reasoning and vulnerability analysis.
"""

import sys
import os
from pathlib import Path

# Ensure imports work
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from InquirerPy import inquirer
    from InquirerPy.separator import Separator
except ModuleNotFoundError:
    print("[!] Missing dependency: InquirerPy")
    print("    Install with: pip install InquirerPy")
    sys.exit(1)

try:
    from core.plugin_manager import load_plugins, run_plugin
    from core.config import CHARLOTTE_CONFIG
except ModuleNotFoundError as e:
    print(f"[!] Missing CHARLOTTE module: {e.name}")
    print("    Ensure you're in the project directory and dependencies are installed.")
    sys.exit(1)

VERSION = "0.1.0-MVP"

def print_banner():
    """Display CHARLOTTE banner"""
    PURPLE = "\033[35m"
    RESET = "\033[0m"
    
    banner = f"""{PURPLE}
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║     ██████╗██╗  ██╗ █████╗ ██████╗ ██╗      ██████╗     ║
    ║    ██╔════╝██║  ██║██╔══██╗██╔══██╗██║     ██╔═══██╗    ║
    ║    ██║     ███████║███████║██████╔╝██║     ██║   ██║    ║
    ║    ██║     ██╔══██║██╔══██║██╔══██╗██║     ██║   ██║    ║
    ║    ╚██████╗██║  ██║██║  ██║██║  ██║███████╗╚██████╔╝    ║
    ║     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝     ║
    ║                                                           ║
    ║              T  ·  T  ·  E     M  V  P                   ║
    ║                                                           ║
    ║   Cybernetic Heuristic Assistant for Recon, Logic,       ║
    ║        Offensive Tactics, Triage & Exploitation           ║
    ║                                                           ║
    ║                    Version {VERSION:14s}                  ║
    ╚═══════════════════════════════════════════════════════════╝
{RESET}
    """
    print(banner)

def run_code_reasoner():
    """Interactive code reasoner interface"""
    print("\n=== Code Reasoner ===")
    print("Analyze code with AI-powered token prediction\n")
    
    mode = inquirer.select(
        message="Select operation:",
        choices=[
            "🔍 Guess missing tokens",
            "✏️  Fill in code",
            "📊 Score options",
            "← Back"
        ],
        default="🔍 Guess missing tokens"
    ).execute()
    
    if mode == "← Back":
        return
    
    code = inquirer.text(
        message="Enter code snippet (use [MASK] for unknown tokens):",
        default="def [MASK](x, y): return x + y"
    ).execute()
    
    if not code:
        print("[!] No code provided.")
        return
    
    try:
        from core.code_reasoner import CodeReasonerCLI
        cli = CodeReasonerCLI()
        
        if "Guess" in mode:
            top_k = inquirer.text(
                message="Top K suggestions (default 5):",
                default="5"
            ).execute()
            try:
                k = int(top_k) if top_k else 5
            except ValueError:
                k = 5
            cli.guess(code, top_k=k)
        
        elif "Fill" in mode:
            top_k = inquirer.text(
                message="Top K branches (default 3):",
                default="3"
            ).execute()
            try:
                k = int(top_k) if top_k else 3
            except ValueError:
                k = 3
            cli.fill(code, top_k=k)
        
        elif "Score" in mode:
            options = inquirer.text(
                message="Enter options (comma-separated):",
                default="func,method,function"
            ).execute()
            if options:
                opts = [o.strip() for o in options.split(",")]
                cli.score(code, opts)
    
    except Exception as e:
        print(f"\n[!] Error: {e}")
        print("\nTip: Make sure transformers and torch are installed.")
        print("     Run: pip install transformers torch")

def run_vulnerability_scan():
    """Run vulnerability scanner"""
    print("\n=== Vulnerability Scanner ===")
    
    path = inquirer.text(
        message="Enter file or directory to scan:",
        default="."
    ).execute()
    
    if not path:
        path = "."
    
    print(f"\n[*] Scanning: {path}")
    
    try:
        result = run_plugin("vuln_scan", {"path": path})
        if result:
            print(f"\n{result}")
    except Exception as e:
        print(f"\n[!] Scan error: {e}")

def run_cve_lookup():
    """CVE lookup interface"""
    print("\n=== CVE Lookup ===")
    
    mode = inquirer.select(
        message="Search by:",
        choices=["CVE ID", "Keyword", "← Back"],
        default="Keyword"
    ).execute()
    
    if mode == "← Back":
        return
    
    if mode == "CVE ID":
        cve_id = inquirer.text(
            message="Enter CVE ID (e.g., CVE-2024-1234):",
            default="CVE-2024-"
        ).execute()
        
        if cve_id:
            try:
                from core.cve_lookup import lookup_cve
                result = lookup_cve(cve_id)
                print(f"\n{result}")
            except Exception as e:
                print(f"\n[!] Lookup error: {e}")
    
    else:  # Keyword
        keyword = inquirer.text(
            message="Enter search keyword:",
            default="apache"
        ).execute()
        
        if keyword:
            try:
                from core.cve_lookup import search_cve
                result = search_cve(keyword, limit=10)
                print(f"\n{result}")
            except Exception as e:
                print(f"\n[!] Search error: {e}")

def main():
    """Main CLI loop"""
    print_banner()
    
    # Load plugins
    try:
        load_plugins()
    except Exception as e:
        print(f"[!] Warning: Plugin loading failed: {e}")
    
    while True:
        try:
            choice = inquirer.select(
                message="What would you like CHARLOTTE to do?",
                choices=[
                    Separator("=== AI Code Analysis ==="),
                    "🧠 Code Reasoner",
                    Separator("=== Security Scanning ==="),
                    "🔍 Vulnerability Scan",
                    "📊 CVE Lookup",
                    Separator("==="),
                    "ℹ️  About",
                    "🚪 Exit"
                ],
                default="🧠 Code Reasoner"
            ).execute()
            
            if choice == "🚪 Exit":
                print("\n👋 Goodbye! Stay safe out there.\n")
                break
            
            elif choice == "🧠 Code Reasoner":
                run_code_reasoner()
            
            elif choice == "🔍 Vulnerability Scan":
                run_vulnerability_scan()
            
            elif choice == "📊 CVE Lookup":
                run_cve_lookup()
            
            elif choice == "ℹ️  About":
                print(f"\n{'='*60}")
                print("C.H.A.R.L.O.T.T.E. MVP")
                print(f"Version: {VERSION}")
                print("\nA streamlined security analysis framework focused on:")
                print("  • AI-powered code reasoning")
                print("  • Vulnerability detection")
                print("  • CVE intelligence")
                print("\nOriginal Project: https://github.com/iaintheardofu/1")
                print("MVP Repository: https://github.com/gitmvp-com/charlotte-mvp")
                print(f"{'='*60}\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n[!] Error: {e}")
            continue
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
