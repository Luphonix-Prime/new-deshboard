"""
Cybersecurity frameworks data for framework selection.
Contains basic framework information for the selection page.
"""

def get_all_frameworks():
    """Return all cybersecurity frameworks for selection page."""
    return {
        'nist_csf': {
            'name': 'NIST CSF (Cybersecurity Framework)',
            'description': 'The NIST framework is US-based and focuses on identifying, protecting, detecting, responding to, and recovering from cybersecurity threats.',
            'icon': 'fas fa-shield-alt',
            'color': '#9c27b0'
        },
        'iso_27001': {
            'name': 'ISO/IEC 27001/27005',
            'description': 'International standard for managing information security. Emphasizes confidentiality, integrity, and availability.',
            'icon': 'fas fa-certificate',
            'color': '#673ab7'
        },
        'cobit_2019': {
            'name': 'COBIT 2019',
            'description': 'A governance framework focusing on aligning IT goals with business objectives.',
            'icon': 'fas fa-cogs',
            'color': '#8e24aa'
        },
        'rbi_cybersecurity': {
            'name': 'RBI Cybersecurity',
            'description': "India's Reserve Bank compliance framework for financial institutions.",
            'icon': 'fas fa-university',
            'color': '#7b1fa2'
        },
        'pci_dss': {
            'name': 'PCI-DSS v4.0',
            'description': 'Security standard for organizations handling cardholder data.',
            'icon': 'fas fa-credit-card',
            'color': '#6a1b9a'
        },
        'hipaa': {
            'name': 'HIPAA',
            'description': 'U.S. healthcare regulation emphasizing patient data privacy.',
            'icon': 'fas fa-user-md',
            'color': '#9c27b0'
        },
        'iso_27001_enterprise': {
            'name': 'ISO 27001 (Enterprise/SaaS)',
            'description': 'Cloud-specific interpretation of ISO 27001 for SaaS or large-scale systems.',
            'icon': 'fas fa-cloud-upload-alt',
            'color': '#673ab7'
        },
        'cert_in': {
            'name': 'CERT-IN',
            'description': "India's national cybersecurity incident response body.",
            'icon': 'fas fa-flag',
            'color': '#8e24aa'
        }
    }