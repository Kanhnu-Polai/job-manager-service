from dataclasses import dataclass
from typing import List

@dataclass
class Application:
    applicationId: str
    applicant_email: str
    status: str  # e.g. "APPLIED", "REVIEWED", "ACCEPTED", "REJECTED"
    resume_link:str

@dataclass
class Job:
    jobId: str
    publisher_email:str
    jobTitle: str
    companyName: str
    applications: List[Application]  # list of Application objects