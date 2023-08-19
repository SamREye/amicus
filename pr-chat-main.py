import os, sys, time, json
from dotenv import load_dotenv
load_dotenv()

from lib.GitHubWrapper import GithubWrapper
from lib.WeaviateWrapper import WeaviateWrapper
import lib.AmicusUtils as utils
from lib.crud import CRUD
from lib.GPTReportChat import GPTReportChat

gh = GithubWrapper()
wv = WeaviateWrapper()
chat = GPTReportChat()

crud = CRUD('queue.json')

CALLOUT = '@semantic-labs'

def main():
    items = crud.get_all_posted()
    print(items)
    for item in items:
        # Split up tuple into repo and pr
        repo_data = item[0]
        pr_data = item[1]
        pr = gh.get_pull_request("{}/{}".format(repo_data['repo_owner'], repo_data['repo_name']), int(pr_data['id']))

        # Read last comment
        comments = pr.get_issue_comments()
        last_comment = comments.reversed.get_page(0)[-1]
        if last_comment.body.lower().strip().startswith(CALLOUT.lower()):
            print("Comment received: {}".format(last_comment.body))
            chunks = utils.get_query_vector_chunks(pr, last_comment.body)
            reply = chat.reply_to_comment(last_comment.body, chunks, last_comment.user.login)
            print("Replying: {}".format(reply))
            pr.create_issue_comment(reply)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == "--deamon":
            while True:
                main()
                time.sleep(10)
    else:
        main()