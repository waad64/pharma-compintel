"""
Batch Report Generator - Generate all 17 reports automatically
Orchestrates report generation for multiple report types with filtering
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd

from report_generator import ReportGenerator, ReportType
from report_templates import TemplateLibrary
from data_pipeline import DataPipeline


class BatchReportGenerator:
    """Generate all 17 standardized reports in batch"""
    
    def __init__(self, csv_path: str, output_dir: str = "reports_output"):
        self.csv_path = csv_path
        self.output_dir = output_dir
        self.report_generator = ReportGenerator(csv_path)
        self.template_library = TemplateLibrary()
        self.pipeline = DataPipeline(csv_path)
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_single_report(self, report_type: ReportType, 
                              filters: Optional[Dict] = None) -> Dict:
        """Generate a single report"""
        
        # Load data
        self.report_generator.load_data(self.csv_path)
        
        # Apply filters
        if filters:
            df_filtered = self.report_generator.apply_filters(**filters)
        else:
            df_filtered = self.report_generator.df
        
        # Generate report
        report = self.report_generator.generate_report(report_type, df_filtered)
        
        return report
    
    def generate_all_reports(self, filters: Optional[Dict] = None) -> Dict[str, Dict]:
        """Generate all 17 reports"""
        
        all_reports = {}
        report_types = [
            ReportType.CLINICAL_POSITIONING,
            ReportType.REGULATORY_RISK,
            ReportType.FINANCIAL_EXPOSURE,
            ReportType.TIME_TO_MARKET,
            ReportType.COMPETITIVE_DENSITY,
            ReportType.PARTNERSHIP_LICENSING,
            ReportType.INNOVATION_STRENGTH,
            ReportType.PATENT_LANDSCAPE,
            ReportType.PIPELINE_MONITORING,
            ReportType.MARKET_ACCESS,
            ReportType.REGULATORY_LANDSCAPE,
            ReportType.CLINICAL_TRIALS,
            ReportType.EARLY_WARNING,
            ReportType.COMPETITIVE_LANDSCAPE,
            ReportType.SALES_MARKET_SHARE,
            ReportType.PATENT_EXPIRY,
            ReportType.FTO_ASSESSMENT
        ]
        
        for report_type in report_types:
            print(f"Generating: {report_type.value}...")
            report = self.generate_single_report(report_type, filters)
            all_reports[report_type.value] = report
        
        return all_reports
    
    def generate_by_company(self, company_name: str) -> Dict[str, Dict]:
        """Generate all reports for a specific company"""
        filters = {"company_name": company_name}
        return self.generate_all_reports(filters)
    
    def generate_by_disease_area(self, disease_area: str) -> Dict[str, Dict]:
        """Generate all reports for a specific disease area"""
        filters = {"disease_area": disease_area}
        return self.generate_all_reports(filters)
    
    def export_reports(self, reports: Dict[str, Dict], format: str = "json") -> List[str]:
        """Export all reports"""
        exported_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for report_name, report_data in reports.items():
            # Sanitize filename
            safe_name = report_name.replace(" ", "_").replace("&", "and").lower()
            filename = f"{safe_name}_{timestamp}.{format}"
            filepath = os.path.join(self.output_dir, filename)
            
            if format == "json":
                with open(filepath, 'w') as f:
                    json.dump(report_data, f, indent=2, default=str)
            
            elif format == "csv":
                # Export CI scores as CSV
                scores_data = []
                for domain, score_info in report_data.get("ci_domain_scores", {}).items():
                    scores_data.append({
                        "Report": report_name,
                        "Domain": domain,
                        "Score": score_info.get("score"),
                        "CI_Lower": score_info.get("ci_lower"),
                        "CI_Upper": score_info.get("ci_upper")
                    })
                
                df_scores = pd.DataFrame(scores_data)
                df_scores.to_csv(filepath, index=False)
            
            exported_files.append(filepath)
        
        return exported_files
    
    def generate_summary_report(self, reports: Dict[str, Dict]) -> Dict:
        """Generate summary of all reports"""
        summary = {
            "generation_date": datetime.now().isoformat(),
            "total_reports": len(reports),
            "reports": {}
        }
        
        for report_name, report_data in reports.items():
            summary["reports"][report_name] = {
                "data_records": report_data.get("metadata", {}).get("data_records"),
                "ci_scores": {
                    domain: {
                        "score": score_info.get("score"),
                        "ci_lower": score_info.get("ci_lower"),
                        "ci_upper": score_info.get("ci_upper")
                    }
                    for domain, score_info in report_data.get("ci_domain_scores", {}).items()
                }
            }
        
        return summary
    
    def run_batch_generation(self, filters: Optional[Dict] = None, 
                            export_format: str = "json") -> Dict:
        """Run complete batch generation workflow"""
        
        print("Starting batch report generation...")
        
        # Generate all reports
        reports = self.generate_all_reports(filters)
        
        # Export reports
        exported_files = self.export_reports(reports, export_format)
        
        # Generate summary
        summary = self.generate_summary_report(reports)
        
        # Export summary
        summary_path = os.path.join(self.output_dir, 
                                   f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"Batch generation completed. {len(reports)} reports generated.")
        print(f"Output directory: {self.output_dir}")
        
        return {
            "status": "completed",
            "reports_generated": len(reports),
            "exported_files": exported_files,
            "summary_path": summary_path
        }


def main():
    """Main execution function"""
    
    # Configuration
    csv_path = "clinical_trials_extracted.csv"
    output_dir = "reports_output"
    
    # Initialize batch generator
    batch_gen = BatchReportGenerator(csv_path, output_dir)
    
    # Option 1: Generate all reports (no filters)
    result = batch_gen.run_batch_generation(export_format="json")
    
    # Option 2: Generate reports for specific company
    # result = batch_gen.run_batch_generation(
    #     filters={"company_name": "Absci Corporation Common Stock"},
    #     export_format="json"
    # )
    
    # Option 3: Generate reports for specific disease area
    # result = batch_gen.run_batch_generation(
    #     filters={"disease_area": "Neurodegenerative Disorders"},
    #     export_format="json"
    # )
    
    print("\nBatch Generation Results:")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
