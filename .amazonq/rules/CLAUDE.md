# Instructions for Claude Code

## Workflow Requirements

Every time a request is made, follow these steps:

### 1. Create CHECKLIST.md
- Create a structured ordered list of tasks that need to be completed
- Format each item as a checkbox using `- [ ]` syntax
- Update the checklist as work progresses by marking completed items with `- [x]`
- At the bottom of the checklist, create a copy of the original prompt that was passed in by the user.

### 2. First Item: Clarifying Questions
- The first item on every checklist must be: "Ask top 3 clarifying questions"
- Identify and ask the 3 most important clarifying questions about the request
- Mark this item complete once questions are asked and answered

### 3. Task Execution
- Work through the checklist in order
- Mark each item complete with `[x]` when finished
- Keep the checklist updated throughout the workflow

## Example Checklist Format

```markdown
# Checklist

- [ ] Ask top 3 clarifying questions
- [ ] Task item 2
- [ ] Task item 3
- [x] Completed task example

User's prompt here
```

