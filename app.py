import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from data.frameworks import get_all_frameworks
from data.controls import get_all_controls, get_control_frameworks_mapping

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

@app.route('/')
def index():
    """Landing page with assessment overview."""
    frameworks = get_all_frameworks()
    return render_template('index.html', frameworks=frameworks)

@app.route('/frameworks')
def frameworks():
    """Page 1: Framework selection with checkboxes."""
    frameworks = get_all_frameworks()
    selected_frameworks = session.get('selected_frameworks', [])
    return render_template('frameworks.html', frameworks=frameworks, selected_frameworks=selected_frameworks)

@app.route('/select_frameworks', methods=['POST'])
def select_frameworks():
    """Handle framework selection and redirect to controls page."""
    selected_frameworks = request.form.getlist('frameworks')
    session['selected_frameworks'] = selected_frameworks
    return redirect(url_for('controls'))

@app.route('/controls')
def controls():
    """Page 2: Controls selection with checkboxes."""
    if 'selected_frameworks' not in session or not session['selected_frameworks']:
        return redirect(url_for('frameworks'))

    frameworks_data = get_all_frameworks()
    selected_frameworks = session['selected_frameworks']
    selected_controls = session.get('selected_controls', [])
    control_frameworks = get_control_frameworks_mapping()

    # Get controls only for selected frameworks
    from data.controls import get_controls_by_framework
    controls_by_framework = get_controls_by_framework()

    # Filter controls based on selected frameworks
    filtered_controls = set()
    for framework_id in selected_frameworks:
        # Map framework IDs to framework names
        framework_name_mapping = {
            'nist_csf': 'NIST CSF',
            'iso_27001': 'ISO/IEC 27001/27005',
            'cobit_2019': 'COBIT 2019',
            'rbi_cybersecurity': 'RBI Cybersecurity',
            'pci_dss': 'PCI-DSS v4.0',
            'hipaa': 'HIPAA',
            'iso_27001_enterprise': 'ISO 27001 (Enterprise/SaaS)',
            'cert_in': 'CERT-IN'
        }

        framework_name = framework_name_mapping.get(framework_id)
        if framework_name and framework_name in controls_by_framework:
            filtered_controls.update(controls_by_framework[framework_name])

    # Convert to list and sort
    filtered_controls = sorted(list(filtered_controls))

    return render_template('controls.html',
                         frameworks_data=frameworks_data,
                         selected_frameworks=selected_frameworks,
                         all_controls=filtered_controls,
                         selected_controls=selected_controls,
                         control_frameworks=control_frameworks)

@app.route('/select_controls', methods=['POST'])
def select_controls():
    """Handle controls selection and redirect to dashboard."""
    selected_controls = request.form.getlist('controls')
    session['selected_controls'] = selected_controls
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """Page 3: Dashboard showing results and analytics."""
    selected_frameworks = session.get('selected_frameworks', [])
    selected_controls = session.get('selected_controls', [])

    if not selected_frameworks or not selected_controls:
        return redirect(url_for('frameworks'))

    # Calculate analytics
    frameworks_data = get_all_frameworks()
    all_controls = get_all_controls()

    analytics = calculate_analytics(selected_frameworks, selected_controls, frameworks_data, all_controls)

    return render_template('dashboard.html', 
                         analytics=analytics,
                         selected_frameworks=selected_frameworks,
                         selected_controls=selected_controls,
                         frameworks_data=frameworks_data)

