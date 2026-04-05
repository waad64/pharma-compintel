"""
Template System - Reusable templates for 17 standardized CI reports
Each template defines structure, sections, and data requirements
"""

from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ReportTemplate:
    """Base template structure for CI reports"""
    name: str
    description: str
    sections: List[str]
    required_data_fields: List[str]
    ci_domains: List[str]
    key_metrics: List[str]


class TemplateLibrary:
    """Library of 17 standardized report templates"""
    
    TEMPLATES = {
        "Clinical Positioning Analysis": ReportTemplate(
            name="Clinical Positioning Analysis",
            description="Analyze clinical development stage and competitive positioning",
            sections=[
                "Executive Summary",
                "Clinical Phase Distribution",
                "Trial Status Overview",
                "Disease Area Focus",
                "Competitive Positioning",
                "Key Findings",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Trial_Clinical_Phase",
                "Trial_Overall_Status",
                "Disease",
                "Disease_Area",
                "Company_Name"
            ],
            ci_domains=[
                "Clinical Maturity",
                "Pipeline Diversification",
                "Innovation Index"
            ],
            key_metrics=[
                "Phase III Trial Count",
                "Active Trial Percentage",
                "Disease Area Diversity",
                "Clinical Maturity Score"
            ]
        ),
        
        "Regulatory Risk Assessment": ReportTemplate(
            name="Regulatory Risk Assessment",
            description="Assess regulatory pathway risks and market access challenges",
            sections=[
                "Executive Summary",
                "Regulatory Milestone Timeline",
                "Risk Factors",
                "Market Access Status",
                "Regulatory Strength Analysis",
                "Recommendations",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Trial_Overall_Status",
                "Trial_Clinical_Phase",
                "Company_Name",
                "Lead_Product"
            ],
            ci_domains=[
                "Regulatory Strength",
                "Financial Stability",
                "Clinical Maturity"
            ],
            key_metrics=[
                "Completed Trial Percentage",
                "Regulatory Risk Score",
                "Time-to-Market Estimate",
                "Regulatory Strength Score"
            ]
        ),
        
        "Financial Exposure Report": ReportTemplate(
            name="Financial Exposure Report",
            description="Analyze financial metrics and investment exposure",
            sections=[
                "Executive Summary",
                "Market Capitalization Analysis",
                "Financial Stability Assessment",
                "Investment Risk Profile",
                "Competitive Financial Position",
                "Financial Outlook",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Market_Cap",
                "Last_Sale",
                "Company_Name",
                "Investor_Highlights"
            ],
            ci_domains=[
                "Financial Stability",
                "Partnership Activity",
                "Clinical Maturity"
            ],
            key_metrics=[
                "Average Market Cap",
                "Market Cap Range",
                "Financial Stability Score",
                "Investment Risk Level"
            ]
        ),
        
        "Time-to-Market Benchmarking": ReportTemplate(
            name="Time-to-Market Benchmarking",
            description="Benchmark time-to-market across competitors",
            sections=[
                "Executive Summary",
                "Phase Progression Timeline",
                "Competitive Timeline Comparison",
                "Acceleration Factors",
                "Delay Risk Factors",
                "Market Entry Forecast",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Trial_Clinical_Phase",
                "Trial_Overall_Status",
                "Company_Name",
                "Lead_Product"
            ],
            ci_domains=[
                "Clinical Maturity",
                "Regulatory Strength",
                "Innovation Index"
            ],
            key_metrics=[
                "Average Phase Duration",
                "Phase Progression Rate",
                "Time-to-Market Score",
                "Competitive Advantage Index"
            ]
        ),
        
        "Competitive Density Mapping": ReportTemplate(
            name="Competitive Density Mapping",
            description="Map competitive density across disease areas and indications",
            sections=[
                "Executive Summary",
                "Disease Area Competitive Density",
                "Indication-Level Competition",
                "Competitive Landscape Heatmap",
                "White Space Opportunities",
                "Strategic Recommendations",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Disease_Area",
                "Disease",
                "Company_Name",
                "Trial_Clinical_Phase"
            ],
            ci_domains=[
                "Pipeline Diversification",
                "Competitive Density",
                "Innovation Index"
            ],
            key_metrics=[
                "Competitors per Disease Area",
                "Indication Saturation Index",
                "White Space Score",
                "Competitive Density Score"
            ]
        ),
        
        "Partnership & Licensing Activity": ReportTemplate(
            name="Partnership & Licensing Activity",
            description="Track partnerships, collaborations, and licensing deals",
            sections=[
                "Executive Summary",
                "Partnership Overview",
                "Collaboration Types",
                "Licensing Activity",
                "Strategic Partnerships",
                "Partnership Impact Analysis",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Partnerships",
                "Company_Name",
                "Lead_Product",
                "Disease_Area"
            ],
            ci_domains=[
                "Partnership Activity",
                "Innovation Index",
                "Financial Stability"
            ],
            key_metrics=[
                "Partnership Count",
                "Active Collaborations",
                "Licensing Deal Value",
                "Partnership Activity Score"
            ]
        ),
        
        "Innovation Strength Assessment": ReportTemplate(
            name="Innovation Strength Assessment",
            description="Assess innovation capabilities and technology platforms",
            sections=[
                "Executive Summary",
                "Technology Platform Analysis",
                "Innovation Pipeline",
                "IP Strength Assessment",
                "Competitive Innovation Position",
                "Future Innovation Outlook",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Technology",
                "Lead_Product",
                "Company_Name",
                "Trial_Clinical_Phase"
            ],
            ci_domains=[
                "Innovation Index",
                "Pipeline Diversification",
                "Partnership Activity"
            ],
            key_metrics=[
                "Technology Diversity Score",
                "Innovation Pipeline Strength",
                "IP Portfolio Score",
                "Innovation Index Score"
            ]
        ),
        
        "Patent Landscape Analysis": ReportTemplate(
            name="Patent Landscape Analysis",
            description="Analyze patent portfolios and IP landscape",
            sections=[
                "Executive Summary",
                "Patent Portfolio Overview",
                "Patent Expiry Timeline",
                "Freedom to Operate Analysis",
                "Competitive Patent Position",
                "IP Strategy Assessment",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Company_Name",
                "Lead_Product",
                "Technology"
            ],
            ci_domains=[
                "Innovation Index",
                "Regulatory Strength",
                "Financial Stability"
            ],
            key_metrics=[
                "Patent Count",
                "Patent Expiry Score",
                "FTO Risk Level",
                "IP Strength Score"
            ]
        ),
        
        "Pipeline Monitoring Report": ReportTemplate(
            name="Pipeline Monitoring Report",
            description="Monitor and track development pipelines",
            sections=[
                "Executive Summary",
                "Pipeline Overview",
                "Phase Distribution",
                "Pipeline Progression",
                "Risk Assessment",
                "Pipeline Strength Analysis",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Company_Name",
                "Trial_Clinical_Phase",
                "Disease",
                "Lead_Product"
            ],
            ci_domains=[
                "Clinical Maturity",
                "Pipeline Diversification",
                "Regulatory Strength"
            ],
            key_metrics=[
                "Total Pipeline Size",
                "Phase Distribution",
                "Pipeline Strength Score",
                "Development Velocity"
            ]
        ),
        
        "Market Access & Pricing Report": ReportTemplate(
            name="Market Access & Pricing Report",
            description="Analyze market access strategies and pricing dynamics",
            sections=[
                "Executive Summary",
                "Market Access Status",
                "Pricing Strategy Analysis",
                "Reimbursement Landscape",
                "Competitive Pricing Position",
                "Market Access Recommendations",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Company_Name",
                "Lead_Product",
                "Market_Cap",
                "Disease_Area"
            ],
            ci_domains=[
                "Regulatory Strength",
                "Financial Stability",
                "Clinical Maturity"
            ],
            key_metrics=[
                "Market Access Score",
                "Pricing Competitiveness",
                "Reimbursement Status",
                "Market Access Strength"
            ]
        ),
        
        "Regulatory Landscape Report": ReportTemplate(
            name="Regulatory Landscape Report",
            description="Map regulatory environment and approval pathways",
            sections=[
                "Executive Summary",
                "Regulatory Pathway Overview",
                "Approval Timeline Analysis",
                "Regulatory Requirements",
                "Competitive Regulatory Position",
                "Regulatory Outlook",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Trial_Overall_Status",
                "Trial_Clinical_Phase",
                "Company_Name",
                "Disease_Area"
            ],
            ci_domains=[
                "Regulatory Strength",
                "Clinical Maturity",
                "Financial Stability"
            ],
            key_metrics=[
                "Approval Rate",
                "Regulatory Timeline",
                "Regulatory Complexity Score",
                "Regulatory Strength Score"
            ]
        ),
        
        "Clinical Trial Competitive Intelligence": ReportTemplate(
            name="Clinical Trial Competitive Intelligence",
            description="Detailed clinical trial competitive analysis",
            sections=[
                "Executive Summary",
                "Trial Portfolio Overview",
                "Enrollment Trends",
                "Trial Design Comparison",
                "Competitive Trial Position",
                "Trial Outcome Analysis",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Trial_NCT_ID",
                "Trial_Clinical_Phase",
                "Trial_Overall_Status",
                "Company_Name",
                "Disease"
            ],
            ci_domains=[
                "Clinical Maturity",
                "Innovation Index",
                "Pipeline Diversification"
            ],
            key_metrics=[
                "Active Trial Count",
                "Enrollment Rate",
                "Trial Success Rate",
                "Clinical Trial Score"
            ]
        ),
        
        "Early Warning Report": ReportTemplate(
            name="Early Warning Report",
            description="Identify emerging threats and opportunities",
            sections=[
                "Executive Summary",
                "Emerging Threats",
                "Opportunity Signals",
                "Market Disruption Indicators",
                "Competitive Moves",
                "Strategic Recommendations",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Company_Name",
                "Trial_Overall_Status",
                "Partnerships",
                "Lead_Product"
            ],
            ci_domains=[
                "Innovation Index",
                "Partnership Activity",
                "Clinical Maturity"
            ],
            key_metrics=[
                "Threat Level",
                "Opportunity Score",
                "Disruption Risk",
                "Early Warning Score"
            ]
        ),
        
        "Competitive Landscape Report": ReportTemplate(
            name="Competitive Landscape Report",
            description="Comprehensive competitive landscape analysis",
            sections=[
                "Executive Summary",
                "Market Overview",
                "Competitive Positioning",
                "Competitor Profiles",
                "Market Share Analysis",
                "Competitive Dynamics",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Company_Name",
                "Market_Cap",
                "Disease_Area",
                "Trial_Clinical_Phase"
            ],
            ci_domains=[
                "Financial Stability",
                "Clinical Maturity",
                "Pipeline Diversification"
            ],
            key_metrics=[
                "Market Share",
                "Competitive Position",
                "Market Concentration",
                "Landscape Score"
            ]
        ),
        
        "Competitor Sales & Market Share Report": ReportTemplate(
            name="Competitor Sales & Market Share Report",
            description="Analyze competitor sales and market share",
            sections=[
                "Executive Summary",
                "Sales Performance",
                "Market Share Distribution",
                "Growth Trends",
                "Competitive Sales Position",
                "Market Share Forecast",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Company_Name",
                "Market_Cap",
                "Last_Sale",
                "Disease_Area"
            ],
            ci_domains=[
                "Financial Stability",
                "Clinical Maturity",
                "Partnership Activity"
            ],
            key_metrics=[
                "Sales Growth Rate",
                "Market Share %",
                "Revenue Trend",
                "Sales Competitiveness"
            ]
        ),
        
        "Patent Expiry & Biosimilar Entry Report": ReportTemplate(
            name="Patent Expiry & Biosimilar Entry Report",
            description="Track patent expirations and biosimilar threats",
            sections=[
                "Executive Summary",
                "Patent Expiry Timeline",
                "Biosimilar Entry Forecast",
                "Revenue Impact Analysis",
                "Mitigation Strategies",
                "Competitive Biosimilar Landscape",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Company_Name",
                "Lead_Product",
                "Market_Cap"
            ],
            ci_domains=[
                "Financial Stability",
                "Innovation Index",
                "Regulatory Strength"
            ],
            key_metrics=[
                "Patent Cliff Timeline",
                "Biosimilar Threat Level",
                "Revenue at Risk",
                "Patent Expiry Score"
            ]
        ),
        
        "Freedom to Operate Assessment": ReportTemplate(
            name="Freedom to Operate Assessment",
            description="Assess freedom to operate and IP risks",
            sections=[
                "Executive Summary",
                "FTO Analysis",
                "Patent Infringement Risk",
                "Licensing Requirements",
                "Competitive FTO Position",
                "Risk Mitigation Strategies",
                "CI Domain Scores"
            ],
            required_data_fields=[
                "Company_Name",
                "Lead_Product",
                "Technology"
            ],
            ci_domains=[
                "Innovation Index",
                "Regulatory Strength",
                "Financial Stability"
            ],
            key_metrics=[
                "FTO Risk Level",
                "Infringement Probability",
                "Licensing Cost Estimate",
                "FTO Score"
            ]
        )
    }
    
    @classmethod
    def get_template(cls, report_type: str) -> ReportTemplate:
        """Get template by report type"""
        return cls.TEMPLATES.get(report_type)
    
    @classmethod
    def list_templates(cls) -> List[str]:
        """List all available templates"""
        return list(cls.TEMPLATES.keys())
    
    @classmethod
    def get_template_sections(cls, report_type: str) -> List[str]:
        """Get sections for a specific report type"""
        template = cls.get_template(report_type)
        return template.sections if template else []
    
    @classmethod
    def get_required_fields(cls, report_type: str) -> List[str]:
        """Get required data fields for a report type"""
        template = cls.get_template(report_type)
        return template.required_data_fields if template else []
