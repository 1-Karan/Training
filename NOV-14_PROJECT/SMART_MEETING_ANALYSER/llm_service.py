import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import Docx2txtLoader
from io import BytesIO

# Load environment variables
load_dotenv()

# Load OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Initialize model
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=["meeting_text"],
    template="""
You are a highly intelligent and organized **AI Meeting Assistant** whose job is to analyze corporate meeting transcripts and produce well-structured professional documentation.  
Your output will be shared with multiple teams, so ensure it is **clear, polished, and formatted for direct email use.**

---

### 🔍 Your Tasks:
Carefully read and interpret the meeting transcript below, and provide the following outputs in clearly separated sections using Markdown formatting:

---

### 🧾 1. Concise Meeting Summary
Provide a short, executive-level summary (4–6 bullet points) highlighting:
- The key objectives discussed
- Major decisions taken
- High-level outcomes or agreements
- Any strategic directions or next steps

Keep it factual, clear, and non-redundant.

---

### 📝 2. Detailed Minutes of Meeting (MOM)
Create a structured list of points capturing :
- Agenda items discussed
- Key participants (if mentioned)
- Discussion highlights and reasoning
- Important takeaways and conclusions
- Decisions finalized

Use a clean bullet only for above mention points, making it easy for readers to skim.

---

### ✅ 3. Action Items and Responsibilities
Extract all **specific tasks or commitments**, even if implied.
and give them in bullet points and not in table format.  
For each, include:
- **Task Description** — What needs to be done  
- **Assigned To** — The responsible person or team  
- **Deadline** — If mentioned (otherwise write “Not specified”)  in this format format '%b %d for eg :Nov 14,Nov 22... 

---

Meeting Transcript:
{meeting_text}
"""
)

# def analyze_meeting_docx(file):
#     """
#     Accepts:
#     - FastAPI UploadFile (file.filename, file.file.read())
#     - Streamlit UploadedFile (file.name, file.read())
#     """
#     # Determine filename
#     filename = getattr(file, "filename", None) or getattr(file, "name", "temp_meeting.docx")
#     temp_path = f"temp_{filename}"
#
#     # Save uploaded file temporarily
#     with open(temp_path, "wb") as f:
#         f.write(file.read() if hasattr(file, "read") else file.file.read())
#     # content = await file.read()
#     # with open("temp.docx", "wb") as f:
#     #     f.write(content)
#
#     # Extract text
#     loader = Docx2txtLoader(temp_path)
#     docs = loader.load()
#     os.remove(temp_path)
#
#     meeting_text = docs[0].page_content.strip()
#
#     # Format prompt
#     prompt = prompt_template.format(meeting_text=meeting_text)
#
#     # Invoke LLM
#     result = llm.invoke(prompt)
#
#     return {
#         "status": "success",
#         "content": result.content
#     }

def analyze_meeting_docx(file_bytes: bytes, filename: str = "meeting.docx"):
    """
    Accepts:
    - Raw bytes from FastAPI UploadFile
    - Optional filename for temporary saving
    """

    temp_path = f"temp_{filename}"

    # Save uploaded file temporarily
    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    # Extract text
    loader = Docx2txtLoader(temp_path)
    docs = loader.load()
    os.remove(temp_path)

    meeting_text = docs[0].page_content.strip()

    # Format prompt
    prompt = prompt_template.format(meeting_text=meeting_text)

    # Invoke LLM
    result = llm.invoke(prompt)

    return {
        "status": "success",
        "content": result.content
    }

def enhance_email_body(meeting_body: str) -> str:
    """
    Enhances the plain meeting summary email body using the LLM.
    Adds a professional greeting, context line, and closing.
    Keeps original content intact.
    """
    enhancement_prompt = f"""
    You are an AI email assistant helping finalize a professional meeting summary email.

    Please rewrite the following meeting summary body to include:
    - A friendly professional greeting such as "Hi Team etc,"
    - A connecting phrase like "As discussed in the meeting,"
    - Keep the original meeting body exactly as is (do not remove or change any information) but make it plain text not markdown text so avid showing ##,** etc please avoid that just plain text 
    - Add a polite closing with "Best regards," and a line "Sent via AI Meeting Assistant 🤖"

    Keep tone: formal yet friendly.
    Return only the enhanced body text (no explanations, no markdown).

    ---
    Meeting Summary Body:
    {meeting_body}
    ---
    """

    result = llm.invoke(enhancement_prompt)
    return result.content.strip()

