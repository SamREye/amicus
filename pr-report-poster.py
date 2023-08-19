import os, sys, time, json

from lib.GitHubWrapper import GithubWrapper
from lib.WeaviateWrapper import WeaviateWrapper
import lib.AmicusUtils as utils
from lib.crud import CRUD

gh = GithubWrapper()
wv = WeaviateWrapper()

crud = CRUD('queue.json')

def main():
    queue = crud.get_all_needing_posting()

    # Treat the reports
    for item in queue:
        repo_data = item[0]
        pr_data = item[1]
        # Get the report
        report = crud.get_report(repo_data['session_id'], pr_data['id'], testing_file="test/samples/good_report.md")
        # Get the PR
        pr = gh.get_pull_request("{}/{}".format(repo_data['repo_owner'], repo_data['repo_name']), int(pr_data['id']))
        # Post a comment on the PR
        utils.post_report(pr, report)
        # Index the report in Weaviate
        # utils.index_report(pr, report)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "--deamon":
            while True:
                main()
                time.sleep(10)
    else:
        main()