import requests
import json
from types import SimpleNamespace
import time

def _fetch_cve_details(cve_id):
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return "No details found"

def fetch_shodan():
    url = "https://internetdb.shodan.io/89.168.47.217"
    response = requests.get(url)
    if response.status_code == 200:
        obj = response.json()
        vulnerabilities = obj.get("vulns", [])
        return vulnerabilities
    return "No details found"

def _get_cve_summary(cve_id):
    cve_details = _fetch_cve_details(cve_id)
    cve_data = cve_details["vulnerabilities"][0]["cve"]
    cve_id = cve_data["id"]
    description = cve_data["descriptions"][0]["value"]
    severity = cve_data["metrics"]["cvssMetricV31"][0]["cvssData"]["baseSeverity"]
    base_score = cve_data["metrics"]["cvssMetricV31"][0]["cvssData"]["baseScore"]
    impact = cve_data["metrics"]["cvssMetricV31"][0]["cvssData"]["availabilityImpact"]

    return {
        "cve_id": cve_id,
        "severity": severity,
        "base_score": base_score,
        "impact": impact,
        "description": description
    }

def get_vuln_message_for_sms():
    return '''Utiliser le lien suivant pour avoir plus d'info sur la vulnérabilité: https://www.cvedetails.com/\n
Toutes les vulnérabilités détectées sur la machine Ubuntu Server:\n''' + "; ".join(fetch_shodan())

def get_vuln_list_for_email():
    vuln_list = []
    for vuln in fetch_shodan():
        try:
            vuln_list.append(_get_cve_summary(vuln))
            time.sleep(5)
        except Exception as e:
            print("failed to get on vulnerability: " + str(e))
            continue
    return vuln_list