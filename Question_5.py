import os
import json
import logging
from typing import Dict, Any

# Set up logging for tracking failures and human-in-the-loop escalations
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def simulate_ocr_and_llm_extraction(pdf_path: str) -> Dict[str, Any]:
    """
    Simulates extracting structured text from an invoice PDF using an OCR layer
    and an LLM function call requesting strict JSON output.
    """
    # Mocking successful extraction based on typical LLM structured output
    # In production, this would use an API client like: openai.chat.completions.create()
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
    """
    Programmatic validation layer to protect against LLM hallucinations.
    Checks if Subtotal + Tax equals the Total Amount.
    """
    try:
        subtotal = data.get("subtotal", 0.0)
        tax = data.get("tax", 0.0)
        total = data.get("total_amount", 0.0)
        
        # Check mathematical consistency
        return abs((subtotal + tax) - total) < 0.01
    except Exception:
        return False

def enqueue_to_human_review(pdf_path: str, raw_data: Dict[str, Any], reason: str):
    """
    Simulates pushing a failed or low-confidence invoice to a Redis Queue (RQ)
    so it can be manually reviewed by a team member in the Frappe dashboard.
    """
    logging.warning(f"[FALLBACK TRIGGERED] Routing document '{pdf_path}' to human review queue.")
    logging.warning(f"Reason for escalation: {reason}")
    # In real pipeline: redis_queue.enqueue(frappe_dashboard.create_review_task, pdf_path, raw_data)

def process_invoice_pipeline(pdf_path: str):
    """
    Main pipeline coordinating extraction, mathematical validation, and fallback logic.
    """
    print(f"--- Starting IDP Pipeline for: {os.path.basename(pdf_path)} ---")
    
    try:
        # Step 1: Run Extraction
        extracted_fields = simulate_ocr_and_llm_extraction(pdf_path)
        
        # Step 2: Run Mathematical Validation
        is_valid = validate_invoice_data(extracted_fields)
        
        if is_valid:
            logging.info("Extraction validation PASSED. Automatically saving to procurement database.")
            print("Final Saved Data:", json.dumps(extracted_fields, indent=2))
        else:
            # Fallback Tier 1: Math Mismatch / Hallucination detected
            enqueue_to_human_review(pdf_path, extracted_fields, "Mathematical validation failed (Subtotal + Tax != Total).")
            
    except json.JSONDecodeError as je:
        # Fallback Tier 2: LLM failed to return valid parseable JSON output
        enqueue_to_human_review(pdf_path, {}, f"Critical Parsing Error: LLM returned invalid JSON string. Details: {str(je)}")
    except Exception as e:
        # Fallback Tier 3: Unexpected system or API timeout failure
        enqueue_to_human_review(pdf_path, {}, f"System / API Timeout Exception: {str(e)}")

if __name__ == "__main__":
    # Test path simulation
    test_invoice = "workspace/receipts/invoice_001.pdf"
    process_invoice_pipeline(test_invoice)