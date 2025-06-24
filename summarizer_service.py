import os
import yaml
from langchain_openai import ChatOpenAI
from schema_classes import SummarizeResponse

class SummarizerService:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(openai_api_key=api_key, model="gpt-4o",temperature=0)
        self.prompt_template = self.load_prompt_template("summarize")
        # with open("summarize_prompt.txt", "r", encoding="utf-8") as f:
        #     self.prompt_template = f.read()
        # Prepare the LLM for structured output using the SummarizeResponse schema
        self.structured_llm = self.llm.with_structured_output(SummarizeResponse)

    def load_prompt_template(self,prompt_name):

        prompts_config = {}    
        """Load prompts configuration from YAML file"""
        with open("prompts.yaml", "r", encoding="utf-8") as f:
            prompts_config = yaml.safe_load(f)

        if prompt_name not in prompts_config["prompts"]:
            raise ValueError(f"Prompt '{prompt_name}' not found in configuration")
        
        prompt_path = prompts_config["prompts"][prompt_name]["path"]
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()


    async def asummarize(self, text: str) -> str:
        prompt = self.prompt_template.format(text=text)
        response = await self.structured_llm.ainvoke(prompt)
        return response.summary 