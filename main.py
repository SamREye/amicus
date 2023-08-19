import os, sys
import uuid, json

from lib.GitHubWrapper import GithubWrapper

from Analyzer import analyze

openai_apikey = os.environ.get('OPENAI_API_KEY')

# Instatiate a GithubWrapper object
gh = GithubWrapper()

REVIEW_LABEL = "amicus:reviewed"

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
    pr_objs = {}
    pr_hashes = []
    for repo in activated_repos:
        # Get all pull requests
        for pr in repo["repo"].get_pulls():
            # Check to see if the PR has a REVIEWED label--if so, ignore it
            if REVIEW_LABEL not in [label.name for label in pr.get_labels()]:
                # Get the pull request's hash
                pr_hash = pr.head.sha
                pr_hashes.append({
                    "repo": repo["repo"].full_name,
                    "hash": pr_hash,
                })
                pr_objs[pr_hash] = pr
    
    # Write the hashes to a file in JSON
    hash_list_file = 'tmp/pr_list.json'
    with open(hash_list_file, 'w') as f:
        f.write(json.dumps(pr_hashes))
    
    # Run the analyzer
    reports_file = analyze(hash_list_file)

    # Extract the JSON reports file
    reports = {}
    with open(reports_file, 'r') as f:
        reports = json.load(f)

    for report in reports["reports"]:
        if report["hash"] not in pr_objs:
            continue
        pr = pr_objs[report["hash"]]
        # Post a comment on the PR
        pr.create_issue_comment(report["report"])
        # Attach a label to the PR
        pr.add_to_labels(REVIEW_LABEL)

if __name__ == '__main__':
    main()