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

    required_job_fields = ["jobId", "jobTitle", "companyName", "publisherEmail"]
    missing_job_fields = [field for field in required_job_fields if field not in job_info or not job_info[field]]

    if missing_job_fields:
        logger.warning(f"❌ Missing required job fields: {missing_job_fields}")
        return missing_fields_exception()

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

    required_field= ["jobId","applicationId", "applicant_email", "status","resume_link"]

    if not all(field in job_application_info for field in required_field):
        return missing_fields_exception()

    job_id = job_application_info["jobId"]
    application = {
        "applicationId" : job_application_info["applicationId"],
        "applicant_email" : job_application_info["applicant_email"],
        "status":job_application_info["status"],
        "resume_link":job_application_info["resume_link"]

    }
    logger.info("✅ Sending the Job application and jobId to the service layer to update database")
    response = job_service.add_application(application,job_id)
    return response



# This end points is responsible for fetching all applicants for the job publisher using email


@app.route("/applications/<publisher_email>",methods=["GET"])
def get_applications(publisher_email):
    logger.info(f"✅Inside get_applications method.......  ")
    logger.info(f"✅Received a request to find all applications for the publisher email : {publisher_email}" )

    response = job_service.get_job_applications_by_publisher_email(publisher_email)

    return response

if __name__ == "__main__":
    app.run(debug=True, port=5000)