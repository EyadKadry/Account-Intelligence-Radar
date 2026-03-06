def generate_human_report(data):

    report = []

    company = data.get("company_identifiers", {})
    snapshot = data.get("business_snapshot", {})
    leadership = data.get("leadership_signals", [])
    initiatives = data.get("strategic_initiatives", [])
    evidence = data.get("evidence", [])

    report.append("COMPANY INTELLIGENCE REPORT")
    report.append("=" * 40)

    report.append(f"\nCompany: {company.get('name', 'N/A')}")
    report.append(f"Headquarters: {company.get('headquarters', 'N/A')}")

    report.append("\nBusiness Units:")
    for unit in snapshot.get("business_units", []):
        report.append(f"- {unit}")

    report.append("\nProducts & Services:")
    for product in snapshot.get("products_services", []):
        report.append(f"- {product}")

    report.append("\nTarget Industries:")
    for industry in snapshot.get("target_industries", []):
        report.append(f"- {industry}")

    report.append("\nLeadership:")
    for leader in leadership:
        name = leader.get("name")
        title = leader.get("title")
        report.append(f"- {name} — {title}")

    report.append("\nStrategic Initiatives:")
    for item in initiatives:
        name = item.get("name")
        desc = item.get("description")
        report.append(f"- {name}")
        report.append(f"  {desc}")

    report.append("\nEvidence Sources:")
    for src in evidence:
        report.append(f"- {src}")

    return "\n".join(report)