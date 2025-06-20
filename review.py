import os
from langchain_openai import AzureChatOpenAI
# from dotenv import load_dotenv
# load_dotenv()
client = AzureChatOpenAI(
    model="gpt-4o",
    deployment_name="gpt-4o",
    openai_api_version="2025-01-01-preview",
    azure_endpoint="https://pstestopenaidply-jeedmlivt7amc.openai.azure.com",
    openai_api_key="8a118427b9c442e1b57761b8d89def5b",
    temperature=0.0,
)
def analyze_python_file(file_path: str, review_file: str = "review.txt") -> None:
    """
    Reads a .py file, sends it to GPT for review, and appends the review to a common review.txt file.
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code_snippet = f.read()

    # Messages for LLM
    messages = [
        {"role": "system", "content": "You are expert in code reviewing."},
        {
            "role": "user",
            "content": f"""Please review the following Python code:
            {code_snippet}

            Perform the following tasks:
            1. Identify any bugs or potential issues.
            2. Detect any security vulnerabilities or bad practices.
            3. Suggest improvements for performance, readability, or maintainability.
            4. Finally, state whether this code is ready to be committed to Git or if changes are required.
            """,
        },
    ]

    # Invoke model (assumes client is defined outside)
    response = client.invoke(messages)
    ai_review = response.content

    # Append formatted review to a single review.txt
    filename = os.path.basename(file_path)
    with open(review_file, "a", encoding="utf-8") as out_file:
        out_file.write(f"\n\n================= {filename} =================\n")
        out_file.write(f"================= AI Review =================\n")
        out_file.write(f"{ai_review}\n")
def process_files_in_directory(directory, review_file="review.txt"):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                analyze_python_file(file_path, review_file)


directory = os.path.join(os.getcwd(), "app")
# Call the function to process files
process_files_in_directory(directory)
