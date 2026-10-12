# GH-300 Budget Buddy Demo Script

This script is aligned to the five modules of the official GH-300 course. Each
module below maps a learning objective to a live Budget Buddy demo you can run.
Pick the depth that fits your time slot (45-90 minutes).

## Module Map

| Module | Theme | Budget Buddy demo | Key assets |
| --- | --- | --- | --- |
| 1 | Introduction to GitHub Copilot | Set up, run the app, explain repository instructions | `setup_demo.ps1`, `.github/copilot-instructions.md` |
| 2 | Exploring Copilot's Features | Chat, Inline Chat, CLI, focused context | `calculator.py`, `file_handler.py` |
| 3 | Developer Use Cases | Generate, transform, optimize, document, DevOps | `data_processor.py`, `Dockerfile`, CI |
| 4 | Building Unit Tests | The coverage journey from ~30% to 90%+ | `tests`, `pytest.ini` |
| 5 | Advanced Capabilities | Agent Mode, AGENTS.md, Skills, MCP, PR review | `AGENTS.md`, `.github/skills` |

> Python note for Module 4: the course slides use C# / xUnit / a BankAccount
> sample. This repo is Python / pytest. Map the concepts directly: Test Explorer
> ≈ pytest output, `[Fact]` ≈ a `test_` function, and `@workspace /tests` works
> the same way.

---

## Before You Begin — Work on a Branch

Create a feature branch off `main` before the demo. Everything you build across
Modules 2-5 lands on this branch, which keeps `main` clean for re-runs and sets up
the Module 5e pull request naturally.

```powershell
git switch -c demo/budget-buddy-walkthrough
```

Talking points:

- All Module 2-5 edits accumulate here as one coherent changeset.
- At the end (Module 5e) you open a PR from this branch and let Copilot review it.
- To reset between sessions, just discard the branch and recreate it:

```powershell
git switch main
git branch -D demo/budget-buddy-walkthrough
```

> Presenter note: if you prefer, commit after each module so the PR diff tells a
> clean story. The `reset_for_demo.ps1` script restores the starter state if you
> need a full reset.

---

## Module 1 — Introduction to GitHub Copilot

Goal: set context. Show that this is a real, working app, not isolated snippets,
and that Copilot uses workspace context and repo instructions.

Run:

```powershell
.\setup_demo.ps1
python main.py
```

Talking points:

- What Copilot is and the value proposition (less boilerplate, faster onboarding).
- Responsible AI: suggestions are assistive; the developer stays accountable.
- Repository instructions are implicit context: Copilot may follow them even when
  the prompt does not repeat every requirement.

### 1a. Minimal repository instructions

Open [.github/copilot-instructions.md](.github/copilot-instructions.md) before the
first coding demonstration. Point out that the starter file contains only stable,
always-on context and engineering conventions:

- this is an intentionally immature Python training app;
- use pytest for tests and the shared logger for app output;
- use type hints and prefer small, readable functions;
- preserve intentional demo issues unless the user asks to fix them.

Ask Copilot in **Ask** mode:

```text
Read the repository instructions. What context and coding conventions will you
apply while working in this repository?
```

Narration:

> "Repository instructions are automatically included as context. At this point
> they are deliberately small: they tell Copilot what this project is and define
> conventions that should apply to every interaction. We will turn this into a
> fuller team workflow in Module 5, after we have seen the core Copilot surfaces."

Talking points:

- Do not make documentation or changelog edits an early surprise. Modules 2-4
  should keep a clear requested code → relevant tests → validation story.
- This is a preview of customization, not the customization lesson itself.
- The developer remains responsible for reviewing suggestions even when Copilot
  follows checked-in instructions correctly.

### 1b. Settings worth showing

Open Settings with `Ctrl+,` and type `copilot` to reveal the whole surface, then
call out a few that matter. Switch to "Preferences: Open Settings (JSON)" to make
the point that everything is just text and that workspace settings (this repo's
`.vscode/settings.json`) ship with the code.

