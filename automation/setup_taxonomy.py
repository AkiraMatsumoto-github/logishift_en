#!/usr/bin/env python3
"""
Setup WordPress Categories and Tags based on sitemap.md (LogiShift Global)
"""

try:
    from automation.wp_client import WordPressClient
except ImportError:
    from wp_client import WordPressClient

import requests

def create_categories(wp):
    """Create all categories defined in sitemap.md (Global)."""
    categories = [
        {
            "name": "Global Trends",
            "slug": "global-trends",
            "description": "Synthesized insights from global logistics news. Comparative analysis of trends in US, EU, and Asia to help you stay ahead of the curve."
        },
        {
            "name": "Technology & DX",
            "slug": "technology-dx",
            "description": "Comprehensive guide to Logistics DX. Covering WMS, RFID, IoT, and AI applications to modernize your supply chain operations."
        },
        {
            "name": "Cost & Efficiency",
            "slug": "cost-efficiency",
            "description": "Practical management strategies for reducing logistics costs and improving operational efficiency. Best practices for ROI maximization."
        },
        {
            "name": "Supply Chain Management",
            "slug": "scm",
            "description": "In-depth analysis of SCM optimization, global procurement, and risk management strategies to build a resilient supply chain."
        },
        {
            "name": "Case Studies",
            "slug": "case-studies",
            "description": "Real-world examples of successful logistics transformation. Exclusive interviews and detailed breakdowns of how leading companies solved their challenges."
        },
        {
            "name": "Logistics Startups",
            "slug": "startups",
            "description": "Spotlight on emerging players and disruptive innovations in the logistics sector. Coverage of funding news, new tech solutions, and future unicorns."
        },
    ]
    
    print("Creating/Updating categories...")
    for cat in categories:
        try:
            # 1. Try to create
            url = f"{wp.api_url}/categories"
            response = requests.post(url, json=cat, auth=wp.auth)
            
            if response.status_code == 201:
                print(f"✓ Created category: {cat['name']}")
            elif response.status_code == 400 and "term_exists" in response.text:
                # 2. If exists, update
                print(f"- Category already exists: {cat['name']}. Updating...")
                
                # Get existing category ID
                # Since api_url already contains ?rest_route=..., we must use & for parameters
                get_url = f"{wp.api_url}/categories&slug={cat['slug']}"
                get_res = requests.get(get_url, auth=wp.auth)
                
                if get_res.status_code == 200 and len(get_res.json()) > 0:
                    cat_id = get_res.json()[0]['id']
                    update_url = f"{wp.api_url}/categories/{cat_id}"
                    # Update description
                    update_res = requests.post(update_url, json={'description': cat['description']}, auth=wp.auth)
                    
                    if update_res.status_code == 200:
                         print(f"  ✓ Updated description for: {cat['name']}")
                    else:
                         print(f"  ✗ Failed to update description: {update_res.text}")
                else:
                    print(f"  ✗ Could not find existing category ID for slug: {cat['slug']}")

            else:
                print(f"✗ Failed to create {cat['name']}: {response.text}")
        except Exception as e:
            print(f"✗ Error processing {cat['name']}: {e}")

