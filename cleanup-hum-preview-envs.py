"""
Script for cleaning up old preview environments to save resources.
"""

import os
from datetime import datetime, timedelta
import re
import requests
import pytz

utc=pytz.UTC

def job():
    try:
        HUMANITEC_URL = os.getenv("HUMANITEC_URL", default="https://api.humanitec.io")
        HUMANITEC_TOKEN = os.getenv("HUMANITEC_TOKEN")
        HUMANITEC_ORG = os.getenv("HUMANITEC_ORG")
        HUMANITEC_APP = os.getenv("HUMANITEC_APP")
        HUMANITEC_ENV_REGEX = os.getenv("HUMANITEC_ENV_REGEX")
        HUMANITEC_ENV_MAX_AGE_DAYS = os.getenv("HUMANITEC_ENV_MAX_AGE_DAYS", default="7")
    except:
        print("Missing environment variables.")
        exit()

    preview_env_regex = re.compile(rf"{HUMANITEC_ENV_REGEX}")
    max_env_age = datetime.utcnow() - timedelta(days=float(HUMANITEC_ENV_MAX_AGE_DAYS))
    max_env_age = utc.localize(max_env_age)

    headers = {"Authorization": f"Bearer {HUMANITEC_TOKEN}", "Content-Type": "application/json"}
    resp_env_list = requests.get(f"{HUMANITEC_URL}/orgs/{HUMANITEC_ORG}/apps/{HUMANITEC_APP}/envs", headers=headers)
    env_list = resp_env_list.json()
    if resp_env_list.status_code == 200:
        for env in env_list:
            if re.fullmatch(preview_env_regex, env['id']):
                print(f"ENV: {env['id']}, last deployed: {env['last_deploy']['created_at']} matches regex.")
                env_last_deploy_date = datetime.strptime(env['last_deploy']['created_at'], "%Y-%m-%dT%H:%M:%S.%f%z")
                if env_last_deploy_date <= max_env_age:
                    print(f"{env['id']}'s last deployment is older than {HUMANITEC_ENV_MAX_AGE_DAYS} day(s).")
                    resp_env_delete = requests.delete(f"{HUMANITEC_URL}/orgs/{HUMANITEC_ORG}/apps/{HUMANITEC_APP}/envs/{env['id']}", headers=headers)
                    if resp_env_delete.status_code == 204:
                        print(f"ENV {env['id']} has been deleted.")
                    else:
                        print(f"Delete request failed with status {resp_env_delete.status_code}")
    else:
        print(f"Listing environments failed with status {resp_env_list.status_code}")

if __name__ == "__main__":
    job()