@app.route('/download_report')
def download_report():
    """Generate and download security assessment report in HTML format."""
    selected_frameworks = session.get('selected_frameworks', [])
    selected_controls = session.get('selected_controls', [])

    if not selected_frameworks or not selected_controls:
        return jsonify({"status": "error", "error": "No assessment data available"}), 400

    frameworks_data = get_all_frameworks()
    all_controls = get_all_controls()
    analytics = calculate_analytics(selected_frameworks, selected_controls, frameworks_data, all_controls)

    # Generate comprehensive report data
    import datetime
    from datetime import timezone
    import platform
    import socket

    # Get accurate current time with timezone info
    current_time = datetime.datetime.now()
    utc_time = datetime.datetime.utcnow()

    # Additional metadata for aphelioncyber compliance
    system_info = {
        'platform': platform.system(),
        'hostname': socket.gethostname(),
        'python_version': platform.python_version()
    }

    # Calculate risk categories
    missing_controls = analytics.get('missing_controls', [])
    technical_risks = [c for c in missing_controls if any(tech in c for tech in ['Network', 'Firewall', 'Patch', 'Vulnerability', 'SIEM', 'Monitoring'])]
    human_risks = [c for c in missing_controls if any(human in c for human in ['Training', 'Awareness', 'Education', 'User'])]
    governance_risks = [c for c in missing_controls if any(gov in c for gov in ['Policy', 'Governance', 'Compliance', 'Audit', 'Documentation'])]

    # Framework name mapping
    framework_name_mapping = {
        'nist_csf': 'NIST CSF',
        'iso_27001': 'ISO/IEC 27001/27005',
        'cobit_2019': 'COBIT 2019',
        'rbi_cybersecurity': 'RBI Cybersecurity',
        'pci_dss': 'PCI-DSS v4.0',
        'hipaa': 'HIPAA',
        'iso_27001_enterprise': 'ISO 27001 (Enterprise/SaaS)',
        'cert_in': 'CERT-IN'
    }

    # Prepare template data
    report_data = {
        'report_metadata': {
            'download_timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"),
            'utc_timestamp': utc_time.strftime("%Y-%m-%d %H:%M:%S UTC"),
            'report_title': 'aphelioncyber Cybersecurity Risk Assessment Report',
            'assessment_scope': 'Multi-Framework Security Control Assessment by aphelioncyber',
            'report_id': f"APHILION-RPT-{current_time.strftime('%Y%m%d-%H%M%S')}",
            'timezone': current_time.strftime("%Z") or "Local Time",
            'report_version': '2.1',
            'assessment_methodology': 'aphelioncyber Standard Risk Assessment Framework',
            'compliance_level': 'Enterprise Grade',
            'system_info': system_info,
            'report_classification': 'Confidential - aphelioncyber',
            'assessment_date_iso': current_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'next_assessment_due': (current_time + datetime.timedelta(days=90)).strftime("%B %d, %Y")
        },
        'analytics': analytics,
        'selected_frameworks': selected_frameworks,
        'selected_controls': selected_controls,
        'frameworks_data': frameworks_data,
        'framework_names': [framework_name_mapping.get(fw_id, fw_id) for fw_id in selected_frameworks],
        'missing_controls': missing_controls,
        'technical_risks': technical_risks,
        'human_risks': human_risks,
        'governance_risks': governance_risks,
        'risk_categories': {
            'technical': {
                'count': len(technical_risks),
                'percentage': round((len(technical_risks) / len(missing_controls) * 100) if missing_controls else 0, 1)
            },
            'human': {
                'count': len(human_risks),
                'percentage': round((len(human_risks) / len(missing_controls) * 100) if missing_controls else 0, 1)
            },
            'governance': {
                'count': len(governance_risks),
                'percentage': round((len(governance_risks) / len(missing_controls) * 100) if missing_controls else 0, 1)
            }
        }
    }

    # Render HTML report template
    html_content = render_template('report.html', **report_data)

    return jsonify({
        "status": "success",
        "html_content": html_content,
        "filename": f"cybersecurity_assessment_report_{current_time.strftime('%Y%m%d_%H%M%S')}.html",
        "download_time": current_time.strftime("%B %d, %Y at %I:%M %p")
    })

@app.route('/reset')
def reset():
    """Clear all selections and start over."""
    session.clear()
    return redirect(url_for('frameworks'))

