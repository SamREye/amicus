import sys

class GitHubHelper:

    VISIBILITY_PUBLIC = "public"
    # Add more constants if needed

    def _print_and_return(self, message: str, func, *args, **kwargs):
        """Helper function to print a message before executing a function."""
        print(message)
        return func(*args, **kwargs)

    def get_repo(self, repo_name: str):
        return self._print_and_return(
            f"Fetching repository {repo_name}...", 
            self.github.get_repo, 
            repo_name
        )

    def get_repos(self, name: str, visibility: str = VISIBILITY_PUBLIC):
        try:
            search = self.github.search_users(name)
            is_user = name.lower() == search[0].login.lower()

            if is_user:
                repos = self.github.get_user(name).get_repos(type=visibility)
            else:
                repos = self.github.get_organization(name).get_repos(type=visibility)

            return self._print_and_return(
                f"Fetching repositories for {name}...", 
                lambda: repos
            )
        except IndexError:  # If search result is empty
            sys.stderr.write(f"No such user or org: {name}")
            return []
        except Exception as e:  # To catch other exceptions and log them
            sys.stderr.write(str(e))
            return []

    def get_pull_request(self, repo: str, id: int):
        repo_obj = self.get_repo(repo)
        return self._print_and_return(
            f"Fetching pull request {id}...", 
            repo_obj.get_pull, 
            id
        )
