# Define your item pipelines here
import sys
import os

# Adjusting the Python path to ensure modules from two levels up are importable
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from database.connection import session_scope  # Importing the session context manager
from database.models import Hospital

class HospitalPipeline:
    
    def process_item(self, item, spider): # type: ignore
        with session_scope() as session:
            hospital = Hospital(**item)
            session.add(hospital)
        return item
