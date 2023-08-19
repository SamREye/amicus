import json
import time
import os
import uuid

class CRUD:

    def __init__(self, file_name):
        directory_path = "tmp"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        self.file_path = f"{directory_path}/{file_name}"

    def _load_data(self):
        with open(self.file_path, 'a+') as file:
            file.seek(0)
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {"queue": []}
        return data

    def add_pull_request(self, session_id, pull_request_id, repo_name, repo_owner, last_commit_hash):
        session_data = {
            "session_id": session_id,
            "repo_name": repo_name,
            "repo_owner": repo_owner,
            "pull_requests": [{
                "review_status": "not_done",
                "post_status": "not_posted",
                "id": pull_request_id,
                "last_commit_hash": last_commit_hash
            }],
            "date_added": int(time.time())
        }

        with open(self.file_path, 'a+') as file:
            file.seek(0)
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {"queue": []}

            existing_data["queue"].append(session_data)
            file.seek(0)
            file.truncate()
            json.dump(existing_data, file)

        return "Pull request added to queue."

    def update_review_status(self, session_id, pull_request_id, review_status):
        data = self._load_data()

        for session in data["queue"]:
            if session["session_id"] == session_id:
                for pull_request in session["pull_requests"]:
                    if pull_request["id"] == pull_request_id:
                        pull_request["review_status"] = review_status
                        with open(self.file_path, 'w') as file:
                            json.dump(data, file)
                        return "Review status updated."

        return "Session ID or Pull Request ID not found."

    def update_post_status(self, session_id, pull_request_id, post_status):
        data = self._load_data()

        for session in data["queue"]:
            if session["session_id"] == session_id:
                for pull_request in session["pull_requests"]:
                    if pull_request["id"] == pull_request_id:
                        pull_request["post_status"] = post_status
                        with open(self.file_path, 'w') as file:
                            json.dump(data, file)
                        return "Post status updated."

        return "Session ID or Pull Request ID not found."

    def get_data_by_session_id(self, session_id):
        data = self._load_data()
        for session in data["queue"]:
            if session["session_id"] == session_id:
                return session

        return "Session ID not found."

    def delete_by_session_id(self, session_id):
        data = self._load_data()
        data["queue"] = [session for session in data["queue"] if session["session_id"] != session_id]

        with open(self.file_path, 'w') as file:
            json.dump(data, file)

        return "Session deleted."

    def get_oldest_not_done(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            queue = data['queue']
            
            not_done_sessions = [session for session in queue if any(pull_request.get('review_status') == 'not_done' for pull_request in session.get("pull_requests", []))]
            
            if not not_done_sessions:
                return None
            
            oldest_not_done = sorted(not_done_sessions, key=lambda x: x['date_added'])[0]
            return oldest_not_done

