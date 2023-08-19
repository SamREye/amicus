import os, sys, time, json

from lib.GitHubWrapper import GithubWrapper
from lib.WeaviateWrapper import WeaviateWrapper
import lib.AmicusUtils as utils
from lib.crud import CRUD

from Analyzer import analyze

gh = GithubWrapper()
wv = WeaviateWrapper()
crud = CRUD('queue.json')

def main():
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
        crud.add_pull_requests_to_queue(pr)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "--deamon":
            while True:
                main()
                time.sleep(10)
    else:
        main()