"""NAICS Industry Code Mapping and Descriptions.

Provides mappings from 2-digit sector codes and common 6-digit NAICS codes
to plain-English business categories.
"""

# 2-digit NAICS Sectors
SECTORS = {
    "11": "Agriculture, Forestry, Fishing and Hunting",
    "21": "Mining, Quarrying, and Oil and Gas Extraction",
    "22": "Utilities (Electric, Gas, Water)",
    "23": "Construction (General, Civil, Specialty Trades)",
    "31": "Manufacturing (Food, Beverage, Textiles)",
    "32": "Manufacturing (Wood, Paper, Chemicals, Plastics)",
    "33": "Manufacturing (Metals, Machinery, Electronics)",
    "42": "Wholesale Trade (B2B Merchant Wholesalers)",
    "44": "Retail Trade (Motor Vehicles, Electronics, Food, Building)",
    "45": "Retail Trade (General Merchandise, E-commerce, Sporting)",
    "48": "Transportation and Warehousing (Air, Rail, Trucking, Pipeline)",
    "49": "Transportation and Warehousing (Postal, Couriers, Warehousing)",
    "51": "Information (Publishing, Telecom, Data Processing, Software)",
    "52": "Finance and Insurance (Banking, Credit, Securities, Insurance)",
    "53": "Real Estate and Rental and Leasing",
    "54": "Professional, Scientific, and Technical Services (Legal, Accounting, IT)",
    "55": "Management of Companies and Enterprises (Holding Companies)",
    "56": "Administrative and Support and Waste Management and Remediation",
    "61": "Educational Services (Schools, Colleges, Training)",
    "62": "Health Care and Social Assistance (Hospitals, Clinics, Doctors)",
    "71": "Arts, Entertainment, and Recreation (Fitness, Amusements, Venues)",
    "72": "Accommodation and Food Services (Hotels, Restaurants, Bars)",
    "81": "Other Services (Repair, Maintenance, Personal Care, Laundry)",
    "92": "Public Administration (Government, Courts, Public Safety)",
}

# Common 6-digit NAICS Descriptions frequently found in Texas Comptroller data
COMMON_NAICS = {
    "236115": "New Single-Family Housing Construction",
    "236116": "New Multifamily Housing Construction",
    "236220": "Commercial and Institutional Building Construction",
    "238210": "Electrical Contractors and Other Wiring Installation",
    "238220": "Plumbing, Heating, and Air-Conditioning Contractors",
    "238160": "Roofing Contractors",
    "441110": "New Car Dealers",
    "441120": "Used Car Dealers",
    "445110": "Supermarkets and Other Grocery Retailers",
    "445120": "Convenience Retailers",
    "447110": "Gasoline Stations with Convenience Stores",
    "448140": "Family Clothing Retailers",
    "531110": "Lessors of Residential Buildings and Dwellings",
    "531210": "Offices of Real Estate Agents and Brokers",
    "541110": "Offices of Lawyers",
    "541211": "Offices of Certified Public Accountants",
    "541330": "Engineering Services",
    "541511": "Custom Computer Programming Services",
    "541512": "Computer Systems Design Services",
    "541611": "Administrative Management and General Management Consulting",
    "541810": "Advertising Agencies",
    "561720": "Janitorial Services",
    "561730": "Landscaping Services",
    "621111": "Offices of Physicians (except Mental Health Specialists)",
    "621210": "Offices of Dentists",
    "713940": "Fitness and Recreational Sports Centers",
    "721110": "Hotels (except Casino Hotels) and Motels",
    "722511": "Full-Service Restaurants",
    "722513": "Limited-Service Restaurants (Fast Food)",
    "722514": "Cafeterias, Grill Buffets, and Buffets",
    "722515": "Snack and Nonalcoholic Beverage Bars (Coffee, Smoothies)",
    "811111": "General Automotive Repair",
    "811121": "Automotive Body, Paint, and Interior Repair",
    "812112": "Beauty Salons",
    "812111": "Barber Shops",
}

# Organization Type Codes used by Texas Comptroller
ORG_TYPES = {
    "CL": "Limited Liability Company (LLC)",
    "CT": "Texas Corporation",
    "CF": "Foreign Corporation (Out-of-State)",
    "SP": "Sole Proprietorship / Individual",
    "PA": "General Partnership",
    "LP": "Limited Partnership (LP)",
    "LL": "Limited Liability Partnership (LLP)",
    "GS": "Government / School District / State Agency",
    "NP": "Non-Profit Corporation",
    "TR": "Trust",
    "ET": "Estate",
    "CI": "Corporation / Corporate Entity",
}


def get_naics_description(naics_code: str) -> str:
    """Return the detailed or sector-level description for a NAICS code."""
    if not naics_code:
        return "Unclassified / Unknown"
    code = str(naics_code).strip()
    if code in COMMON_NAICS:
        return COMMON_NAICS[code]
    sector = code[:2]
    if sector in SECTORS:
        return SECTORS[sector]
    return f"NAICS Industry Code {code}"


def get_org_type_description(org_code: str) -> str:
    """Return the human-readable entity organization type."""
    if not org_code:
        return "Unknown"
    return ORG_TYPES.get(str(org_code).upper().strip(), f"Type {org_code}")
