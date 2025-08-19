from dataclasses import asdict
from app.models.job_repo import Job ,Application
from flask_pymongo import PyMongo
from app.exceptions.custom_exceptions import job_already_available_exception
from app.utils.logger import get_logger
from pymongo.errors import DuplicateKeyError


logger = get_logger("Job_service")
class JobService:
    def __init__(self,mongo:PyMongo):
        self.mongo = mongo
        self.mongo.db.jobs.create_index("jobId", unique=True)

    def add_job(self,data:dict):
        logger.info(f"✅ Adding Job details.....{data}")
        job = Job(
            jobId=data["jobId"],
            jobTitle=data["jobTitle"],
            companyName=data["companyName"],
            applications=[Application(**app) for app in data.get("applications", [])]
        )

        try:
            self.mongo.db.jobs.insert_one(asdict(job))
            logger.info(f"✅ Job added successfully......")
            return {"message": "Job added successfully!"}
        except DuplicateKeyError:
            logger.warning(f"❌ Job with jobId '{data['jobId']}' already exists ")
            return job_already_available_exception()

    def add_application(self,application_data:dict,jobId):
        logger.info(f"✅ Adding new application for job id ➡️{jobId}")







