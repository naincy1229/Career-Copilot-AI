def get_companies_by_domain(domain):
    domain = domain.lower()
    mapping = {
        "data analyst": ["Mu Sigma", "Fractal Analytics", "Tredence", "Accenture", "ZS Associates"],
        "ui ux": ["Razorpay", "Swiggy", "CRED", "Tata Digital", "Flipkart"],
        "web developer": ["Wipro", "Cognizant", "TCS", "Mindtree", "LTI"],
        "machine learning": ["HCL", "Quantiphi", "Incedo", "Google", "Amazon"],
        "cybersecurity": ["Palo Alto Networks", "KPMG", "EY", "CrowdStrike", "Cisco"],
        "devops": ["TCS", "Zensar", "Infosys", "AWS", "RedHat"]
    }
    return mapping.get(domain, [])
