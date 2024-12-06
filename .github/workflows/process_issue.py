import os
import anthropic
import json
from github import Github

def get_claude_response(prompt):
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content

def update_readme(recent_questions):
    with open('README.md', 'r') as file:
        content = file.read()
    
    questions_section = "\n".join([
        f"- Q: {q['question']}\n  A: {q['answer'][:200]}..." 
        for q in recent_questions[:5]
    ])
    
    start_marker = "<!-- CLAUDE-RECENT-QUESTIONS -->"
    end_marker = "<!-- CLAUDE-RECENT-QUESTIONS-END -->"
    
    new_content = content.split(start_marker)[0] + start_marker + "\n" + \
                 questions_section + "\n" + end_marker + \
                 content.split(end_marker)[1]
    
    with open('README.md', 'w') as file:
        file.write(new_content)

def main():
    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
    issue = repo.get_issue(number=int(os.environ['GITHUB_EVENT_ISSUE_NUMBER']))
    
    response = get_claude_response(issue.body)
    issue.create_comment(response)
    
    try:
        with open('question_history.json', 'r') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    
    history.insert(0, {
        "question": issue.body,
        "answer": response
    })
    
    with open('question_history.json', 'w') as f:
        json.dump(history[:5], f)
    
    update_readme(history)
    
    os.system('git config --global user.name "GitHub Action"')
    os.system('git config --global user.email "action@github.com"')
    os.system('git add README.md question_history.json')
    os.system('git commit -m "Update README with new Claude response"')
    os.system('git push')

if __name__ == "__main__":
    main()