"""
Data Pipeline - Extract → Process → Score → Export
Orchestrates the complete data flow for report generation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import json


class DataExtractor:
    """Extract raw data from multiple sources"""
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None
    
    def extract_from_csv(self) -> pd.DataFrame:
        """Extract data from CSV file"""
        self.df = pd.read_csv(self.csv_path)
        return self.df
    
    def extract_by_company(self, company_name: str) -> pd.DataFrame:
        """Extract data for specific company"""
        return self.df[self.df['Company_Name'] == company_name]
    
    def extract_by_disease_area(self, disease_area: str) -> pd.DataFrame:
        """Extract data for specific disease area"""
        return self.df[self.df['Disease_Area'] == disease_area]
    
    def extract_by_phase(self, phase: str) -> pd.DataFrame:
        """Extract data for specific clinical phase"""
        return self.df[self.df['Trial_Clinical_Phase'] == phase]
    
    def get_unique_values(self, column: str) -> List:
        """Get unique values for a column"""
        return self.df[column].unique().tolist()


class DataProcessor:
    """Process and transform raw data"""
    
    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize data"""
        df_clean = df.copy()
        
        # Handle missing values
        df_clean['Market_Cap'] = pd.to_numeric(df_clean['Market_Cap'], errors='coerce')
        df_clean['Last_Sale'] = pd.to_numeric(df_clean['Last_Sale'], errors='coerce')
        
        # Standardize text fields
        df_clean['Trial_Overall_Status'] = df_clean['Trial_Overall_Status'].fillna('UNKNOWN')
        df_clean['Trial_Clinical_Phase'] = df_clean['Trial_Clinical_Phase'].fillna('UNKNOWN')
        
        return df_clean
    
    @staticmethod
    def aggregate_by_company(df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate data by company"""
        agg_dict = {
            'Trial_NCT_ID': 'nunique',
            'Disease': 'nunique',
            'Disease_Area': 'nunique',
            'Market_Cap': 'first',
            'Last_Sale': 'first',
            'Partnerships': lambda x: x.notna().sum()
        }
        
        return df.groupby('Company_Name').agg(agg_dict).reset_index()
    
    @staticmethod
    def aggregate_by_disease(df: pd.DataFrame) -> pd.DataFrame:
        """Aggregate data by disease area"""
        agg_dict = {
            'Company_Name': 'nunique',
            'Trial_NCT_ID': 'nunique',
            'Trial_Clinical_Phase': lambda x: x.value_counts().to_dict()
        }
        
        return df.groupby('Disease_Area').agg(agg_dict).reset_index()
    
    @staticmethod
    def calculate_phase_distribution(df: pd.DataFrame) -> Dict[str, int]:
        """Calculate phase distribution"""
        return df['Trial_Clinical_Phase'].value_counts().to_dict()
    
    @staticmethod
    def calculate_status_distribution(df: pd.DataFrame) -> Dict[str, int]:
        """Calculate trial status distribution"""
        return df['Trial_Overall_Status'].value_counts().to_dict()
    
    @staticmethod
    def calculate_disease_distribution(df: pd.DataFrame, top_n: int = 10) -> Dict[str, int]:
        """Calculate disease distribution"""
        return df['Disease'].value_counts().head(top_n).to_dict()


class DataScorer:
    """Score data for CI metrics"""
    
    @staticmethod
    def score_clinical_maturity(df: pd.DataFrame) -> float:
        """Score clinical maturity (0-100)"""
        phase_weights = {
            "PHASE1": 20, "PHASE2": 40, "PHASE3": 70, "PHASE4": 90,
            "EARLY_PHASE1": 10, "UNKNOWN": 30
        }
        
        scores = [phase_weights.get(phase, 30) for phase in df['Trial_Clinical_Phase']]
        return np.mean(scores) if scores else 50
    
    @staticmethod
    def score_regulatory_strength(df: pd.DataFrame) -> float:
        """Score regulatory strength (0-100)"""
        status_weights = {
            "COMPLETED": 80, "ACTIVE_NOT_RECRUITING": 60,
            "RECRUITING": 50, "TERMINATED": 20, "UNKNOWN": 30
        }
        
        scores = [status_weights.get(status, 40) for status in df['Trial_Overall_Status']]
        return np.mean(scores) if scores else 50
    
    @staticmethod
    def score_pipeline_diversity(df: pd.DataFrame) -> float:
        """Score pipeline diversity (0-100)"""
        unique_diseases = df['Disease'].nunique()
        unique_areas = df['Disease_Area'].nunique()
        
        diversity_score = min(100, (unique_diseases + unique_areas * 2) * 5)
        return diversity_score
    
    @staticmethod
    def score_financial_stability(df: pd.DataFrame) -> float:
        """Score financial stability (0-100)"""
        market_caps = pd.to_numeric(df['Market_Cap'], errors='coerce').dropna()
        
        if len(market_caps) == 0:
            return 50
        
        # Normalize to 0-100 scale
        median_cap = market_caps.median()
        avg_cap = market_caps.mean()
        
        if median_cap > 0:
            score = 50 + 20 * np.log10(avg_cap / median_cap)
            return np.clip(score, 20, 95)
        
        return 50
    
    @staticmethod
    def score_partnership_activity(df: pd.DataFrame) -> float:
        """Score partnership activity (0-100)"""
        partnership_count = df['Partnerships'].notna().sum()
        total_records = len(df)
        
        partnership_ratio = partnership_count / total_records if total_records > 0 else 0
        score = 30 + (partnership_ratio * 70)
        
        return np.clip(score, 0, 100)
    
    @staticmethod
    def score_innovation_index(df: pd.DataFrame) -> float:
        """Score innovation index (0-100)"""
        tech_count = df['Technology'].notna().sum()
        total_records = len(df)
        
        tech_ratio = tech_count / total_records if total_records > 0 else 0
        score = 40 + (tech_ratio * 60)
        
        return np.clip(score, 0, 100)


class DataExporter:
    """Export processed data and reports"""
    
    @staticmethod
    def export_to_json(data: Dict, output_path: str):
        """Export data to JSON"""
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    @staticmethod
    def export_to_csv(df: pd.DataFrame, output_path: str):
        """Export data to CSV"""
        df.to_csv(output_path, index=False)
    
    @staticmethod
    def export_to_excel(df: pd.DataFrame, output_path: str):
        """Export data to Excel"""
        df.to_excel(output_path, index=False)
    
    @staticmethod
    def export_report_summary(report: Dict, output_path: str):
        """Export report summary"""
        summary = {
            "report_type": report.get("metadata", {}).get("report_type"),
            "generated_date": report.get("metadata", {}).get("generated_date"),
            "data_records": report.get("metadata", {}).get("data_records"),
            "ci_scores": {
                domain: {
                    "score": scores.get("score"),
                    "ci_lower": scores.get("ci_lower"),
                    "ci_upper": scores.get("ci_upper")
                }
                for domain, scores in report.get("ci_domain_scores", {}).items()
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(summary, f, indent=2)


class DataPipeline:
    """Orchestrates complete data pipeline: Extract → Process → Score → Export"""
    
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.extractor = DataExtractor(csv_path)
        self.processor = DataProcessor()
        self.scorer = DataScorer()
        self.exporter = DataExporter()
        
        self.raw_data = None
        self.processed_data = None
        self.scores = None
    
    def extract(self) -> pd.DataFrame:
        """Step 1: Extract raw data"""
        self.raw_data = self.extractor.extract_from_csv()
        return self.raw_data
    
    def process(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """Step 2: Process and transform data"""
        if df is None:
            df = self.raw_data
        
        self.processed_data = self.processor.clean_data(df)
        return self.processed_data
    
    def score(self, df: Optional[pd.DataFrame] = None) -> Dict[str, float]:
        """Step 3: Calculate CI scores"""
        if df is None:
            df = self.processed_data
        
        self.scores = {
            "Clinical Maturity": self.scorer.score_clinical_maturity(df),
            "Regulatory Strength": self.scorer.score_regulatory_strength(df),
            "Pipeline Diversification": self.scorer.score_pipeline_diversity(df),
            "Financial Stability": self.scorer.score_financial_stability(df),
            "Partnership Activity": self.scorer.score_partnership_activity(df),
            "Innovation Index": self.scorer.score_innovation_index(df)
        }
        
        return self.scores
    
    def export(self, output_format: str = "json", output_path: str = None) -> str:
        """Step 4: Export results"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"report_{timestamp}.{output_format}"
        
        if output_format == "json":
            report = {
                "metadata": {
                    "generated_date": datetime.now().isoformat(),
                    "data_records": len(self.processed_data)
                },
                "ci_scores": self.scores
            }
            self.exporter.export_to_json(report, output_path)
        
        elif output_format == "csv":
            self.exporter.export_to_csv(self.processed_data, output_path)
        
        return output_path
    
    def run_pipeline(self, output_format: str = "json") -> Dict:
        """Run complete pipeline"""
        self.extract()
        self.process()
        self.score()
        output_path = self.export(output_format)
        
        return {
            "status": "completed",
            "records_processed": len(self.processed_data),
            "scores": self.scores,
            "output_path": output_path
        }