def calculate_analytics(selected_frameworks, selected_controls, frameworks_data, all_controls):
    """Calculate precise security analytics and scores for aphelioncyber compliance assessment."""
    from data.controls import get_controls_by_framework

    # Get framework-specific controls with exact mapping
    controls_by_framework = get_controls_by_framework()
    framework_name_mapping = {
        'nist_csf': 'NIST CSF',
        'iso_27001': 'ISO/IEC 27001/27005',
        'cobit_2019': 'COBIT 2019',
        'rbi_cybersecurity': 'RBI Cybersecurity',
        'pci_dss': 'PCI-DSS v4.0',
        'hipaa': 'HIPAA',
        'iso_27001_enterprise': 'ISO 27001 (Enterprise/SaaS)',
        'cert_in': 'CERT-IN'
    }

    # Get applicable controls for selected frameworks with validation
    applicable_controls = set()
    framework_coverage = {}

    for framework_id in selected_frameworks:
        framework_name = framework_name_mapping.get(framework_id)
        if framework_name and framework_name in controls_by_framework:
            framework_controls = controls_by_framework[framework_name]
            applicable_controls.update(framework_controls)
            framework_coverage[framework_name] = len(framework_controls)

    applicable_controls = sorted(list(applicable_controls))
    total_applicable = len(applicable_controls)

    # Precise control implementation tracking
    implemented_controls = [c for c in selected_controls if c in applicable_controls]
    implemented_count = len(implemented_controls)
    missing_controls = [c for c in applicable_controls if c not in selected_controls]

    # Enterprise-standard coverage calculation (exact percentage)
    coverage_percentage = round((implemented_count / total_applicable * 100), 2) if total_applicable > 0 else 0

    # Enhanced security scoring methodology for enterprise compliance
    # Base coverage score (60% weight)
    coverage_score = coverage_percentage * 0.6

    # Critical controls assessment (30% weight) - Enterprise Priority Controls
    critical_controls = [
        'MFA (Multi-Factor Authentication)', 'Encryption at Rest', 'Encryption in Transit',
        'Access Control & Identity Management', 'Incident Response Plan', 
        'Backup & Disaster Recovery', 'Network Firewall & Segmentation',
        'Vulnerability Management & Scanning', 'SIEM (Security Information and Event Management)',
        'Privileged Access Management', 'Data Loss Prevention (DLP)', 'Security Awareness Training'
    ]

    critical_implemented = sum(1 for control in implemented_controls 
                              if any(crit.lower() in control.lower() for crit in critical_controls))
    critical_applicable = sum(1 for control in applicable_controls 
                             if any(crit.lower() in control.lower() for crit in critical_controls))

    critical_score = (critical_implemented / critical_applicable * 30) if critical_applicable > 0 else 0

    # Compliance framework alignment (10% weight)
    framework_alignment_score = min(len(selected_frameworks) * 2, 10)  # Max 10 points for framework diversity

    # Final security score calculation
    security_score = min(int(coverage_score + critical_score + framework_alignment_score), 100)

    # Enhanced risk categorization for accurate dashboard display
    missing_critical = [c for c in missing_controls 
                       if any(crit.lower() in c.lower() for crit in critical_controls)]

    # Technical risks - infrastructure and technical controls
    technical_keywords = ['Patch Management', 'Vulnerability', 'Firewall', 'Monitoring', 
                         'Authentication', 'Network Security', 'Endpoint Protection', 'Intrusion Detection',
                         'SIEM', 'Encryption', 'Antivirus', 'IDS', 'IPS', 'Security Tools']
    missing_high = [c for c in missing_controls 
                   if any(hp.lower() in c.lower() for hp in technical_keywords) 
                   and c not in missing_critical]

    # Human/operational risks - training, awareness, procedures
    human_keywords = ['Training', 'Awareness', 'Education', 'User', 'Phishing', 'Social Engineering',
                     'Security Culture', 'Staff', 'Employee', 'Personnel']
    missing_medium = [c for c in missing_controls 
                     if any(mp.lower() in c.lower() for mp in human_keywords) 
                     and c not in missing_critical and c not in missing_high]

    # Governance risks - policies, procedures, compliance
    governance_keywords = ['Policy', 'Procedure', 'Governance', 'Compliance', 'Audit', 'Documentation', 
                          'Risk Assessment', 'Management', 'Oversight', 'Review', 'Process']
    missing_low = [c for c in missing_controls 
                  if any(gk.lower() in c.lower() for gk in governance_keywords) 
                  and c not in missing_critical and c not in missing_high and c not in missing_medium]

    # Any remaining controls go to governance
    remaining_controls = [c for c in missing_controls 
                         if c not in missing_critical and c not in missing_high 
                         and c not in missing_medium and c not in missing_low]
    missing_low.extend(remaining_controls)

    # Enterprise-standard risk metrics
    risk_levels = {
        'critical': len(missing_critical),
        'high': len(missing_high),
        'medium': len(missing_medium),
        'low': len(missing_low)
    }

    # Calculate compliance percentage by framework
    framework_compliance = {}
    for framework_id in selected_frameworks:
        framework_name = framework_name_mapping.get(framework_id)
        if framework_name in controls_by_framework:
            fw_controls = controls_by_framework[framework_name]
            fw_implemented = len([c for c in selected_controls if c in fw_controls])
            fw_total = len(fw_controls)
            framework_compliance[framework_name] = round((fw_implemented / fw_total * 100), 2) if fw_total > 0 else 0

    # Calculate framework-specific missing controls
    framework_missing_controls = {}
    for framework_id in selected_frameworks:
        framework_name = framework_name_mapping.get(framework_id)
        if framework_name and framework_name in controls_by_framework:
            fw_controls = set(controls_by_framework[framework_name])
            fw_missing = [c for c in missing_controls if c in fw_controls]
            framework_missing_controls[framework_name] = len(fw_missing)

    return {
        'security_score': security_score,
        'coverage_percentage': coverage_percentage,
        'frameworks_selected': len(selected_frameworks),
        'total_frameworks': len(frameworks_data),
        'controls_implemented': implemented_count,
        'total_controls': total_applicable,
        'missing_controls': missing_controls,
        'missing_critical': missing_critical,
        'missing_high': missing_high,
        'missing_medium': missing_medium,
        'missing_low': missing_low,
        'implemented_controls': implemented_controls,
        'framework_compliance': framework_compliance,
        'framework_coverage': framework_coverage,
        'framework_missing_controls': framework_missing_controls,
        'critical_controls_status': {
            'implemented': critical_implemented,
            'total': critical_applicable,
            'percentage': round((critical_implemented / critical_applicable * 100), 2) if critical_applicable > 0 else 0
        },
        'risk_levels': risk_levels,
        'risk_distribution': {
            'technical_percent': round((len(missing_high) / len(missing_controls) * 100), 1) if missing_controls else 0,
            'human_percent': round((len(missing_medium) / len(missing_controls) * 100), 1) if missing_controls else 0,
            'governance_percent': round(((len(missing_critical) + len(missing_low)) / len(missing_controls) * 100), 1) if missing_controls else 0
        },
        'recommendations': generate_recommendations(selected_controls, missing_controls, selected_frameworks)
    }

