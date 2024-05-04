# models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()


class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True)
    hospital_name = Column(String)
    city = Column(String)
    state = Column(String)
    staffed_beds = Column(Integer)
    total_discharges = Column(Integer)
    patient_days = Column(Integer)
    gross_patient_revenue = Column(Float)
    free_profile = Column(String)
    hospital_name_detail = Column(String)
    street_address_detail = Column(String)
    city_detail = Column(String)
    state_detail = Column(String)
    postal_code_detail = Column(String)
    telephone_detail = Column(String)
    website_detail = Column(String)
    cms_no_detail = Column(String)
    facility_type_detail = Column(String)
    ownership_detail = Column(String)
    staffed_beds_detail = Column(Integer)
    gross_patient_revenue_detail = Column(Float)
    total_discharges_detail = Column(Integer)
    patient_days_detail = Column(Integer)
    quality_score_detail = Column(Float)

    def __repr__(self):
        return f"<HospitalDetail(hospital_name='{self.hospital_name}', city='{self.city}', state='{self.state}', cms_no_detail='{self.cms_no_detail }', website_detail='{self.website_detail}')>"
