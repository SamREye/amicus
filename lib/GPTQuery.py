from lib.GPTBase import GPTBase

class GPTQuery(GPTBase):
    def __init__(self, prompt='You are a stict python code reviewer reviewing a pull request.'):
        super().__init__(system_prompt=prompt)
        self.prompt = prompt
    
    def summarize_code(self, file_content):
        prompt = f"""
           Provide a detailed summary of what the code does:
            {file_content}
        """
        # print(prompt)
        # print("SENDING PROMPT TO GPT")
        return self.generate_message(prompt)

    def analyze(self, metrics, code_summary, diff_summary, subject):
        prompt = f"""
            Given the following metrics: {metrics}
            Given the summary of the code: {code_summary}
            Given the summary of the diff: {diff_summary}
            Create a clear and concise code review related to {subject}
            """
        # print(prompt)
        # print("SENDING PROMPT TO GPT")
        return self.generate_message(prompt, temperature=0)
    
    def summarize_diff(self, diff, code_summary):
        # print(file_content)
        prompt = f"""
            Given the summary of the code: {code_summary}
            Does the following diff improve the code functionality?
            Does the following diff improve the code quality?
            Does the following diff improve the code readability?
            Does the following diff improve the code performance?
            Does the following diff improve the code maintainability?
            Does the following diff improve the code security?
            Does the following diff improve the code testability?
            Code:
            {diff}"
            Answers must contain line number, code snippet and explanation.
            Think step by step.
        """
        # print(prompt)
        # print("SENDING PROMPT TO GPT")
        return self.generate_message(prompt, "gpt-4")
    
    def get_metrics(self, diff_summary):
        prompt = f"""
            Based on the Code Quality review summary provided, please evaluate and score the following aspects in a JSON format:

            - Functionality improvement
            - Code quality improvement
            - Readability improvement
            - Performance improvement
            - Maintainability improvement
            - Security improvement
            - Testability improvement

            Code Quality review summary: {diff_summary}

            Example JSON response:
            {{
                "functionality": "1",
                "quality": 0,
                "readability": 1,
                "performance": 0,
                "maintainability": 1,
                "security": 0,
                "testability": 0
            }}

            Notes:
            - Score 1 if the aspect was improved, 0 if no change, and -1 if it was worsened.
        

        """
        return self.generate_message(prompt)