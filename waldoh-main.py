from lib.CodeReview import CodeReview
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    code_review = CodeReview()
    results = code_review.execute()
    print(results)

    

