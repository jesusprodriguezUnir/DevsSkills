# Agent Guidelines: MySkills Project

## The Four Principles
These principles must be followed strictly by every agent (Antigravity, Claude, VS Code Copilot, etc.) interacting with this repository.

### 1. Think Before Coding
- **No Assumptions**: Never assume requirements. If a task is unclear or has multiple paths, surface the trade-offs and ask for clarification.
- **Plan First**: For architectural changes or new features, a formal implementation plan must be reviewed.

### 2. Simplicity First
- **Minimalism**: Write the minimum code necessary to achieve the goal.
- **No Premature Abstractions**: Avoid hooks, patterns, or libraries that aren't immediately required.
- **YAGNI**: You Ain't Gonna Need It. Focus on current requirements.

### 3. Surgical Changes
- **Targeted Edits**: Only modify what is strictly necessary.
- **Respect Context**: Do not refactor unrelated code or "improve" style in adjacent files unless explicitly requested.

### 4. Goal-Driven Execution
- **Success Criteria**: Define what success looks like BEFORE implementation.
- **Verification**: Every change must be verified (automated tests, manual validation, or visual audit).

---

## Technical Stack
- **Framework**: Astro (Static)
- **Styling**: Vanilla CSS (Modern CSS Variables, Flex/Grid)
- **Data**: Astro Content Collections (Markdown)
- **Principle**: No database by default; scale only when requested.
