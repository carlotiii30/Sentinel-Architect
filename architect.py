from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()


class GeneratedFile(BaseModel):
    filename: str = Field(
        description="The suggested filename, e.g., 'docker-compose.yml' or 'main.tf'"
    )
    content: str = Field(description="The complete and valid source code for the file")


class ArchitectureResponse(BaseModel):
    files: List[GeneratedFile] = Field(
        description="List of infrastructure files generated"
    )
    security_summary: str = Field(
        description="Executive summary of the security posture"
    )
    validation_checklist: List[str] = Field(
        description="5 critical security checks to verify this deployment"
    )


class SentinelArchitect:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        self.structured_llm = self.llm.with_structured_output(ArchitectureResponse)

    def generate_infrastructure(self, prompt: str):
        system_template = """
        You are a Senior Cloud Security Architect (ISC2 Certified). 
        Your mission is to generate secure Infrastructure as Code (IaC) based on natural language requirements.

        RULES:
        1. Apply LEAST PRIVILEGE and DEFENSE IN DEPTH.
        2. Include #Comments within the code explaining the SECURITY RATIONALE.
        3. Ensure all generated code is production-ready and follows security hardening best practices.
        """

        full_prompt = f"{system_template}\n\nUser Requirement: {prompt}"
        return self.structured_llm.invoke(full_prompt)
