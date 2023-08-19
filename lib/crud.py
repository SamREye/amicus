import json
import time
import os

BASE_DIR = "tmp"

class CRUD:

    def __init__(self, file_name):
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
        self.file_path = f"{BASE_DIR}/{file_name}"

    def is_pr_in_queue(self, pr):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            queue = data['queue']
            for repo in queue:
                for pr_in_queue in repo['pull_requests']:
                    if pr_in_queue['id'] == pr['id']:
                        return True
            return False

    def get_all_needing_posting(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            queue = data['queue']
            needs_posting = []
            for repo in queue:
                for pr in repo['pull_requests']:
                    if pr['review_status'] == 'done' and ('post_status' not in pr or pr['post_status'] != "not_done"):
                        needs_posting.append((repo, pr))
            return needs_posting
    
    def get_all_posted(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            queue = data['queue']
            posted = []
            for repo in queue:
                for pr in repo['pull_requests']:
                    if 'post_status' in pr and pr['post_status'] == "done":
                        posted.append((repo, pr))
            return posted
    
    def mark_as_posted(self, session_id, pr_id):
        with open(self.file_path, 'r+') as file:
            data = json.load(file)
            for session in data["queue"]:
                if session["session_id"] == session_id:
                    for pr in session['pull_requests']:
                        if pr['id'] == pr_id:
                            pr['post_status'] = 'done'
                            file.seek(0)
                            file.truncate()
                            json.dump(data, file)
                            return "Status updated."
            return "Session ID not found."
        
    def get_report(self, session_id, pr_id, testing_file=None):
        if testing_file is not None:
            with open(testing_file, 'r') as file:
                return file.read()
        with open(BASE_DIR + "/" + session_id + "/reports.json", 'r') as file:
            data = json.load(file)
            for report in data["reports"]:
                if report["id"] == pr_id:
                    return report["report"]
            return "PR ID not found."

    def add_pull_requests_to_queue(self, session_id, pull_requests, repo_name, repo_owner):
        session_data = {
            "session_id": session_id,
            "repo_name": repo_name,        # Added repo_name
            "repo_owner": repo_owner,      # Added repo_owner
            "pull_requests": pull_requests,
            "date_added": int(time.time()),
            "status": "not_done"
        }

        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as file:
                json.dump({"queue": []}, file)

        with open(self.file_path, 'r+') as file:
            existing_data = json.load(file)
            existing_data["queue"].append(session_data)
            file.seek(0)
            file.truncate()
            json.dump(existing_data, file)

        return "Pull requests added to queue."


    def update_status(self, session_id, status):
        with open(self.file_path, 'r+') as file:
            data = json.load(file)
            for session in data["queue"]:
                if session["session_id"] == session_id:
                    session['status'] = status
                    file.seek(0)
                    file.truncate()
                    json.dump(data, file)
                    return "Status updated."

            return "Session ID not found."

    def get_data_by_session_id(self, session_id):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            for session in data["queue"]:
                if session["session_id"] == session_id:
                    return session

            return "Session ID not found."

    def delete_by_session_id(self, session_id):
        with open(self.file_path, 'r+') as file:
            data = json.load(file)
            data["queue"] = [session for session in data["queue"] if session["session_id"] != session_id]
            file.seek(0)
            file.truncate()
            json.dump(data, file)
            return "Session deleted."
    
    def get_queue_item(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            queue = data['queue']
            not_done_items = [item for item in queue if item['status'] == 'not_done']
            oldest_not_done = sorted(not_done_items, key=lambda x: x['date_added'])[0] if not_done_items else None
            return oldest_not_done