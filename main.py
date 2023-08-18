import os, sys
import github

# Get Access Token for GitHub
gh_token = os.environ.get('GITHUB_TOKEN')
openai_apikey = os.environ.get('OPENAI_API_KEY')

# Create GitHub object
gh = github.GitHub(gh_token)

def main():
    pass

if __name__ == '__main__':
    main()