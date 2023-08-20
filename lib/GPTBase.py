from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

load_dotenv()

class GPTBase:
    def __init__(self, system_prompt, model_name="gpt-3.5-turbo-16k", temperature=0):
        self.default_model_name = model_name
        self.default_temperature = temperature
        self.chat = self._initialize_chat(self.default_model_name, self.default_temperature)
        self.system_message = SystemMessage(content=system_prompt)

    def _initialize_chat(self, model_name, temperature):
        """Initialize a chat with given model name and temperature."""
        return ChatOpenAI(model_name=model_name, temperature=temperature)

    def _get_chat_config(self, model_name=None, temperature=None):
        """Return the effective model and temperature settings."""
        effective_model_name = model_name or self.default_model_name
        effective_temperature = temperature if temperature is not None else self.default_temperature
        return effective_model_name, effective_temperature

    def generate_message(self, human_message, model_name=None, temperature=None):
        """Generates a system response message given a human message."""
        effective_model_name, effective_temperature = self._get_chat_config(model_name, temperature)
        
        if effective_model_name != self.default_model_name or effective_temperature != self.default_temperature:
            chat_instance = self._initialize_chat(effective_model_name, effective_temperature)
        else:
            chat_instance = self.chat

        messages = [self.system_message, HumanMessage(content=human_message)]
        result = chat_instance(messages)

        return result.content
