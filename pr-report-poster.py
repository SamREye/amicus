import os, sys, time, json
from dotenv import load_dotenv
load_dotenv()

from lib.GitHubWrapper import GithubWrapper
from lib.WeaviateWrapper import WeaviateWrapper
import lib.AmicusUtils as utils
from lib.crud import CRUD
import requests

gh = GithubWrapper()
wv = WeaviateWrapper()

def main():
    # Load the queue
    crud = CRUD('queue.json')
    queue = crud.get_all_needing_posting()

    # Treat the reports
    for item in queue:
        repo_data = item[0]
        pr_data = item[1]
        session_id = repo_data['session_id']
        pr_id = pr_data['id']

        # Get the report from amicus.semantic-labs.com/pr/report/markdown/<session_id>
        url = "https://amicus.semantic-labs.com/pr/report/markdown/{}".format(session_id)
        result = requests.get(url)
        document = result.json()["document"]
        # Get the comment from amicus.semantic-labs.com/pr/report/comment/<session_id>
        url = "https://amicus.semantic-labs.com/pr/report/comment/{}".format(session_id)
        result = requests.get(url)
        comment = result.json()["comment"]
        # Get the PR
        pr = gh.get_pull_request("{}/{}".format(repo_data['repo_owner'], repo_data['repo_name']), int(pr_id))
        # Post a comment on the PR
        utils.post_report(pr, comment)
        # Index the report in Weaviate
        utils.index_report(pr, document)
        # Update the queue
        crud.update_post_status(session_id, pr_id, "done")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "--deamon":
            while True:
                main()
                time.sleep(1)
    else:
        main()