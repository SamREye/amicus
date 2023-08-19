import json
import time
import os
class CRUD:

    def __init__(self, file_name):
        directory_path = "tmp"
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        self.file_path = f"{directory_path}/{file_name}"


    def add_pull_requests_to_queue(self, session_id, pull_requests):
        session_data = {
            "session_id": session_id,
            "pull_requests": pull_requests,
            "date_added": int(time.time()),
            "status": "not_done"
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