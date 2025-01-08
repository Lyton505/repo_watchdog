from calendar import c
from configparser import InterpolationMissingOptionError
import time
import requests
from flask import Flask, jsonify
import os

app = Flask(__name__)

REPO_OWNER = os.environ['GITHUB_REPO_OWNER']
REPO_NAME = os.environ['GITHUB_REPO_NAME']
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
CHECK_INTERVAL = 60

last_checked_issue_number = 0

def check_for_new_issues():
    global last_checked_issue_number
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues?state=open&per_page=100"

    headers = {
        "Accept": "application/vnd.github.v3+json",
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        issues = response.json()
        if issues:
            for issue in issues:
                # print(issue["pull_request"])
                # print(issue["number"])
                if ("pull_request" not in issue or issue["pull_request"] is None) and issue["number"] > last_checked_issue_number:
                    print(f"New Issue Found: #{issue['number']} - {issue['title']}")
                    last_checked_issue_number = issue["number"]
                    return issue
            # latest_issue = issues[0]  # Most recent issue
            # if latest_issue["number"] > last_checked_issue_number:
            #     last_checked_issue_number = latest_issue["number"]
            #     return latest_issue
    print("No new issues found.")
    return None


# Background polling function
def poll_issues():
    while True:
        latest_issue = check_for_new_issues()
        if latest_issue:
            print(f"New Issue Found: #{latest_issue['number']} - {latest_issue['title']}")
        time.sleep(CHECK_INTERVAL)  # Wait before polling again


# Flask route to check latest issue manually
@app.route("/check_latest_issue", methods=["GET"])
def check_issue():
    latest_issue = get_latest_issue()
    if latest_issue:
        return jsonify({
            "message": "New issue detected!",
            "issue_number": latest_issue["number"],
            "issue_title": latest_issue["title"],
        }), 200
    else:
        return jsonify({"message": "No new issues."}), 200

if __name__ == "__main__":
    # Start polling in a separate thread
    from threading import Thread
    poller_thread = Thread(target=poll_issues, daemon=True)
    poller_thread.start()

    # Start the Flask server
    app.run(port=5000)