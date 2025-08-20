from dataclasses import asdict
from flask import jsonify
from app.models.job_repo import Job ,Application
from flask_pymongo import PyMongo
from app.exceptions.custom_exceptions import job_already_available_exception ,email_not_found_exception
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


    def get_job_applications_by_publisher_email(self,publisher_email):
        logger.info(f"✅ Getting request form controller with publisher email ➡️{publisher_email}")
        logger.info(f"🧿 Validating the publisher email")

        # Check if email exists in DB
        existing_publisher = self.mongo.db.jobs.find_one({"publisher_email":publisher_email})

        if not existing_publisher:
            logger.warning(f"❌ No jobs found for publisher {publisher_email}")
            return email_not_found_exception()

        logger.info(f"✅ Validation successful...")
        logger.info(f"✅Fetch all jobs for the publisher")

        jobs_info = self.mongo.db.jobs.find({"publisher_email":publisher_email})
        job_list = []

        for job in jobs_info:
            job["_id"]=str(job["_id"])
            job_list.append(job)

        return jsonify(job_list)















