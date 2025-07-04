
"""
Cybersecurity controls data extracted from all frameworks.
Contains the complete list of security controls across all supported frameworks.
"""

def get_all_controls():
    """Return the complete list of all security controls across all frameworks."""
    return [
        # NIST CSF Controls
        "Asset Inventory",
        "Network Firewall",
        "IDS/IPS (Intrusion Detection/Prevention System)",
        "MFA (Multi-Factor Authentication)",
        "RBAC (Role-Based Access Control)",
        "Patch Management",
        "Security Awareness Training",
        "SIEM (Security Information and Event Management)",
        "Encryption",
        "Backup & Recovery",
        "Incident Response Plan",
        "Vulnerability Scanning",
        "Penetration Testing",
        "Configuration Management",
        "Risk Register",

        # ISO/IEC 27001/27005 Controls
        "Information Classification",
        "Access Control Policy",
        "Authentication & Authorization",
        "Physical and Environmental Security",
        "Secure Backup Procedures",
        "Logging & Monitoring",
        "Supplier Risk Management",
        "Secure Network Design",
        "Data Protection & Encryption",
        "Security Incident Handling",
        "Business Continuity Planning",
        "Secure Disposal of Assets",
        "Mobile Device Controls",
        "Internal Audit",

        # COBIT 2019 Controls
        "IT Governance Structure",
        "Strategic Risk Management",
        "Compliance Management",
        "Change Control",
        "Security Logging & Audit Trails",
        "Identity & Access Management",
        "Incident & Problem Management",
        "IT Asset Management",
        "Threat Monitoring",
        "Policy & Procedure Management",
        "Resource Optimization",
        "Performance Metrics",
        "Third-Party Risk Management",

        # RBI Cybersecurity Framework Controls
        "CISO Appointment & Governance",
        "Network Segmentation",
        "ATM & SWIFT Isolation",
        "User Access Reviews",
        "VA/PT Testing",
        "Email Security Controls",
        "Incident Reporting to RBI",
        "SIEM/SOC Operations",
        "DLP (Data Loss Prevention)",
        "Application Whitelisting",
        "Malware Detection",
        "Backup & Recovery Testing",
        "Board-Level Cyber Reporting",

        # PCI-DSS v4.0 Controls
        "Network Firewall Configuration",
        "CHD Encryption (Cardholder Data)",
        "Tokenization",
        "Access Logging & Monitoring",
        "Anti-Malware Protection",
        "Segmentation Testing",
        "Physical Security",
        "Secure Configuration Standards",
        "Key Management",
        "Audit Log Retention",

        # HIPAA Controls
        "Access Control",
        "Audit Control",
        "Integrity Checks",
        "Data Encryption",
        "Physical Facility Access",
        "Device Security Policies",
        "User Activity Monitoring",
        "Contingency Planning",
        "Breach Notification",
        "Workforce Security Policies",

        # ISO 27001 (Enterprise/SaaS) Controls
        "Cloud Access Control",
        "DevOps Security Controls",
        "Secure SDLC Practices",
        "API Gateway Security",
        "Secure API Authentication",
        "Vulnerability Management",
        "Configuration Baselines",
        "Container Security",
        "Key Rotation Policies",
        "Secure Remote Access",
        "Data Residency Compliance",
        "Service Availability Monitoring",

        # CERT-IN Controls
        "Public Sector Threat Reporting",
        "Log Retention",
        "EDR (Endpoint Detection & Response)",
        "DNS Security Controls",
        "Zero Trust Implementation",
        "National Incident Alert Handling",
        "System Hardening Benchmarks",
        "Public Cloud Security Baselines",
        "Cyber Drill Participation",
        "Web Application Security Review"
    ]

def get_control_frameworks_mapping():
    """Return mapping of each control to its frameworks."""
    frameworks_by_control = {}
    controls_by_framework = get_controls_by_framework()

    for framework, controls in controls_by_framework.items():
        for control in controls:
            if control not in frameworks_by_control:
                frameworks_by_control[control] = []
            frameworks_by_control[control].append(framework)

    return frameworks_by_control