| Setting | Why it matters in the demo |
| --- | --- |
| `github.copilot.enable` | Per-language on/off — show disabling Copilot in secrets/`.env` files. |
| `editor.inlineSuggest.enabled` | Master switch for ghost-text completions. |
| `github.copilot.nextEditSuggestions.enabled` | The newer "predict my next edit" feature. |
| `chat.agent.enabled` | Turns on Agent mode (the star of Module 5). |
| `chat.tools.autoApprove` | Auto-run tools without confirmation — good trust/safety talking point. |
| `chat.mcp.enabled` | Enables Model Context Protocol servers (Module 5). |
| `github.copilot.chat.codeGeneration.useInstructionFiles` | Makes Copilot honor `.github/copilot-instructions.md`. |
| `chat.agentSkillsLocations` | Configures the workspace and user locations where Copilot discovers Skills. |
| `telemetry.telemetryLevel` | Privacy/enterprise trust — what data is sent. |

> This repo preconfigures `inlineChat.askInChat: false` in `.vscode/settings.json`
> so `Ctrl+I` reliably opens classic Inline Chat for the Module 2 demo.

### 1c. Chat modes and custom agents

When you open the Copilot Chat input box you see a mode picker with three options.
These ship with the GitHub Copilot extension in VS Code (`v1.99+`) and are
available to **everyone**:

| Mode | What it does |
| --- | --- |
| **Ask** | Default. Answers questions in chat; never edits files or runs commands autonomously. |
| **Plan** | Produces a step-by-step plan for review *before* executing — ideal for showing learners what an agentic workflow looks like without surprise edits. |
| **Agent** | Full agentic mode: reads files, edits multiple files, runs terminal commands, and iterates in one turn. The star of Module 5. |

Below the modes you may see a list of **custom agents** (e.g. *AIAgentExpert*,
*Azure IaC Exporter*, *AzureCostOptimizeAgent*, and others). These are **not**
part of the standard Copilot product — they are agents configured in your
personal VS Code environment, typically installed by internal Microsoft tooling
(AI Toolkit / Foundry Toolkit extension or `.agent.md` config files). External
customers will not have them unless they build their own.

The **ability** to create custom agents *is* available to everyone via
`Configure Custom Agents...`. The specific Azure-centric ones shown here are
MS-internal.

> Presenter note: when demoing to customers, show the `Configure Custom Agents…`
> option as proof that teams can author domain-specific agents for their own
> stack. Do not demo the MS-internal Azure agents unless your audience has the
> same tooling configured.

### 1d. Explore the GitHub Copilot Trust Center

The Trust Center is a public, no-login page. Open it live in a browser — nothing
to configure first.

