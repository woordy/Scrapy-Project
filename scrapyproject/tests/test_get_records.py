# test_get_records.py

import sys
import os

# Adjusting the path to ensure correct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.connection import session_scope  
from database.models import Hospital


def print_hospital_records():
    with session_scope() as session:
        try:
            # Query all records in the Hospital table
            records = session.query(Hospital).all()
            for record in records:
                print(
                    f"ID: {record.id}, Name: {record.hospital_name}, City: {record.city}, "
                    f"State: {record.state}, Beds: {record.staffed_beds}, Discharges: {record.total_discharges}, "
                    f"Patient Days: {record.patient_days}, Revenue: {record.gross_patient_revenue}, "
                    f"Profile: {record.free_profile}"
                )
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    print_hospital_records()
