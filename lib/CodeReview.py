from lib.crud import CRUD
from lib.GitHubWrapper import GithubWrapper
from lib.GPTQuery import GPTQuery
from github import GithubException
import json
import time
import os
import requests

class CodeReview:
    def __init__(self):
        self.database_name = "queue.json"
        self.github_wrapper = GithubWrapper()
        self.gpt_query = GPTQuery()
        self.results = []

    def get_repo_details(self, queue_item):
        repo_name = queue_item[0]['repo_name']
        repo_owner = queue_item[0]['repo_owner']
        repo_name_and_owner = repo_owner + "/" + repo_name
        return self.github_wrapper.get_repo(repo_name_and_owner)

    def process_pull_request(self, pull_request, repo):
        files_data = []
        # if not pull_request.mergeable:
        #     return files_data

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

        code_summary = self.gpt_query.summarize_code(original_content)
        diff_json = self.gpt_query.summarize_diff(parsed_diff, code_summary)
        metrics = self.gpt_query.get_metrics(diff_json)

        REPORT_TYPE = "code quality"
        result = self.gpt_query.analyze(
            metrics, code_summary, diff_json, REPORT_TYPE
        )

        return {
            "filename": file_name,
            "results": {
                "code_summary": code_summary,
                "diff_json": diff_json,
                "metrics": metrics,
                "analysis_result": result
            }
        }

    def transform_json(self, original_json, results_dict):
        new_entry = {
            "session_id": original_json["session_id"],
            "repo_name": original_json["repo_name"],
            "repo_owner": original_json["repo_owner"],
            "latest_sha_commit": original_json["pull_requests"][0]["last_commit_hash"],
            "date_added": int(time.time()),  # Updating date_added to current timestamp
            "results": results_dict  # Add the results_dict
        }
        return {"reviews": [new_entry]}

    def get_file_content_from_commit(self, repo, file_name, base_commit_sha):
        try:
            original_content = repo.get_contents(file_name, ref=base_commit_sha).decoded_content.decode("utf-8")
            return original_content
        except GithubException as e:
            return None

    def execute(self):
        queue_items = CRUD(self.database_name).get_all_oldest_reviews_not_done()
        # print(queue_item)



        #loop through queue_item
        for queue_item in queue_items:
            # repo_info = self.get_repo_details(queue_item)
            repo_name = queue_item['repo_name']
            repo_owner = queue_item['repo_owner']
            repo_name_and_owner = repo_owner + "/" + repo_name
            repo = self.github_wrapper.get_repo(repo_name_and_owner)
            self.results = []
            for pull_request in queue_item['pull_requests']:
                print("doing PR id: " + str(pull_request['id']))
                pull_request_id = int(pull_request['id'])
                pull_request = repo.get_pull(pull_request_id)
                files_data = self.process_pull_request(pull_request, repo)

                # Create a new dictionary for this pull request's data
                pull_request_data = {
                    "pull_request_id": pull_request_id,
                    "data": files_data
                }
                
                # Append the new data to self.results
                self.results.append(pull_request_data)

            json_data = self.transform_json(queue_item, self.results)

            extracted_data = [{"filename": item["filename"], "analysis_result": item["results"]["analysis_result"]} for item in json_data["reviews"][0]["results"][0]["data"]]

            long_summary = self.gpt_query.summarize_entire_pr(extracted_data)
            short_summary = self.gpt_query.summary_shortener(long_summary)

            json_data["reviews"][0]["results"][0]["long_summary"] = long_summary
            json_data["reviews"][0]["results"][0]["executive_summary"] = short_summary

            self.update_results_file(json_data["reviews"][0])

            url = "https://amicus.semantic-labs.com/pr/report/add"
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=json_data["reviews"][0], headers=headers)
            print(response)


        return json_data
    #
    def add_review(self, existing_json, new_review):
        """
        Add a new review to the reviews array in the existing JSON structure.
        
        Parameters:
        - existing_json (dict): The existing JSON structure.
        - new_review (dict): The new review to be added.

        Returns:
        - dict: The updated JSON structure.
        """
        existing_json['reviews'].append(new_review)
        return existing_json

    def update_results_file(self, new_review, file_path="data/reviews.json"):
        """
        Read the JSON structure from a file, append a new review, and save it back to the file.

        Parameters:
        - new_review (dict): The new review to be added.
        - file_path (str, optional): Path to the JSON file. Defaults to "data/results.json".
        """
        with open(file_path, 'r') as file:
            existing_json = json.load(file)

        updated_json = self.add_review(existing_json, new_review)

        with open(file_path, 'w') as file:
            json.dump(updated_json, file, indent=4)




    # def save_results_to_json(self, results):
    #     with open("data/reviews.json", "w") as json_file:
    #         json.dump(results, json_file, indent=4)

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
