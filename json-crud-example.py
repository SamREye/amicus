import uuid
from lib.crud import CRUD

DATABASE_NAME = "queue.json"
db = CRUD(DATABASE_NAME)

session_id = str(uuid.uuid4())


# 1. Add a new pull request
repo_name = "amicus"
repo_owner = "SamREye"
last_commit_hash = "abc12345"
pull_request_id = "1"
response = db.add_pull_request(session_id, pull_request_id, repo_name, repo_owner, last_commit_hash)
print(response)

# 2. Update the review status for a specific session and pull request
# response = db.update_review_status(session_id, pull_request_id, "in_progress")
# print(response)

# 3. Update the post status for the same session and pull request
response = db.update_post_status(session_id, pull_request_id, "posted")
print(response)

# 4. Retrieve a specific session by session_id
session_data = db.get_data_by_session_id(session_id)
print(session_data)

# # 5. Delete a session by its session_id
# response = db.delete_by_session_id(session_id_example)
# print(response)

# 6. Get the oldest 'not_done' session
oldest_not_done = db.get_oldest_not_done()
print(oldest_not_done)


