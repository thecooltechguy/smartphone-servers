import requests
SERVER_ENDPOINT = "http://localhost:5000"

submit_job_url = f"{SERVER_ENDPOINT}/jobs/submit/"

job_spec = {
    "code_url": "https://github.com/jfswitzer/ut_test.git",
    "resource_requirements" : {} # TODO: Later, when we add support for resource_requirements, test some real values for this
}

resp = requests.post(submit_job_url, json=job_spec).json()
print(resp)