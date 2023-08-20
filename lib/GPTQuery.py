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
        return self.generate_message(prompt)

    def summarize_generic(self, file_content):
        prompt = f"""
           Provide a detailed summary of the following text:
            {file_content}
        """
        return self.generate_message(prompt)
    
    def analyze(self, metrics, code_summary, diff_summary, subject):
        prompt = f"""
            Given the following metrics: {metrics}
            Given the summary of the code: {code_summary}
            Given the summary of the diff: {diff_summary}
            Create a clear and concise code review related to {subject}
            """
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
        return self.generate_message(prompt, "gpt-4")
    
    def summarize_entire_pr(self, pull_request):
        prompt = f"""
            Summarize each filename's summary into 1 large summary that will help the developer understand the entire pull request.
            {pull_request}
        """
        return self.generate_message(prompt)

    def summary_shortener(self, long_summary):
        prompt = f"""
            Start by saying that you've reviewed the code and then summarize in 3 sentences maximum the actionable items that the developer should take to improve the code.
            {long_summary}
        """
        return self.generate_message(prompt)
    
    def coherence_and_appropriateness_check(self, file_diff, readme_summary, coc_summary):
        if readme_summary and coc_summary:
            prompt = f"""
                Given the content of the README, the Code of Conduct, and the provided file differences, please evaluate and score the following aspects in a JSON format, and provide a brief explanation for each score:

                - Coherence of the changes with the goals and purpose described in the README
                - Appropriateness of the changes in relation to the Code of Conduct

                README: {readme_summary}
                Code of Conduct: {coc_summary}
                File differences: {file_diff}

                Example JSON response:
                {{
                    "coherence": {{
                        "score": 1,
                        "explanation": "The changes are in line with the goals described in the README."
                    }},
                    "appropriateness": {{
                        "score": -1,
                        "explanation": "The changes seem to violate one of the principles because of <reason>."
                    }}
                }}

                Notes:
                - Score 1 if the changes align positively, 0 if there's no change or neutral alignment, and -1 if they misalign or violate the respective document.


            """

        elif readme_summary:
            prompt = f"""
                    Given the content of the README and the provided file differences, please evaluate and score the coherence of the changes with the goals and purpose described in the README in a JSON format, and provide a brief explanation for each score:

                    README: {readme_summary}
                    File differences: {file_diff}

                    Example JSON response:
                    {{
                        "coherence": {{
                            "score": 1,
                            "explanation": "The changes are in line with the goals described in the README."
                        }},
                    }}

                    Notes:
                    - Score 1 if the changes align positively with the goals and purpose of the README, 0 if there's no change or neutral alignment, and -1 if they misalign with the README's intent.

                """

        elif coc_summary:
            prompt = f"""
                Given the content of the Code of Conduct and the provided file differences, please evaluate and score the appropriateness of the changes in relation to the Code of Conduct in a JSON format, and provide a brief explanation for each score:

                Code of Conduct: {coc_summary}
                File differences: {file_diff}

                Example JSON response:
                {{
                    "appropriateness": {{
                        "score": -1,
                        "explanation": "The changes seem to violate one of the principles because of <reason>."
                    }}
                }}

                Notes:
                - Score 1 if the changes align positively with the Code of Conduct, 0 if there's no change or neutral alignment, and -1 if they misalign or violate the Code of Conduct.

            """

        else:
            return None

        return self.generate_message(prompt)
    
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