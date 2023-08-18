import os, sys
import github

class GithubWrapper:
    def __init__(self):
        self.github = github.Github(os.environ.get("GITHUB_API_KEY"))

    def get_repo(self, repo_name):
        print(f"Fetching repository {repo_name}...")
        return self.github.get_repo(repo_name)
    
    def get_repos(self, name, visibility="public"):
        print(f"Fetching repositories for {name}...")
        try:
            search = self.github.search_users(name)
            if name.lower() == search[0].login.lower():
                return self.github.get_user(name).get_repos(type=visibility)
            return self.github.get_organization(name).get_repos(type=visibility)
        except:
            sys.stderr.write("No such user or org: {}".format(name))
            return []
    
    def get_pull_request_by_hash(self, repo, hash):
        print(f"Fetching pull request {hash}...")
        repo = self.get_repo(repo)
        return repo.get_pull(hash)