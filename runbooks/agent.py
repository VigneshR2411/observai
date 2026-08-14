import requests
from github import Github

# 1. Local RAG Memory (Past Runbooks)
runbooks = [
    "Incident: Checkout endpoint high latency. Cause: Downstream payment service connection pool exhausted under load. Fix: Increased pool size, added circuit breaker with 2s timeout.",
    "Incident: Health endpoint returns 500 error. Cause: Database connection timeout due to expired credentials. Fix: Rotated database credentials and increased connection idle timeout.",
    "Incident: Order endpoint slow. Cause: High CPU from memory leak. Fix: Restarted pod and applied memory limit."
]

# 2. Find similar incidents
def find_similar(problem):
    matches = []
    for r in runbooks:
        if any(word in r.lower() for word in problem.lower().split()):
            matches.append(r)
    return matches[:2]

# 3. LLM Diagnosis via Ollama
def diagnose(problem):
    similar = find_similar(problem)
    context = "\n---\n".join(similar)
    prompt = f"A production issue occurred: {problem}\n\nSimilar past incidents:\n{context}\n\nBased on this, give: 1) likely root cause 2) suggested fix. Be concise."
    
    try:
        r = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': 'llama3.2', 'prompt': prompt, 'stream': False}
        )
        data = r.json()
        return data.get('response', f"Ollama error: {data}")
    except Exception as e:
        return f"Failed to connect to Ollama: {e}"

# 4. File GitHub Issue
def file_issue(title, diagnosis):
    GITHUB_TOKEN = "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"  # REPLACE THIS
    REPO_NAME = "VigneshR2411/observai"                      # REPLACE THIS
    
    try:
        gh = Github(GITHUB_TOKEN)
        repo = gh.get_repo(REPO_NAME)
        issue = repo.create_issue(title=title, body=diagnosis)
        print(f"✅ Issue created! URL: {issue.html_url}")
    except Exception as e:
        print(f"❌ Failed to create issue: {e}")

# 5. Run the agent
if __name__ == "__main__":
    fake_problem = "Checkout API is timing out and showing slow response times"
    print("🤖 Analyzing problem...")
    diagnosis = diagnose(fake_problem)
    print("\n🧠 Diagnosis:\n", diagnosis)
    print("\n📝 Filing GitHub issue...")
    file_issue("[ObservAI] Checkout Timeout", diagnosis)
    print("🎉 Done!")