**URL:** [https://copilot.github.trust.page](https://copilot.github.trust.page)

Walk the page top to bottom:

1. **Compliance badges** — SOC 1, SOC 2, SOC 3, ISO 27001:2013, CSA STAR Level 2,
   TISAX, and ISO/IEC 42001:2023 (the AI management system standard, achieved
   March 2026). Click any badge to download the certificate or report.
2. **Data used section** — four categories GitHub collects:
   - *Prompts* — your code context and chat input sent to the model.
   - *Suggestions* — the AI responses returned to you.
   - *Feedback data* — thumbs up/down and support tickets.
   - *User engagement data* — pseudonymous interaction metrics (accepted/dismissed
     completions, error logs).
3. **FAQ** — click "Does GitHub use Copilot Business or Enterprise data to train
   AI models?" The answer is **no**. This is the slide every legal/security team
   asks about — show it directly rather than quoting it.
4. **Resources tab** — downloadable SOC 2 Type 2 report, bridge letters, PCI DSS
   report. Useful for enterprise procurement.
5. **Updates tab** — shows the compliance changelog. Demonstrates that the posture
   is maintained and auditable over time.

Talking points:

- This is what you send to your CISO, legal team, or enterprise customer before
  procurement — one URL, all the evidence.
- The ISO/IEC 42001 cert is notable: it is the international standard for AI
  management systems, not just security. GitHub is one of the first major AI
  platforms to hold it.
- The "no training on Business/Enterprise data" commitment is contractual, not
  just a policy page — it is backed by the Microsoft Product Terms.

---

### 1e. Managing GitHub Copilot policies (org admin demo)

> **Requires:** Organization owner or enterprise admin role on GitHub.com.
> If you are showing this to an audience, screenshare your own org settings —
> do not ask attendees to change their org policies live.

**Path:** GitHub.com → your profile picture (top-right) → **Your organizations** →
select org → **Settings** tab → sidebar: **Code, planning, and automation** →
**Copilot** → **Policies**

Step by step:

1. Go to **github.com**, click your profile picture (top-right), choose
   **Your organizations**, then click the org you want to manage.
2. Click the **Settings** tab in the org header.
3. In the left sidebar, under *Code, planning, and automation*, click **Copilot**.
4. Click **Policies** (next to Models) to see the feature policy panel.
5. Walk through the key policy toggles:

   | Policy | What to show |
   | --- | --- |
   | **Suggestions matching public code** | Set to *Blocked* to prevent suggestions that match licensed public code — the IP protection talking point. |
   | **Copilot Chat in IDE and mobile** | Enable or restrict Chat access org-wide. |
   | **Copilot on GitHub.com** | Controls the web UI chat and PR summaries. |
   | **MCP servers in Copilot** | Enables/restricts Model Context Protocol server support (Module 5 topic). |
   | **Agent apps** | Separate toggle for third-party Copilot agent app marketplace access. |
   | **Opt in to preview features** | Lets your org try GA-candidates before official release. |

6. Click **Models** (next to Policies) to show which models are available
   (e.g. GPT-4o, Claude Sonnet, Gemini) and whether the org allows premium models
   that may incur additional cost.
7. To manage **seats**: in the same sidebar click **Access** → here you can assign
   seats by team, revoke individual seats, and see *last active* dates to identify
   unused licenses.

> **Enterprise vs. org:** if the org is inside a GitHub Enterprise Cloud account,
> an enterprise admin can lock policies at the enterprise level — the org-level
> dropdown will show greyed-out values for locked policies. Mention this so
> admins understand the inheritance model.

Talking points:

- Policies are enforced server-side. An individual developer cannot override the
  "block matching public code" policy by changing a VS Code setting.
- Seat management via *last active* makes it easy to reclaim licenses from
  developers who have stopped using Copilot.
- The **Models** tab lets the org balance capability vs. cost — premium models
  are opt-in per org, not on by default.

No code changes in this module.

---

## Module 2 — Exploring Copilot's Features

Goal: demonstrate the core surfaces — Copilot Chat, Inline Chat, the CLI, and
prompt engineering with added context.

### 2a. Explain the workspace (Chat)

```text
Explain this repository. What does the app do, what are the main files, and where should I start reading?
```

### 2b. Inline Chat on a function

Open [calculator.py](calculator.py), select `savings_rate()`, and use Inline Chat:

```text
Explain what this method does and what happens when income is zero.
```

This naturally surfaces a real bug to revisit in Module 4.

> Presenter note: the code no longer carries `# BUG` spoiler comments. The
> zero-income bug is documented in
> [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md#L11) (Savings rate row).

### 2c. Copilot in the terminal

There are two different "terminal" surfaces. Show both so the distinction is clear.

**1) `@terminal` chat participant (inside VS Code).** Type this in the Copilot
**Chat** panel — not the shell. It specializes in shell/terminal questions and
gives a one-click Run button:

```text
@terminal How do I run the tests with coverage in this repo?
```

**2) GitHub Copilot CLI (standalone `copilot` in your shell).** This is a separate
agentic tool you launch from PowerShell. Start an interactive session:

```powershell
copilot
```

Then ask, in natural language, inside the Copilot CLI prompt:

```text
How do I run this app and its tests with coverage?
```

```text
Inspect .gitignore, then add an entry for generated *.log files if it is missing
and explain why Budget Buddy should not commit runtime logs.
```

You can also run a one-shot prompt without entering the session:

```powershell
copilot -p "Explain what main.py does in two sentences."
```

Talking points:

- `@terminal` lives in the editor's Chat; the `copilot` CLI lives in the terminal
  and can read files and run commands with your approval.
- Both honor repo context, so answers are tailored to Budget Buddy (pytest, the
  `.venv`, the coverage gate) rather than generic.

### 2d. Focused context (security example)

The course shows a "review this banking app for security" prompt. The Budget
Buddy equivalent is the path-traversal gap in file handling. Select
[file_handler.py](file_handler.py) and ask:

```text
Review file_handler.py for path traversal and unsafe file handling. Ex
plain the risk before changing code.
```

Emphasize how a focused prompt plus repo context produces a better answer than a
vague one.

