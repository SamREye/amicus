import os, sys, time

from lib.GitHubWrapper import GithubWrapper
from lib.WeaviateWrapper import WeaviateWrapper
from lib.crud import CRUD

gh = GithubWrapper()
wv = WeaviateWrapper()

crud = CRUD('queue.json')

CALLOUT = '@semantic-labs'

def main():
    items = crud.get_all_posted()
    print(items)
    for item in items:
        # Split up tuple into repo and pr
        repo_data = item[0]
        pr_data = item[1]
        pr = gh.get_pull_request("{}/{}".format(repo_data['repo_owner'], repo_data['repo_name']), int(pr_data['id']))

        # Read last comment
        comments = pr.get_issue_comments()
        last_comment = comments.reversed.get_page(0)[-1].body
        if last_comment.lower().strip().startswith(CALLOUT.lower()):
            # TODO: Reply to comment
            print("Must reply")

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "--deamon":
            while True:
                main()
                time.sleep(10)
    else:
        main()