def generate_recommendations(selected_controls, missing_controls, selected_frameworks):
    """Generate security recommendations based on missing controls and selected frameworks."""
    recommendations = []

    # If no missing controls, don't generate any recommendations (perfect security posture)
    if not missing_controls:
        return []

    # Critical missing controls
    critical_controls = [
        'MFA (Multi-Factor Authentication)', 'Encryption', 'Access Control', 
        'Incident Response Plan', 'Backup & Recovery', 'Network Firewall'
    ]
    missing_critical = [c for c in missing_controls if any(crit in c for crit in critical_controls)]

    if missing_critical:
        recommendations.append({
            'title': 'CRITICAL: Implement essential security controls immediately',
            'description': f'Missing critical controls: {", ".join(missing_critical[:3])}{"..." if len(missing_critical) > 3 else ""}',
            'priority': 'critical'
        })

    # Only show framework-specific recommendations if there are missing controls for those frameworks
    framework_recommendations = {
        'nist_csf': 'Implement NIST Cybersecurity Framework core functions',
        'iso_27001': 'Establish Information Security Management System (ISMS)',
        'pci_dss': 'Secure cardholder data environment and payment processes',
        'hipaa': 'Protect healthcare information and ensure patient data privacy',
        'rbi_cybersecurity': 'Meet Reserve Bank of India cybersecurity requirements',
        'cobit_2019': 'Align IT governance with business objectives',
        'cert_in': 'Follow national cybersecurity guidelines and incident reporting',
        'iso_27001_enterprise': 'Implement cloud-specific security controls'
    }

    # Check if any selected framework has missing controls before showing framework recommendations
    from data.controls import get_controls_by_framework
    controls_by_framework = get_controls_by_framework()
    framework_name_mapping = {
        'nist_csf': 'NIST CSF',
        'iso_27001': 'ISO/IEC 27001/27005',
        'cobit_2019': 'COBIT 2019',
        'rbi_cybersecurity': 'RBI Cybersecurity',
        'pci_dss': 'PCI-DSS v4.0',
        'hipaa': 'HIPAA',
        'iso_27001_enterprise': 'ISO 27001 (Enterprise/SaaS)',
        'cert_in': 'CERT-IN'
    }

    for framework_id in selected_frameworks:
        framework_name = framework_name_mapping.get(framework_id)
        if framework_name and framework_name in controls_by_framework:
            fw_controls = set(controls_by_framework[framework_name])
            fw_missing = [c for c in missing_controls if c in fw_controls]
            
            # Only add framework recommendation if this framework has missing controls
            if fw_missing and framework_id in framework_recommendations:
                recommendations.append({
                    'title': f'Framework Compliance: {framework_recommendations[framework_id]}',
                    'description': f'Focus on {len(fw_missing)} missing controls specific to {framework_id.replace("_", " ").title()} requirements',
                    'priority': 'high'
                })

    # Specific missing control categories
    if any('Patch' in c or 'Vulnerability' in c for c in missing_controls):
        recommendations.append({
            'title': 'Vulnerability Management: Implement patch management and vulnerability scanning',
            'description': 'Regular vulnerability assessments and timely patching are essential',
            'priority': 'high'
        })

    if any('Monitoring' in c or 'SIEM' in c or 'Logging' in c for c in missing_controls):
        recommendations.append({
            'title': 'Security Monitoring: Deploy comprehensive monitoring and logging',
            'description': 'Implement SIEM, continuous monitoring, and audit trail capabilities',
            'priority': 'high'
        })

    if any('Training' in c or 'Awareness' in c for c in missing_controls):
        recommendations.append({
            'title': 'Human Factor Security: Establish security awareness training program',
            'description': 'Regular training reduces risk of human error and social engineering',
            'priority': 'medium'
        })

    if any('Backup' in c or 'Recovery' in c or 'Continuity' in c for c in missing_controls):
        recommendations.append({
            'title': 'Business Continuity: Implement robust backup and disaster recovery',
            'description': 'Ensure business continuity with tested backup and recovery procedures',
            'priority': 'medium'
        })

    return recommendations[:6]  # Return top 6 recommendations

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6767 , debug=True)