from flask import jsonify

def invalid_job_Info_exception():
    error_code = "JOB_MANAGER_SERVICE_1000"
    error_message = "The provided Job details is invalid or Empty"
    return jsonify({
        "error_code": error_code,
        "error_message": error_message,
    }), 400

def job_already_available_exception():
    error_code = "JOB_MANAGER_SERVICE_1001"
    error_message = "The provided jobId details is already in database"
    return jsonify({
        "error_code": error_code,
        "error_message": error_message,
    }), 409

def missing_fields_exception():
    error_code = "JOB_MANAGER_SERVICE_1002"
    error_message = "The provided details have some missing or invalid fields"
    return jsonify({
        "error_code": error_code,
        "error_message": error_message,
    }), 400

def email_not_found_exception():
    error_code = "JOB_MANAGER_SERVICE_1003"
    error_message = "The provided publisher email not available in database"
    return jsonify({
        "error_code": error_code,
        "error_message": error_message,
    }), 404