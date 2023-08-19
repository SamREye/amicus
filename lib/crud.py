import json
import time
import os


BASE_DIR = "tmp"
import uuid

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
    def _load_data(self):
        with open(self.file_path, 'a+') as file:
            file.seek(0)
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = {"queue": []}
        return data

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

    def get_oldest_review_not_done(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            queue = data['queue']

            not_done_reviews = [session for session in queue if any(pull_request['review_status'] == 'not_done' for pull_request in session["pull_requests"])]
            
            oldest_not_done_review = sorted(not_done_reviews, key=lambda x: x['date_added'])[0] if not_done_reviews else None
            return oldest_not_done_review

    def get_oldest_post_not_posted(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            queue = data['queue']

            not_posted_items = [session for session in queue if any(pull_request['post_status'] == 'not_posted' for pull_request in session["pull_requests"])]
            
            oldest_not_posted = sorted(not_posted_items, key=lambda x: x['date_added'])[0] if not_posted_items else None
            return oldest_not_posted

    def get_all_oldest_posts_not_posted(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            queue = data['queue']
            not_posted_sessions = [session for session in queue if any(pull_request['post_status'] == 'not_posted' for pull_request in session["pull_requests"])]
            sorted_sessions = sorted(not_posted_sessions, key=lambda x: x['date_added'])
            return sorted_sessions

    def get_all_oldest_reviews_not_done(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
            queue = data['queue']
            not_done_reviews = [session for session in queue if any(pull_request['review_status'] == 'not_done' for pull_request in session["pull_requests"])]
            sorted_sessions = sorted(not_done_reviews, key=lambda x: x['date_added'])
            return sorted_sessions