def create_tags(wp):
    """Create all tags defined in sitemap.md with SEO descriptions."""
    tags = [
        # Region
        {
            "name": "Japan", 
            "slug": "japan",
            "description": "Insights into the Japanese logistics market, '2024 Problem', and government regulations. The source of Kaizen philosophy."
        },
        {
            "name": "North America", 
            "slug": "usa",
            "description": "Trends from the US logistics tech scene. Strategies from giants like Amazon and Walmart, and Silicon Valley startup movements."
        },
        {
            "name": "Europe", 
            "slug": "europe",
            "description": "Sustainable logistics examples from Europe. Advanced models of physical internet and city logistics."
        },
        {
            "name": "Asia-Pacific", 
            "slug": "asia-pacific",
            "description": "Logistics in the rapidly growing ASEAN and Chinese markets. Cross-border EC trends and manufacturing shifts."
        },
        
        # Industry
        {
            "name": "Manufacturing", 
            "slug": "manufacturing",
            "description": "Logistics strategies for manufacturers. JIT delivery, parts procurement optimization, and factory automation."
        },
        {
            "name": "Retail", 
            "slug": "retail",
            "description": "Supply chain solutions for the retail sector. Omnichannel logistics, store replenishment, and inventory visibility."
        },
        {
            "name": "eCommerce", 
            "slug": "ecommerce",
            "description": "Fulfillment strategies for online retailers. Fast shipping, returns management (reverse logistics), and packaging."
        },
        {
            "name": "3PL / Warehousing", 
            "slug": "3pl-warehouse",
            "description": "Trends for Third-Party Logistics providers and warehouse operators. Contract logistics, multi-client operations, and value-added services."
        },
        {
            "name": "Food & Beverage", 
            "slug": "food-beverage",
            "description": "Cold chain logistics and freshness management. HACCP compliance and temperature-controlled transportation."
        },
        {
            "name": "Apparel", 
            "slug": "apparel",
            "description": "Fashion logistics trends. Handling seasonality, SKU proliferation, and RFID implementation for inventory accuracy."
        },
        {
            "name": "Medical / Pharma", 
            "slug": "medical",
            "description": "Healthcare logistics and GDP compliance. Secure transport of pharmaceuticals and medical devices."
        },
        
        # Topics
        {
            "name": "Sustainability", 
            "slug": "sustainability",
            "description": "Green logistics, carbon neutrality, and ESG initiatives. Corporate responsibility in the supply chain."
        },
        {
            "name": "Labor Shortage", 
            "slug": "labor-shortage",
            "description": "Solutions for the labor crisis. Automation, work-sharing, and effective human resource management strategies."
        },
        {
            "name": "Last Mile", 
            "slug": "last-mile",
            "description": "Optimization of the final delivery leg. Drone delivery, locker systems, and efficient routing technologies."
        },
        {
            "name": "Warehouse Automation", 
            "slug": "automation",
            "description": "Deep dive into AS/RS, AGVs, AMRs, and robotic picking. How to automate warehouse operations for maximum efficiency."
        },
        {
            "name": "Kaizen", 
            "slug": "kaizen",
            "description": "The Japanese philosophy of continuous improvement. 5S, visual management, and waste reduction techniques applied to logistics."
        },
    ]
    
    print("\nCreating/Updating tags...")
    for tag in tags:
        try:
            # 1. Try to create
            url = f"{wp.api_url}/tags"
            response = requests.post(url, json=tag, auth=wp.auth)
            
            if response.status_code == 201:
                print(f"✓ Created tag: {tag['name']}")
            elif response.status_code == 400 and "term_exists" in response.text:
                # 2. If exists, update
                print(f"- Tag already exists: {tag['name']}. Updating...")
                
                # Get existing tag ID
                get_url = f"{wp.api_url}/tags&slug={tag['slug']}" # tags endpoint usually accepts ?slug parameter
                get_res = requests.get(get_url, auth=wp.auth)
                
                if get_res.status_code == 200 and len(get_res.json()) > 0:
                    tag_id = get_res.json()[0]['id']
                    update_url = f"{wp.api_url}/tags/{tag_id}"
                    # Update description
                    update_res = requests.post(update_url, json={'description': tag['description']}, auth=wp.auth)
                    
                    if update_res.status_code == 200:
                         print(f"  ✓ Updated description for: {tag['name']}")
                    else:
                         print(f"  ✗ Failed to update description: {update_res.text}")
                else:
                    print(f"  ✗ Could not find existing tag ID for slug: {tag['slug']}")
            else:
                print(f"✗ Failed to create {tag['name']}: {response.text}")
        except Exception as e:
            print(f"✗ Error processing {tag['name']}: {e}")

def main():
    print("=== WordPress Taxonomy Setup (Global) ===\n")
    try:
        wp = WordPressClient()
        create_categories(wp)
        create_tags(wp)
        print("\n✓ Setup complete!")
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")

if __name__ == "__main__":
    main()
