import time 
import logging

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")

def fetch_vendor_data(vendor_ids):
    mock_db = {
        "V001": {"name": "Alpha Corp", "rating": 4.5},
        "V002": {"name": "Beta Ltd", "rating": 3.8},
        "V004": {"name": "Delta Inc", "rating": 4.9},
    }

    vendors_retrieved={}
    for id in vendor_ids:

        time.sleep(0.5)
        if id in  mock_db:
            vendors_retrieved[id]=mock_db[id]
        else:
            logging.warning(f"Vendor ID {id} is not found in the given database")

    return vendors_retrieved

#Example
testing_ids=["V001","V002","V003","V004"]
print("Fetching vendor data....")
results=fetch_vendor_data(testing_ids)
print("\nRetrieved vendor ids are:")
print(results)

    