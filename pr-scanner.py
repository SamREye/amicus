import os, sys, time, json
from dotenv import load_dotenv
load_dotenv()

from lib.GitHubWrapper import GithubWrapper
from lib.WeaviateWrapper import WeaviateWrapper
import lib.AmicusUtils as utils
from lib.crud import CRUD

gh = GithubWrapper()
wv = WeaviateWrapper()

def main():
    # Load the queue
    crud = CRUD('queue.json')
    # Get the list of owners
    owners = utils.get_owners()
    # Get the list of repos for each owner
    all_repos = utils.get_repos(owners)
    # Filter the list of activated repos
    activated_repos = utils.filter_repos_to_activated(all_repos)
    # Get all pull requests for each repo
    prs = utils.get_pull_requests(activated_repos)

    # Add prs to the queue
    for pr in prs:
        if crud.is_pr_in_queue(pr):
            continue
        crud.add_pull_request(pr)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "--deamon":
            while True:
                main()
                time.sleep(1)
    else:
        main()