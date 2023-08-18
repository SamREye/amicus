import os, sys
import uuid

from lib.GitHubWrapper import GithubWrapper

openai_apikey = os.environ.get('OPENAI_API_KEY')

# Instatiate a GithubWrapper object
gh = GithubWrapper()

def main():
    # Open a file to get the list of owners
    owners = []
    with open('owners.txt', 'r') as f:
        for line in f.readlines():
            owner = line.strip()
            if owner != '':
                owners.append(owner)
    
    # Get the list of repos for each owner
    repos = []
    for owner in owners:
        for repo in gh.get_repos(owner, visibility="public"):
            repos.append(repo)

    activated_repos = []
    # Check to see if the repo has a AMICUS.md file
    for repo in repos:
        # Get the AMICUS.md file
        try:
            file = repo.get_contents("AMICUS.json")
            activated_repos.append({
                "repo": repo,
                "amicus_cfg": file.decoded_content.decode("utf-8")
            })
        except:
            # print("No AMICUS.md file found")
            continue
    
    # Get all pull requests for each repo
    prs = []
    for repo in activated_repos:
        # Get all pull requests
        for pr in repo["repo"].get_pulls():
            # Get the pull request's hash
            pr_hash = pr.head.sha
            prs.append({
                "hash": pr_hash,
                "uuid": uuid.uuid4(),
            })
    
    print(prs)

if __name__ == '__main__':
    main()