def get_controls_by_framework():
    """Return controls organized by framework."""
    return {
        "NIST CSF": [
            "Asset Inventory",
            "Network Firewall",
            "IDS/IPS (Intrusion Detection/Prevention System)",
            "MFA (Multi-Factor Authentication)",
            "RBAC (Role-Based Access Control)",
            "Patch Management",
            "Security Awareness Training",
            "SIEM (Security Information and Event Management)",
            "Encryption",
            "Backup & Recovery",
            "Incident Response Plan",
            "Vulnerability Scanning",
            "Penetration Testing",
            "Configuration Management",
            "Risk Register"
        ],
        "ISO/IEC 27001/27005": [
            "Information Classification",
            "Access Control Policy",
            "Authentication & Authorization",
            "Physical and Environmental Security",
            "Secure Backup Procedures",
            "Logging & Monitoring",
            "Supplier Risk Management",
            "Secure Network Design",
            "Data Protection & Encryption",
            "Patch Management",
            "Security Incident Handling",
            "Business Continuity Planning",
            "Secure Disposal of Assets",
            "Mobile Device Controls",
            "Internal Audit"
        ],
        "COBIT 2019": [
            "IT Governance Structure",
            "Strategic Risk Management",
            "Compliance Management",
            "Change Control",
            "Security Logging & Audit Trails",
            "Identity & Access Management",
            "Business Process Controls",
            "IT Performance Management",
            "Resource Optimization",
            "Information Architecture",
            "Service Level Management",
            "Vendor Management",
            "Data Quality Management",
            "IT Project Management",
            "Benefits Realization"
        ],
        "RBI Cybersecurity": [
            "Board Oversight",
            "Cyber Security Policy",
            "Organizational Structure",
            "Baseline Security Requirements",
            "Advanced Persistent Threat Detection",
            "Customer Education & Awareness",
            "Incident Response & Recovery",
            "Cyber Crisis Management Plan",
            "Inter-Bank Connectivity Security",
            "Mobile Payment Security",
            "Outsourcing Security",
            "Cyber Forensics & Evidence Management",
            "Business Continuity Planning",
            "Information Sharing & Intelligence",
            "Testing of Cyber Resilience"
        ],
        "PCI-DSS v4.0": [
            "Install & Maintain Network Security Controls",
            "Apply Secure Configurations",
            "Protect Stored Account Data",
            "Protect Cardholder Data with Strong Cryptography",
            "Protect All Systems & Networks from Malicious Software",
            "Develop & Maintain Secure Systems & Software",
            "Restrict Access by Business Need-to-Know",
            "Identify Users & Authenticate Access",
            "Restrict Physical Access to Cardholder Data",
            "Log & Monitor All Access",
            "Test Security of Systems & Networks Regularly",
            "Support Information Security with Organizational Policies"
        ],
        "HIPAA": [
            "Assigned Security Responsibility",
            "Workforce Training & Access Management",
            "Information Access Management",
            "Security Awareness & Training",
            "Security Incident Procedures",
            "Contingency Plan",
            "Evaluation",
            "Business Associate Contracts",
            "Facility Access Controls",
            "Workstation Use",
            "Device & Media Controls",
            "Access Control",
            "Audit Controls",
            "Integrity",
            "Person or Entity Authentication",
            "Transmission Security"
        ],
        "ISO 27001 (Enterprise/SaaS)": [
            "Cloud Security Architecture",
            "Multi-Tenant Data Isolation",
            "API Security Controls",
            "Container Security",
            "DevSecOps Integration",
            "Automated Security Testing",
            "Scalable Identity Management",
            "Service Mesh Security",
            "Cloud Access Security Broker (CASB)",
            "Zero Trust Network Architecture",
            "Microservices Security",
            "Data Loss Prevention (DLP)",
            "Cloud Workload Protection",
            "Security Orchestration & Response",
            "Compliance Automation"
        ],
        "CERT-IN": [
            "Incident Reporting",
            "Vulnerability Disclosure",
            "Cyber Threat Intelligence",
            "Security Advisory Compliance",
            "Critical Infrastructure Protection",
            "Cyber Security Framework Implementation",
            "Sectoral CERT Coordination",
            "Malware Analysis & Response",
            "Phishing & Social Engineering Defense",
            "Mobile & IoT Security",
            "Cloud Security Guidelines",
            "Cyber Forensics",
            "Capacity Building Programs",
            "International Cooperation",
            "Research & Development"
        ]
    }
