from lib.crud import CRUD
from lib.GitHubWrapper import GithubWrapper
from lib.GPTQuery import GPTQuery
from github import GithubException
class CodeReview:
    def __init__(self):
        self.database_name = "queue.json"
        self.github_wrapper = GithubWrapper()
        self.gpt_query = GPTQuery()
        self.results = {}  # Dictionary to store GPT results

    def get_repo_details(self, queue_item):
        repo_name = queue_item['repo_name']
        repo_owner = queue_item['repo_owner']
        repo_name_and_owner = repo_owner + "/" + repo_name
        return self.github_wrapper.get_repo(repo_name_and_owner)

    def process_pull_request(self, pull_request, repo):
        files_data = []
        if not pull_request.mergeable:
            return files_data

        files = pull_request.get_files()
        for file in files:
            data = self.process_file(file, repo, pull_request)
            if data:  # If data exists, append it
                files_data.append(data)

        return files_data

    def process_file(self, file, repo, pull_request):
        file_name = file.filename
        file_diff = file.patch
        base_commit_sha = pull_request.base.sha
        original_content = self.get_file_content_from_commit(repo, file_name, base_commit_sha)
        parsed_diff = self.convert_diff_to_json(file_diff, original_content)

        code_summary = "a" #self.gpt_query.summarize_code(original_content)
        diff_json = "b" #self.gpt_query.summarize_diff(parsed_diff, code_summary)
        metrics = "c" #self.gpt_query.get_metrics(diff_json)

        REPORT_TYPE = "code quality"
        result = "d" #self.gpt_query.analyze_file(
        #     metrics, code_summary, diff_json, REPORT_TYPE
        # )

        return {
            "filename": file_name,
            "code_summary": code_summary,
            "diff_json": diff_json,
            "metrics": metrics,
            "analysis_result": result
        }

    def get_file_content_from_commit(self, repo, file_name, base_commit_sha):
        try:
            original_content = repo.get_contents(file_name, ref=base_commit_sha).decoded_content.decode("utf-8")
            return original_content
        except GithubException as e:
            return None

    def execute(self):
        queue_item = CRUD(self.database_name).get_oldest_review_not_done()
        print(queue_item)

        repo = self.get_repo_details(queue_item)

        for pull_request in queue_item['pull_requests']:
            pull_request_id = int(pull_request['id'])
            pull_request = repo.get_pull(pull_request_id)
            files_data = self.process_pull_request(pull_request, repo)

            # Update results with pull_request_id as key
            self.results[pull_request_id] = files_data

        return self.results
    
    def convert_diff_to_json(self, diff_text, original_code):
        file_changes = {
            "file_name": None,  # You can extract this if available in the diff or elsewhere
            "original_code": original_code,
            "changes": [],
        }

        lines = diff_text.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("@@"):
                continue

            action = None
            if line.startswith("-"):
                action = "removed"
            elif line.startswith("+"):
                action = "added"

            if action:
                change = {
                    "action": action,
                    "line_number": i,  # Assuming the diff starts at line 0; adjust as needed
                    "content": line[1:].strip(),
                }
                file_changes["changes"].append(change)

        return file_changes
