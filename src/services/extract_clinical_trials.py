import openpyxl
import requests
import pandas as pd
import json
import time
from urllib.parse import quote
import csv
import os

# Setup base directory for relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load the Excel file
excel_file = os.path.join(BASE_DIR, 'pharma_compintel_latest 25-March-2026.xlsx')
wb = openpyxl.load_workbook(excel_file)
ws = wb.active

# Extract data from Excel
companies_data = []
for row in ws.iter_rows(min_row=4, values_only=True):
    if row[1]:  # Check if symbol exists
        companies_data.append({
            'symbol': row[1],
            'name': row[2],
            'disease_area': row[18],
            'disease': row[17],
            'lead_product': row[20],
            'clinical_phase': row[19],
            'technology': row[23],
            'partnerships': row[24],
            'competition_level': row[32],
            'investor_highlights': row[29],
            'trial_id': row[34],
            'link_clinical_trials': row[13],
            'link_NCT': row[35]
        })

print(f"Loaded {len(companies_data)} companies from Excel")

# API endpoint
API_BASE = "https://clinicaltrials.gov/api/v2/studies"

# Store results
all_trials = []

def search_clinicaltrials_api(query, company_name, disease_area):
    """Search clinicaltrials.gov API"""
    try:
        # Try searching by company name first
        params = {
            'query.term': company_name,
            'pageSize': 100,
            'format': 'json'
        }
        
        response = requests.get(API_BASE, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('totalCount', 0) > 0:
            return data.get('studies', [])
        
        # If no results, try searching by disease area
        if disease_area:
            params = {
                'query.term': disease_area,
                'pageSize': 100,
                'format': 'json'
            }
            response = requests.get(API_BASE, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('studies', [])
        
        return []
    
    except Exception as e:
        print(f"Error searching for {company_name}: {str(e)}")
        return []

def extract_trial_details(study):
    """Extract relevant details from a trial"""
    try:
        protocol = study.get('protocolSection', {})
        identification = protocol.get('identificationModule', {})
        status = protocol.get('statusModule', {})
        conditions = protocol.get('conditionsModule', {})
        design = protocol.get('designModule', {})
        
        nct_id = identification.get('nctId', 'N/A')
        title = identification.get('officialTitle', 'N/A')
        
        # Extract diseases/conditions
        disease_list = conditions.get('conditions', [])
        diseases = ' | '.join(disease_list) if disease_list else 'N/A'
        
        # Extract clinical phase
        phases = design.get('phases', [])
        clinical_phase = ' | '.join(phases) if phases else 'N/A'
        
        # Extract study type
        study_type = design.get('studyType', 'N/A')
        
        # Extract status
        overall_status = status.get('overallStatus', 'N/A')
        
        return {
            'nct_id': nct_id,
            'title': title,
            'diseases': diseases,
            'clinical_phase': clinical_phase,
            'study_type': study_type,
            'overall_status': overall_status
        }
    except Exception as e:
        print(f"Error extracting trial details: {str(e)}")
        return None

# Process each company
for idx, company in enumerate(companies_data):
    print(f"\n[{idx+1}/{len(companies_data)}] Processing: {company['name']}")
    
    # Search API
    trials = search_clinicaltrials_api(
        company['name'],
        company['name'],
        company['disease_area']
    )
    
    if trials:
        print(f"  Found {len(trials)} trials")
        for trial in trials:
            trial_details = extract_trial_details(trial)
            if trial_details:
                all_trials.append({
                    'Company_Symbol': company['symbol'],
                    'Company_Name': company['name'],
                    'Disease_Area': company['disease_area'],
                    'Disease': company['disease'],
                    'Lead_Product': company['lead_product'],
                    'Clinical_Phase': company['clinical_phase'],
                    'Technology': company['technology'],
                    'Partnerships': company['partnerships'],
                    'Competition_Level': company['competition_level'],
                    'Investor_Highlights': company['investor_highlights'],
                    'Trial_NCT_ID': trial_details['nct_id'],
                    'Trial_Title': trial_details['title'],
                    'Trial_Diseases': trial_details['diseases'],
                    'Trial_Clinical_Phase': trial_details['clinical_phase'],
                    'Trial_Study_Type': trial_details['study_type'],
                    'Trial_Overall_Status': trial_details['overall_status']
                })
    else:
        print(f"  No trials found")
    
    # Rate limiting
    time.sleep(0.5)

print(f"\n\nTotal trials extracted: {len(all_trials)}")

# Create DataFrame
df = pd.DataFrame(all_trials)

# Save to CSV
csv_file = os.path.join(BASE_DIR, 'clinical_trials_extracted.csv')
df.to_csv(csv_file, index=False, encoding='utf-8')
print(f"CSV saved: {csv_file}")

# Save to Excel
excel_output = os.path.join(BASE_DIR, 'clinical_trials_extracted.xlsx')
df.to_excel(excel_output, index=False, sheet_name='Clinical Trials')
print(f"Excel saved: {excel_output}")

print("\nExtraction complete!")
