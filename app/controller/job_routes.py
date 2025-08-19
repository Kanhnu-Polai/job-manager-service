from flask import Flask, request, jsonify
from app.utils.logger import get_logger
from flask_pymongo import PyMongo
from app.config import DevelopmentConfig , ProductionConfig
from app.exceptions.custom_exceptions import invalid_job_Info_exception,missing_fields_exception
import os
from app.service.job_service import JobService
app = Flask(__name__)

if os.getenv("FLASK_ENV") == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

mongo = PyMongo(app)
job_service = JobService(mongo)
logger = get_logger("AppRoutes")

# To add job details for the very first time
@app.route("/add_job", methods=["POST"])
def add_job_info():
    logger.info("✅ Inside add_job_info() method....... ")
    job_info = request.get_json()

    if not job_info:
        logger.warning("❌ Failed - Empty Job Info received")
        return invalid_job_Info_exception()

    logger.info(f"✅ Received Job Info : {job_info}")
    result = job_service.add_job(job_info)

    logger.info(f"✅ Result from add JobService : {result}")

    return result

# To add a new application details on each new candidate, apply for the respective job id
@app.route("/application",methods = ["POST"])
def add_application():
    logger.info("✅ Inside add_application() method....... ")
    job_application_info = request.get_json()

    if not job_application_info:
        return invalid_job_Info_exception()

    required_fild= ["jobId","applicationId", "applicant_email", "status"]

    if not all(field in job_application_info for field in required_fild):
        return missing_fields_exception()

    job_id = job_application_info["jobId"]
    application = {
        "applicationId" : job_application_info["applicationId"],
        "applicant_email" : job_application_info["applicant_email"],
        "status":job_application_info["status"]
    }



if __name__ == "__main__":
    app.run(debug=True, port=5000)