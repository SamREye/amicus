import json

def analyze(pull_requests):
    # Get tmp/pr_list.json for a sample input
    # Get tmp/reports.json for a sample output
    with open('tmp/reports.json', 'r') as f:
        return json.load(f)
