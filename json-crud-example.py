import uuid
from lib.crud import CRUD

DATABASE_NAME = "queue.json"
crud = CRUD(DATABASE_NAME)

session_id = str(uuid.uuid4())

# I need the pull request ID from the repo

# I need the owner + repo name
repo_owner = "SamREye"
repo_name = "amicus"

pull_requests = [{"id": "1"}, {"id": "2"}]

# write to json file
crud.add_pull_requests_to_queue(session_id, pull_requests, repo_name, repo_owner)

# update status
crud.update_status(session_id, "done")

# get data by session id
print(crud.get_data_by_session_id(session_id))

# delete by session id
# crud.delete_by_session_id(session_id)

