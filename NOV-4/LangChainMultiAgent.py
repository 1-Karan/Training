import os
import requests
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable

# Load environment variables
load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

if not OPENROUTER_API_KEY:
    raise ValueError("API key is missing. Please set OPENROUTER_API_KEY in .env file")


# API Communication Function
def call_llm_api(prompt):
    """Call OpenRouter API and return the response"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:3000",
        "X-Title": "Multi-Agent System"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 800,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers, timeout=60)
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"API Error: {e}")
        return None


# AGENT 1: Research Agent
class ResearchAgent(Runnable):
    """Conducts research and gathers information on a topic using LLM"""

    def __init__(self):
        self.prompt_template = PromptTemplate(
            input_variables=["query"],
            template="""
            You are a research assistant. Conduct comprehensive research on the following topic 
            and provide detailed findings with key points, recent developments, and important information.

            Research Topic: {query}

            Provide a thorough research report with multiple sections covering different aspects of the topic.
            Include specific details, facts, and recent advancements.
            """
        )

    def invoke(self, query, config=None):
        print(f"\n{'=' * 60}")
        print("🔍 RESEARCH AGENT - Gathering Information")
        print(f"{'=' * 60}")
        print(f"Topic: {query}\n")

        # Create research prompt
        prompt = self.prompt_template.format(query=query)
        print("Calling LLM API for research...\n")

        # Get research data from LLM
        research_data = call_llm_api(prompt)

        if not research_data:
            raise Exception("Failed to generate research data from API")

        print("✓ Research completed successfully")
        print(f"Data collected: {len(research_data)} characters\n")

        return research_data


# AGENT 2: Summarizer Agent
class SummarizerAgent(Runnable):
    """Summarizes research data using LLM"""

    def __init__(self):
        self.prompt_template = PromptTemplate(
            input_variables=["research_data"],
            template="""
            You are an expert technical writer. Summarize the following research findings 
            in a clear, concise manner with 3-5 key bullet points.

            Research Data:
            {research_data}

            Provide a well-structured summary that captures the most important points.
            """
        )

    def invoke(self, research_data, config=None):
        print(f"\n{'=' * 60}")
        print("📝 SUMMARIZER AGENT - Creating Summary")
        print(f"{'=' * 60}")

        # Create prompt from template
        prompt = self.prompt_template.format(research_data=research_data)
        print("Calling LLM API for summarization...\n")

        # Get summary from LLM
        summary = call_llm_api(prompt)

        if not summary:
            raise Exception("Failed to generate summary from API")

        print("✓ Summary generated successfully")
        print(f"Summary length: {len(summary)} characters\n")

        return summary


# AGENT 3: Notifier Agent
class NotifierAgent(Runnable):
    """Outputs results to console and saves to file"""

    def invoke(self, summary, config=None):
        print(f"\n{'=' * 60}")
        print("📢 NOTIFIER AGENT - Publishing Results")
        print(f"{'=' * 60}\n")

        # Output to console
        print("=" * 70)
        print("FINAL SUMMARY REPORT")
        print("=" * 70)
        print(summary)
        print("=" * 70)

        # Save to file
        file_path = os.path.join(os.getcwd(), "summary_output.txt")

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("=" * 70 + "\n")
                file.write("RESEARCH SUMMARY REPORT\n")
                file.write("=" * 70 + "\n\n")
                file.write(summary)
                file.write("\n\n" + "=" * 70 + "\n")

            print(f"\n✓ Summary saved to file: {file_path}")
            print(f"✓ File size: {os.path.getsize(file_path)} bytes")

        except Exception as e:
            print(f"✗ Error saving file: {e}")

        return summary


# Multi-Agent Pipeline
def create_multi_agent_pipeline():
    """Create and return the multi-agent pipeline"""
    research_agent = ResearchAgent()
    summarizer_agent = SummarizerAgent()
    notifier_agent = NotifierAgent()

    # Chain agents using pipe operator
    pipeline = research_agent | summarizer_agent | notifier_agent

    return pipeline


# Main Execution
def main():
    print("\n" + "=" * 70)
    print("MULTI-AGENT RESEARCH SYSTEM")
    print("=" * 70)
    print("Pipeline: Research → Summarize → Notify")
    print("=" * 70)

    try:
        # Create pipeline
        pipeline = create_multi_agent_pipeline()

        # Execute pipeline with any query
        query = "Latest advancements in quantum computing"
        result = pipeline.invoke(query)

        print("\n" + "=" * 70)
        print("✓ PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Pipeline Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()