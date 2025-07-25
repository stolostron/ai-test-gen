# AI Test Generation 🤖

This repository hosts an AI project focused on automating the generation of end-to-end (E2E) test scripts. The primary goal is to create an intelligent agent that can analyze JIRA tickets and pull requests to produce fully functional **Cypress** test scripts.

---

## 🎯 Core Objective

As a QE team, our goal is to improve testing efficiency, increase test coverage, and reduce the manual effort required to write and maintain test automation. This project investigates the use of AI to automatically generate test scripts by interpreting the context and code changes associated with a new feature or bug fix.

### Key Goals:
* **Automated Script Generation:** Leverage AI to create Cypress test scripts directly from the information in JIRA tickets (descriptions, acceptance criteria, comments).
* **Context from Code:** Analyze developer pull requests (PRs) to understand the scope of changes and inform the generated tests.
* **Increased Efficiency:** Reduce the time it takes for a QE engineer to write initial test automation for a new feature.
* **Improved Coverage:** Allow the AI to suggest test scenarios that might be missed during manual test case design.

---

## ⚙️ How It Works (High-Level)

The AI agent will follow a simple, powerful workflow:

1.  **Ingest Data:** The system will take a JIRA ticket and a corresponding PR as input.
2.  **Analyze Content:** It will parse key information:
    * **JIRA Ticket:** Value Statement, Description, and Acceptance Criteria.
    * **Pull Request:** Code diffs, file changes, and commit messages.
3.  **Generate Test:** Based on the analysis, the AI will generate a draft of a Cypress test file (`.cy.js` or `.cy.ts`).
4.  **Review & Refine:** The QE engineer reviews the generated script, makes any necessary adjustments, and commits it to the test suite.

---

## 🚀 Getting Started

This section will be updated with instructions on how to set up and run the AI agent locally.

```bash
# Clone the repository
git clone [https://github.com/stolostron/ai-test-gen.git](https://github.com/stolostron/ai-test-gen.git)

# Installation steps (TBD)
cd ai-test-gen
npm install

# How to run the script (TBD)
# Example: node generate-test.js --jira=TICKET-123 --pr=456
