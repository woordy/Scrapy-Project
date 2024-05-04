import sys
import os

# Adjusting the path to ensure correct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.connection import session_scope, db_connect, create_tables
from database.models import Hospital


def test_db():
    engine = db_connect()
    create_tables(engine)  # This will create all necessary tables if they don't exist

    with session_scope() as session:
        try:
            # Inserting a new record
            new_hospital = Hospital(
                hospital_name="Test Hospital",
                city="Test City",
                state="FL",
                staffed_beds=10,
                total_discharges=5,
                patient_days=20,
                gross_patient_revenue=5000.00,
                free_profile="/test/profile",
                hospital_name_detail = "Test Hospital Detail",
                street_address_detail = "123 Main Street",
                city_detail = "Atlanta",
                state_detail = "PA",
                postal_code_detail = "90887",
                telephone_detail = "908-090-8976",
                website_detail = "www.yahoo.com",
                cms_no_detail = "676578",
                facility_type_detail = "Long Term",
                ownership_detail = "Private",
                staffed_beds_detail = 23,
                gross_patient_revenue_detail = 556.90,
                total_discharges_detail = 34,
                patient_days_detail = 45,
                quality_score_detail = None

            )
            session.add(new_hospital)
            session.flush()  # Flush to enforce constraints and make it retrievable in the same transaction
            print("Inserted:", new_hospital.hospital_name)

            # Retrieving the inserted record
            hospital = (
                session.query(Hospital).filter_by(hospital_name="Test Hospital").first()
            )
            if hospital:
                print(hospital)
                print("Retrieved:", hospital.hospital_name)

            # Deleting the record
            if hospital:
                session.delete(hospital)
                print("Deleted:", hospital.hospital_name)

            # Verifying deletion
            hospital_check = (
                session.query(Hospital).filter_by(hospital_name="Test Hospital").first()
            )
            if not hospital_check:
                print("Verification: The record has been successfully deleted.")
            else:
                print("Verification failed: The record is still present.")

        except Exception as e:
            print("An error occurred:", e)


if __name__ == "__main__":
    test_db()
