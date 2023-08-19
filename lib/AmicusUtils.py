from lib.GitHubWrapper import GithubWrapper
from lib.WeaviateWrapper import WeaviateWrapper

gh = GithubWrapper()
wv = WeaviateWrapper()

REVIEWED_LABEL = "amicus:reviewed"

def get_owners():
    # Open the owners file to get the list of owners
    owners = []
    with open('owners.txt', 'r') as f:
        for line in f.readlines():
            owner = line.strip()
            if owner != '':
                owners.append(owner)
    return owners

def get_repos(owners):
    repos = []
    for owner in owners:
        for repo in gh.get_repos(owner, visibility="public"):
            repos.append(repo)
    return repos

def filter_repos_to_activated(repos):
    activated_repos = []
    for repo in repos:
        # Get the AMICUS file
        try:
            file = repo.get_contents("AMICUS.json")
            activated_repos.append({
                "repo": repo,
                "amicus_cfg": file.decoded_content.decode("utf-8")
            })
        except:
            # print("No AMICUS file found")
            continue
    return activated_repos

def get_pull_requests(repos):
    prs = []
    for repo in repos:
        # Get all pull requests
        for pr in repo["repo"].get_pulls(state="open"):
            # Check to see if the PR has a REVIEWED label--if so, ignore it
            if REVIEWED_LABEL not in [label.name for label in pr.get_labels()]:
                # Get the pull request's hash
                pr_hash = pr.head.sha
                prs.append({
                    "repo": repo["repo"],
                    "pr": pr,
                })
    return prs

def post_report(pr, report):
    print("Posting report to PR #{}".format(pr.number))
    print(report)
    pr.create_issue_comment(report)
    pr.add_to_labels(REVIEWED_LABEL)

def _get_class_name(pr):
    return "Report_{}".format(pr.head.sha[-6:])

def index_report(pr, report):
    wv.insert_md_document(_get_class_name(pr), report)
