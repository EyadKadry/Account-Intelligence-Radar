from app.serp_discovery import find_official_website
from app.serp_initiatives import discover_initiatives
from app.llm_decision import select_best_sources
from app.firecrawl_extract import extract_company_data
from app.intelligence_fusion import fuse_company_intelligence
from app.report_generator import generate_human_report
import json
import os

if __name__ == "__main__":

    company_name = input("Enter company name: ")
    objective = input(
    "\nEnter objective prompt:\n"
)

    print("\nStep 1: Finding official website...\n")

    website = find_official_website(company_name)

    print("Official Website Found:")
    print(website)

    print("\nStep 2: Discovering company initiatives...\n")

    initiatives = discover_initiatives(company_name)

    for i, item in enumerate(initiatives[:5], start=1):
        print(f"{i}. {item['title']}")
        print(f"   {item['url']}")

    print("\nStep 3: LLM selecting best sources...\n")

    selected = select_best_sources(
        official_site=website,
        initiative_results=initiatives,
        objective=objective
    )

    print("Selected Sources by LLM:\n")
    print(selected)

    print("\nStep 4: Extracting structured company intelligence...\n")

    urls = [s["url"] for s in selected["selected_sources"]]

    company_data = extract_company_data(urls)

    print("\nFinal Extracted Company Intelligence:\n")
    print(company_data)
    fused = fuse_company_intelligence(
    company_name,
    objective,
    company_data
    )

    print("\nFinal Company Intelligence Report:\n")
    print(json.dumps(fused, indent=2))
    print("\nGenerating human readable report...\n")

    report = generate_human_report(fused)

    print(report)
    # create reports folder if not exists
    os.makedirs("reports", exist_ok=True)

    report_path = f"reports/{company_name.replace(' ', '_')}_report.json"

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(fused, f, indent=2, ensure_ascii=False)

    os.makedirs("reports", exist_ok=True)

    report_path = f"reports/{company_name.replace(' ', '_')}_report.md"

    markdown_content = f"""
    # Company Report: {fused.get('company_name', company_name)}

    ## Company Identifiers
    - **Name:** {fused.get('company_name')}
    - **Headquarters:** {fused.get('headquarters')}

    ## Business Snapshot

    ### Business Units
    """

    for unit in fused.get("business_units", []):
        markdown_content += f"- {unit.get('name')}  \n"

    markdown_content += "\n### Products / Services\n"

    for product in fused.get("products_services", []):
        markdown_content += f"- {product}  \n"

    markdown_content += "\n### Target Industries\n"

    for industry in fused.get("target_industries", []):
        markdown_content += f"- {industry}  \n"

    markdown_content += "\n## Leadership Signals\n"

    for leader in fused.get("leadership", []):
        markdown_content += f"- **{leader.get('name')}** — {leader.get('title')}  \n"

    markdown_content += "\n## Strategic Initiatives\n"

    for initiative in fused.get("strategic_initiatives", []):
        markdown_content += f"- **{initiative.get('name')}**: {initiative.get('description')}  \n"

    markdown_content += "\n## Evidence Sources\n"

    for source in fused.get("selected_sources", []):
        markdown_content += f"- {source.get('url')}\n"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"Report saved to {report_path}")
    