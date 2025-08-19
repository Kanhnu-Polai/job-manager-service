from dataclasses import asdict
from flask import jsonify
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
            publisher_email=data["publisherEmail"],
            applications=[Application(**app) for app in data.get("applications", [])]
        )

        try:
            self.mongo.db.jobs.insert_one(asdict(job))
            logger.info(f"✅ Job added successfully......")
            return {"message": "Job added successfully!"}
        except DuplicateKeyError:
            logger.warning(f"❌ Job with jobId '{data['jobId']}' already exists ")
            return job_already_available_exception()

    def add_application(self,application_data:dict,job_id):
        logger.info(f"✅ Adding new application for job id ➡️{job_id}")
        application = Application(**application_data)

        result = self.mongo.db.jobs.update_one(
            {"jobId": job_id},
            {"$push": {"applications": asdict(application)}}
        )

        if result.matched_count == 0:
            return jsonify({"error": f"No job found with jobId {job_id}"}), 404

        return jsonify({
            "message": f"Application added successfully to job {job_id}",
            "application": asdict(application)
        }), 200