> Presenter note: the path-traversal gap is in `read_transactions_json`, logged
> in [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md#L13) (Security row).

---

## Module 3 — Developer Use Cases

Goal: walk the generate / transform / optimize / document / explain loop, plus a
DevOps beat.

### 3a. Generate code from a TODO

Open [calculator.py](calculator.py) and implement `forecast_month_end_spend()` or
`is_over_budget()` from the TODO stubs.

### 3b. Transform / refactor

```text
Transform group_expenses_by_category in data_processor.py into a single-pass aggregation.
```

### 3c. Optimize (performance)

Ask Copilot:

```text
Refactor duplicate detection in data_processor.py to avoid O(n^2) behavior while preserving output.
```

> Presenter note: the O(n^2) hotspot is in `find_duplicate_transactions`,
> tracked in [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md#L21) (Performance row).

### 3d. Document and explain

```text
Add concise docstrings and type hints to the public methods in calculator.py.
```

### 3e. DevOps snippets

The repo ships a `Dockerfile` and a CI workflow with intentional TODOs. Ask:

```text
Complete the Dockerfile to run Budget Buddy, then finish the GitHub Actions workflow to install deps and run pytest.
```

---

## Module 4 — Building Unit Tests

Goal: the headline demo. Drive coverage from the ~30% starter baseline to 90%+.

### 4a. Show the starting point

```powershell
pytest
```

Expected: starter tests pass, coverage around 30%.

### 4b. Generate tests

Ask Copilot:

```text
Generate focused pytest tests for BudgetCalculator edge cases, including empty transactions, zero income, zero expenses, and history behavior.
```

You can also use `@workspace /tests` on a selected function.

> Presenter note: the calculator edge-case bugs (empty expenses, category
> percentage, savings rate) are listed in
> [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md#L9) (rows 9-11). Input
> validation lives at
> [INTENTIONAL_ISSUES.md](INTENTIONAL_ISSUES.md#L12).

### 4c. Run, verify, and fix (red-green loop)

```text
Use the pytest failure output to identify the root cause. Fix the smallest relevant code path and rerun the tests.
```

### 4d. Push past 90% and raise the gate

After enough tests pass, raise the bar in [pytest.ini](pytest.ini) from
`--cov-fail-under=30` to `--cov-fail-under=90` (and `fail_under = 90`), then:

```powershell
pytest
```

---

## Module 5 — Advanced Capabilities

Goal: show Copilot beyond the editor — Agent Mode, custom instructions, Skills,
MCP, and the GitHub review workflow.

### 5a. Expand custom instructions into a team workflow

Reopen [.github/copilot-instructions.md](.github/copilot-instructions.md). Remind
the audience that Module 1 introduced a minimal set of always-on conventions.
Now add the workflow policy below to the end of the file:

```markdown
## Change Workflow

- Before editing, identify which repository instructions affect the task.
- Add or update tests first when practical.
- Fix the narrowest relevant code path.
- Run `pytest` after code changes.
- Update `README.md` when setup, commands, or user-facing behavior changes.
- Update `CHANGELOG.md` for meaningful user-facing changes.
- Before committing, summarize changed files, tests run, and remaining risks.
```

Narration:

> "In Module 1 these instructions supplied stable project context. We are now
> evolving them into checked-in team policy. The next request will mention only
> the feature; tests, validation, documentation, and release notes should appear
> because of these rules rather than because I repeat them in every prompt."

Ask Copilot in **Ask** or **Plan** mode:

```text
Which repository instructions will affect the next feature change, and which
additional files might those instructions require you to update?
```

Review the answer before starting the agent task. This makes the expected
multi-file scope explicit without giving away the implementation.

### 5b. Agent Mode multi-file feature

Switch to **Agent** mode and enter a deliberately minimal request directly in
Chat. Do not invoke `/agent-feature` for this demonstration because that Skill
explicitly includes tests, docs, changelog, and validation steps; here we want
the repository instructions to be the only source of those requirements.

```text
Add CSV export support for transactions.
```

Watch Copilot plan, edit several files, run tests, and report back. When reviewing
the diff, connect each additional file to the workflow rule that caused it:

| Observed change | Instruction behind it |
| --- | --- |
| Tests added or updated | Add or update tests first when practical. |
| `pytest` executed | Run `pytest` after code changes. |
| `README.md` updated | Document changed commands or user-facing behavior. |
| `CHANGELOG.md` updated | Record meaningful user-facing changes. |
| Final summary | Report files, tests, and remaining risks before committing. |

Narration:

> "The agent did not independently decide that every feature needs release notes.
> We changed the repository's operating policy, and the agent followed it. If
> these changes are not what the team wants, we improve the checked-in policy
> instead of correcting every future prompt."

### 5c. AGENTS.md and Skills

Open [AGENTS.md](AGENTS.md) and [.github/copilot-instructions.md](.github/copilot-instructions.md).

Narration:

> "Copilot reads project files that describe *how we work*. `copilot-instructions.md`
> sets repo-wide rules, and `AGENTS.md` gives an agent its operating manual for this
> repo — build and test commands, conventions, and guardrails. Because these live
> in the repo, every teammate and every Copilot session follows the same playbook.
> We introduced minimal always-on instructions in Module 1, expanded them into a
> workflow in Module 5a, and have now seen Agent mode apply that workflow."

#### Skills (SKILL.md)

Open [.github/skills/add-budget-report-section/SKILL.md](.github/skills/add-budget-report-section/SKILL.md)
and show its structure.

Narration:

> "Skills are reusable, on-demand playbooks. A `SKILL.md` packages domain
> knowledge and step-by-step instructions for a specific task — here, 'add a new
> budget report section' — with a name and description Copilot can match against
> your request. Skills can be discovered automatically or invoked explicitly with
> `/`; the migrated workshop Skills set `disable-model-invocation: true` so the
> trainer controls exactly when they run. Copilot loads the full instructions only
> when the Skill is invoked, avoiding unnecessary context. Think of instructions
> as *always-on rules*, prompts as *single focused task templates*, and Skills as
> *reusable workflows that can also bundle scripts and reference material*."

Optional live beat:

```text
Add a new "top merchants" section to the budget report.
```

Let Copilot discover and follow the Skill.

A Skill can also bundle scripts. Open
[.github/skills/run-coverage/SKILL.md](.github/skills/run-coverage/SKILL.md),
which ships `run-coverage.sh` and `run-coverage.ps1` alongside its instructions:

```text
Run the test coverage report.
```

Copilot matches the `run-coverage` skill and runs the bundled script (asking for
confirmation first, since `shell` is not pre-approved). Mention that
`allowed-tools: shell` would skip that prompt in a trusted repo.

### 5d. MCP servers

Talking point: MCP lets Copilot reach external tools and data (issues, databases,
docs) through a standard protocol. Mention the configured MCP servers available in
this environment as an example of extending Copilot's reach.

### 5e. Coding Agent and PR review

This is the closing "ship it" story: take the changes you just made with Copilot,
open a pull request, and let **Copilot review its own PR on github.com**.

**1) Create the PR from VS Code.** With your branch's changes committed, ask
Copilot to draft and open the PR from the `demo/budget-buddy-walkthrough` branch
you created in [Before You Begin](#before-you-begin--work-on-a-branch) (the GitHub
Pull Requests extension exposes this as a tool/skill):

```text
Create a pull request for my current branch. Write a title and description summarizing the changes, the tests run, and any risks.
```

Copilot reads the diff (`#changes`), drafts the title/body, and opens the PR. You
can also draft the body first with the
[pr-summary Skill](.github/skills/pr-summary/SKILL.md):

```text
Summarize the current diff as a pull request description with test results and risk notes.
```

**2) Show the Copilot review on github.com.** Open the PR in the browser and add
**Copilot** as a reviewer (Reviewers → *Copilot*), or it may review
automatically if the repo has that rule enabled. Walk the audience through:

- the **PR summary** Copilot generates at the top of the page,
- the **inline review comments** Copilot leaves on specific lines (style, bugs,
  edge cases, suggested changes),
- accepting a **suggested change** with one click, and re-requesting review.

**3) Optional — Coding Agent end to end.** Assign a GitHub issue to **Copilot**
and let the coding agent open a PR by itself, then circle back to the review flow
above. Mention PR review + Actions troubleshooting as the bookend to the local
pipeline you finished in Annex A.

> Presenter note: the *Create PR* and *review* steps need a GitHub remote with
> push access and the GitHub Pull Requests extension signed in. If you're offline
> or on a fork without access, fall back to drafting the PR description with
> `pr-summary.prompt.md` and narrate the github.com review from a screenshot.

### 5f. Chat shortcuts worth knowing (`/`, `@`, `#`)

A quick "get to know Copilot" beat. In the Chat box, three keystrokes change what
you're addressing. Type each one live and let the menu pop up.

| Key | What it is | Example |
| --- | --- | --- |
| `/` | **Slash commands** — built-in intents plus this repo's Skills | `/explain`, `/tests`, `/fix`, and `/agent-feature`, `/security-review` |
| `@` | **Participants** — scope *who* answers | `@workspace`, `@terminal`, `@vscode` |
| `#` | **Context references** — attach *what* to look at | `#file`, a selected symbol, `#changes` |

Talking points:

- **`/` (slash):** the fastest shortcuts. Built-ins like `/explain`, `/tests`,
  `/fix`, `/doc`, and `/new` are one-word versions of common requests. Skills
  under [.github/skills](.github/skills) also appear here because they are
  user-invocable by default. `/agent-feature` is the reusable, explicit-workflow
  alternative to the minimal request used in Module 5b; it packages code, tests,
  docs, changelog, and validation into one command.
- **`@` (participants):** decide who handles the question. `@workspace` reasons
  over the whole repo, `@terminal` specializes in shell commands (see 2c), and
  `@vscode` answers editor/settings questions.
- **`#` (context):** pin specific context to a message — `#file` to attach a file,
  a highlighted symbol, or `#changes` to reference the current diff. Great for
  keeping Copilot focused on exactly the right code.

Demo tip: combine them — e.g. `@workspace /tests #file:calculator.py` says
"workspace participant, generate tests, for this file."

---

## Backup Demo Path

If live generation runs long, implement one narrow slice end to end:

1. Fix `savings_rate()` zero-income behavior (Module 2/4).
2. Add tests for it (Module 4).
3. Rerun `pytest`.
4. Ask Copilot to summarize the diff (Module 5).

---

## Annex A — DevOps files (`Dockerfile` and CI workflow)

Module 3e references these two files, but they ship **intentionally incomplete**
so you can complete them live with Copilot. This annex is a self-contained,
optional deep-dive you can run any time you want a DevOps beat. Neither file is
exercised by `pytest`, so finishing them won't affect the coverage journey.

### Starting state

| File | What's missing |
| --- | --- |
| [Dockerfile](Dockerfile) | `WORKDIR`, dependency install, app copy, and the run command are TODO stubs. |
| [.github/workflows/ci.yml](.github/workflows/ci.yml) | Python setup, dependency install, and the pytest step are TODO stubs. |

> Talking point: both files carry guiding TODO comments. This mirrors a real
> onboarding task — "finish the pipeline" — and shows Copilot turning intent in
> comments into working DevOps config.

### A1. Complete the Dockerfile

Open [Dockerfile](Dockerfile) and prompt (Agent mode works well here):

```text
Complete this Dockerfile so Budget Buddy runs in a container: set a working directory, install dependencies from requirements-test.txt, copy the app, and run python main.py.
```

Expected result: a slim image based on `python:3.13-slim` with `WORKDIR`,
dependency caching (copy manifest → install → copy source), and
`CMD ["python", "main.py"]`.

Validate (optional, if Docker is available on the demo machine):

```powershell
docker build -t budget-buddy .
docker run --rm budget-buddy
```

> Presenter note: if Docker isn't installed, just review the generated file and
> explain the layer-caching order (manifest before source). No build required to
> make the teaching point.

### A2. Finish the CI workflow

Open [.github/workflows/ci.yml](.github/workflows/ci.yml) and prompt:

```text
Finish this GitHub Actions workflow: set up Python 3.13, install dependencies from requirements-test.txt, and run pytest with coverage.
```

Expected result: the `test` job gains `actions/setup-python@v5` (Python 3.13), a
`pip install -r requirements-test.txt` step, and a `pytest` step.

Talking points:

- Tie it back to Module 4: the same `pytest` gate that runs locally now runs on
  every push and PR.
- Mention that Copilot honored the repo's existing patterns (pinned action
  versions, `requirements-test.txt`) because it read the surrounding context.

### A3. Optional: validate the workflow without pushing

You can lint or dry-run the YAML locally:

```powershell
# Schema/lint check in the editor: open ci.yml and check the Problems panel.
# Or, if you have 'act' installed, dry-run the job:
act -n
```

> Wrap-up: this annex closes the "code → tests → ship" story — Module 3 generated
> and refactored code, Module 4 proved it with tests, and these two files take it
> to a reproducible container and an automated pipeline.
