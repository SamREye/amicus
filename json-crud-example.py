import uuid
from lib.crud import CRUD

database_name = "queue.json"

crud = CRUD(database_name)

session_id = str(uuid.uuid4())

pull_requests = [{"hash": "39ee68c87bb0018c5ca31c00b1ecf1d5f688faec"}]

crud.add_pull_requests_to_queue(session_id, pull_requests)
crud.update_status(session_id, "done")
print(crud.get_data_by_session_id(session_id))
# crud.delete_by_session_id(session_id)