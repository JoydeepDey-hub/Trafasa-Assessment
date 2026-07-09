import os
import json
import logging
from typing import Dict, Any


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def simulate_ocr_and_llm_extraction(pdf_path: str) -> Dict[str, Any]:
    mock_extracted_json = """
    {
        "invoice_number": "INV-2026-8891",
        "invoice_date": "2026-07-01",
        "vendor_name": "Steel Pipes Global Ltd",
        "subtotal": 12000.00,
        "tax": 2160.00,
        "total_amount": 14160.00
    }
    """
    return json.loads(mock_extracted_json)

def validate_invoice_data(data: Dict[str, Any]) -> bool:
    try:
        subtotal = data.get("subtotal", 0.0)
        tax = data.get("tax", 0.0)
        total = data.get("total_amount", 0.0)
        
       
        return abs((subtotal + tax) - total) < 0.01
    except Exception:
        return False

def enqueue_to_human_review(pdf_path: str, raw_data: Dict[str, Any], reason: str):
    logging.warning(f"[FALLBACK TRIGGERED] Routing document '{pdf_path}' to human review queue.")
    logging.warning(f"Reason for escalation: {reason}")
   

def process_invoice_pipeline(pdf_path: str):
    print(f"--- Starting IDP Pipeline for: {os.path.basename(pdf_path)} ---")
    
    try:
       
        extracted_fields = simulate_ocr_and_llm_extraction(pdf_path)
        
        
        is_valid = validate_invoice_data(extracted_fields)
        
        if is_valid:
            logging.info("Extraction validation PASSED. Automatically saving to procurement database.")
            print("Final Saved Data:", json.dumps(extracted_fields, indent=2))
        else:
           
            enqueue_to_human_review(pdf_path, extracted_fields, "Mathematical validation failed (Subtotal + Tax != Total).")
            
    except json.JSONDecodeError as je:
        
        enqueue_to_human_review(pdf_path, {}, f"Critical Parsing Error: LLM returned invalid JSON string. Details: {str(je)}")
    except Exception as e:
        
        enqueue_to_human_review(pdf_path, {}, f"System / API Timeout Exception: {str(e)}")

if __name__ == "__main__":
    
    test_invoice = "workspace/receipts/invoice_001.pdf"
    process_invoice_pipeline(test_invoice)