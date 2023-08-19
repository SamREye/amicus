from lib.GPTBase import GPTBase
import json
class GPTReportChat(GPTBase):
    def __init__(self, prompt='You are a helpful assistant helping coders understand their code review report.'):
        super().__init__(system_prompt=prompt)
        self.prompt = prompt
    
    def reply_to_comment(self, question, report_chunks, sender):
        chunks = "\n".join(report_chunks)
        prompt = f"""
            Given relevant code review report chunks in REPORT, answer the collaborator's question in QUESTION.

            [REPORT]{chunks}[/REPORT]

            Example:
            {sender}: What is the code quality score?
            AI: @{sender} The code quality score is 0.8.
            
            {sender}: {question}
            AI:
        """
        # print(prompt)
        # print("SENDING PROMPT TO GPT")
        return self.generate_message(prompt)
