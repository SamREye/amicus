import os, sys

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
        for repo in gh.get_repos(owner):
            repos.append(repo)
    print(repos)

if __name__ == '__main__':
    main()