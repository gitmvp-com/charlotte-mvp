"""
CHARLOTTE MVP - CVE Lookup

Simplified CVE database lookup using NVD API.
Provides basic CVE search and retrieval.
"""

import requests
from typing import Dict, List, Optional
import json

NVD_API_BASE = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def lookup_cve(cve_id: str) -> str:
    """Look up a specific CVE by ID"""
    try:
        # Normalize CVE ID
        cve_id = cve_id.upper().strip()
        if not cve_id.startswith("CVE-"):
            return f"[!] Invalid CVE ID format: {cve_id}\nExpected format: CVE-YYYY-NNNN"
        
        print(f"[*] Fetching {cve_id} from NVD...")
        
        # Query NVD API
        url = f"{NVD_API_BASE}?cveId={cve_id}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return f"[!] NVD API error: {response.status_code}"
        
        data = response.json()
        
        if not data.get("vulnerabilities"):
            return f"[!] CVE not found: {cve_id}"
        
        # Extract CVE data
        vuln = data["vulnerabilities"][0]["cve"]
        
        # Format output
        result = f"\n{'='*60}\n"
        result += f"CVE ID: {vuln.get('id', 'N/A')}\n"
        result += f"{'='*60}\n"
        
        # Description
        descriptions = vuln.get("descriptions", [])
        if descriptions:
            desc = next((d["value"] for d in descriptions if d["lang"] == "en"), "N/A")
            result += f"\nDescription:\n{desc}\n"
        
        # CVSS Scores
        metrics = vuln.get("metrics", {})
        if metrics:
            result += "\nCVSS Scores:\n"
            
            # CVSS v3.x
            for key in ["cvssMetricV31", "cvssMetricV30"]:
                if key in metrics and metrics[key]:
                    cvss = metrics[key][0]["cvssData"]
                    result += f"  • CVSS v3: {cvss.get('baseScore', 'N/A')} ({cvss.get('baseSeverity', 'N/A')})\n"
                    result += f"    Vector: {cvss.get('vectorString', 'N/A')}\n"
                    break
            
            # CVSS v2
            if "cvssMetricV2" in metrics and metrics["cvssMetricV2"]:
                cvss = metrics["cvssMetricV2"][0]["cvssData"]
                result += f"  • CVSS v2: {cvss.get('baseScore', 'N/A')}\n"
        
        # Published date
        result += f"\nPublished: {vuln.get('published', 'N/A')}\n"
        result += f"Last Modified: {vuln.get('lastModified', 'N/A')}\n"
        
        # References
        references = vuln.get("references", [])
        if references:
            result += f"\nReferences ({len(references)}):  "
            for i, ref in enumerate(references[:5], 1):
                result += f"\n  {i}. {ref.get('url', 'N/A')}"
            if len(references) > 5:
                result += f"\n  ... and {len(references) - 5} more"
        
        result += f"\n{'='*60}\n"
        return result
    
    except requests.RequestException as e:
        return f"[!] Network error: {e}\nCheck your internet connection."
    except Exception as e:
        return f"[!] Error: {e}"

def search_cve(keyword: str, limit: int = 10) -> str:
    """Search CVEs by keyword"""
    try:
        print(f"[*] Searching for '{keyword}' (limit: {limit})...")
        
        # NVD API keyword search
        url = f"{NVD_API_BASE}?keywordSearch={keyword}&resultsPerPage={limit}"
        response = requests.get(url, timeout=15)
        
        if response.status_code != 200:
            return f"[!] NVD API error: {response.status_code}"
        
        data = response.json()
        
        vulnerabilities = data.get("vulnerabilities", [])
        
        if not vulnerabilities:
            return f"[!] No results found for: {keyword}"
        
        # Format results
        result = f"\n{'='*60}\n"
        result += f"Search Results for '{keyword}' ({len(vulnerabilities)} found)\n"
        result += f"{'='*60}\n"
        
        for i, item in enumerate(vulnerabilities, 1):
            cve = item["cve"]
            cve_id = cve.get("id", "N/A")
            
            # Get description
            descriptions = cve.get("descriptions", [])
            desc = next((d["value"] for d in descriptions if d["lang"] == "en"), "N/A")
            # Truncate long descriptions
            if len(desc) > 200:
                desc = desc[:200] + "..."
            
            # Get CVSS score
            metrics = cve.get("metrics", {})
            score = "N/A"
            severity = "N/A"
            
            for key in ["cvssMetricV31", "cvssMetricV30"]:
                if key in metrics and metrics[key]:
                    cvss = metrics[key][0]["cvssData"]
                    score = cvss.get("baseScore", "N/A")
                    severity = cvss.get("baseSeverity", "N/A")
                    break
            
            result += f"\n{i}. {cve_id}\n"
            result += f"   Score: {score} ({severity})\n"
            result += f"   {desc}\n"
        
        result += f"\n{'='*60}\n"
        result += "\nTip: Use 'CVE Lookup > CVE ID' to get full details for a specific CVE\n"
        
        return result
    
    except requests.RequestException as e:
        return f"[!] Network error: {e}\nCheck your internet connection."
    except Exception as e:
        return f"[!] Error: {e}"

if __name__ == "__main__":
    # Test
    print(search_cve("apache", limit=5))
