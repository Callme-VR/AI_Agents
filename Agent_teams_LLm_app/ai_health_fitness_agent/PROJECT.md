# 🤖 AI Health & Fitness Agent — Project Documentation

> A complete walkthrough of `agent.py`: what each part does, how the code flows, and how the AI agents work under the hood.

---

## 📌 1. Project Overview

**What is this project?**
A **Streamlit web app** that uses **AI agents** (built with the **Agno** framework) powered by **Google Gemini** to generate **personalized diet plans** and **workout routines** based on a user's body stats, activity level, and fitness goals. After generating a plan, the user can ask **follow-up questions** about it.

**One-liner:**
> A multi-agent AI system where a "Diet Agent" and a "Fitness Agent" collaborate to produce personalized health plans, with a chat-style Q&A on top.

**Who is it for?**
Anyone learning how to build **LLM-powered agents** with a clean, friendly UI — beginners to intermediate AI developers.

---

## 🧠 2. Key Concepts to Understand First

| Concept | Explanation |
|---|---|
| **Streamlit** | A Python library that turns scripts into web apps with no HTML/JS needed. |
| **LLM (Large Language Model)** | An AI model (here: Google's Gemini) that generates text. |
| **Agent** | An LLM wrapped with **instructions** (a system prompt) and a defined role/task. |
| **Agno** | A framework (`agno` package) for building AI agents with a clean Python API. |
| **Gemini** | Google's family of LLMs. This project uses `gemini-2.5-flash` (fast, cheap, capable). |
| **Session State** | Streamlit's way of remembering variables between user interactions. |
| **Prompt** | The text you send to the LLM. Better prompts → better outputs. |
| **Multi-agent** | Using **multiple specialized agents** instead of one generalist — each does one job well. |

---

## 🏗️ 3. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                  AI HEALTH & FITNESS AGENT — FLOW                    │
└──────────────────────────────────────────────────────────────────────┘

   [👤 User opens browser → http://localhost:8501]
                       │
                       ▼
        ┌──────────────────────────────┐
        │   STREAMLIT UI (agent.py)   │
        │  ┌────────────────────────┐  │
        │  │ Sidebar: Gemini API key│  │
        │  └────────────────────────┘  │
        │  ┌────────────────────────┐  │
        │  │ Form: age, weight,     │  │
        │  │ height, goal, etc.     │  │
        │  └──────────┬─────────────┘  │
        └─────────────┼────────────────┘
                      │ [Generate Plan] click
                      ▼
   ┌───────────────────────────────────────────────┐
   │         AGENT LAYER (agno + Gemini)           │
   │                                               │
   │   ┌──────────────────┐  ┌──────────────────┐ │
   │   │  🍽 DIETRY AGENT  │  │  💪 FITNESS AGENT│ │
   │   │  Role: Nutrition  │  │  Role: Training  │ │
   │   │  Model: Gemini    │  │  Model: Gemini   │ │
   │   │  Instructions:    │  │  Instructions:   │ │
   │   │  - meal plan      │  │  - warmup/main/  │ │
   │   │  - why it works   │  │    cooldown      │ │
   │   └─────────┬─────────┘  └─────────┬────────┘ │
   │             │                       │          │
   │             ▼                       ▼          │
   │        Meal Plan Text      Workout Plan Text  │
   └───────────────────────────────────────────────┘
                      │
                      ▼
        ┌──────────────────────────────┐
        │  STREAMLIT DISPLAY           │
        │  - Diet Plan (expander)      │
        │  - Workout Plan (expander)   │
        │  - Q&A chat input            │
        └──────────────┬───────────────┘
                       │ [Ask Question] click
                       ▼
        ┌──────────────────────────────┐
        │   💬 Q&A AGENT (general)     │
        │   Input: plan + question     │
        │   Output: contextual answer  │
        └──────────────────────────────┘
```

---

## 📂 4. Project Structure

```
ai_health_fitness_agent/
│
├── agent.py            # The ENTIRE application (single-file Streamlit app)
├── requirements.txt    # Python dependencies
├── venv/               # Virtual environment (created locally)
└── PROJECT.md          # ← This file
```

This is a **single-file project** — everything (UI logic, agents, display, state) lives in `agent.py`. That's intentional: it's easy to read end-to-end.

---

## 🔍 5. Code Walkthrough — Line by Line

### 5.1 Imports (lines 1–4)

```python
import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
from agno.run.agent import RunOutput
```

| Import | Purpose |
|---|---|
| `streamlit as st` | The web UI framework. `st` is the conventional alias. |
| `from agno.agent import Agent` | The `Agent` class — used to create AI agents. |
| `from agno.models.google import Gemini` | The Gemini model wrapper for Agno. |
| `from agno.run.agent import RunOutput` | The response type returned by `agent.run()`. (Note: imported but not actually used in the code — could be removed.) |

**What's Agno?**
Agno is a modern framework for building **agentic AI apps**. It lets you define agents in pure Python — no JSON config, no LangChain abstractions. Each agent has a `name`, a `model`, and `instructions`.

---

### 5.2 Page Configuration (lines 8–13)

```python
st.set_page_config(
     page_title="AI Health & Fitness Agent", 
     page_icon="🤖",
     layout="wide",
     initial_sidebar_state="expanded"
)
```

This sets up the **browser tab and page layout**:
- **Title:** "AI Health & Fitness Agent" (shown in the browser tab).
- **Icon:** 🤖 emoji.
- **Layout:** `"wide"` — uses the full screen width (good for two-column forms).
- **Sidebar:** starts expanded so the API key input is visible.

> ⚠️ `st.set_page_config()` must be the **first Streamlit command** in the script.

---

### 5.3 Helper Function: `display_diet_plan` (lines 16–31)

```python
def display_diet_plan(plane_context):
    with st.expander("Diet Plan", expanded=True):
        col1, col2 = st.columns([2, 1])
        ...
```

**Purpose:** Renders the diet plan in a **collapsible card** with two columns.

**Breakdown:**

| Line | Code | What it does |
|---|---|---|
| 17 | `with st.expander(...)` | Creates a collapsible section (starts expanded). |
| 18 | `col1, col2 = st.columns([2, 1])` | Two columns, **2:1 ratio** — left column is twice as wide. |
| 21 | `st.markdown("### Why this plan works")` | Renders an `<h3>` heading. |
| 22 | `st.write(plane_context.get("why_this_plan_works", ""))` | Safely reads the value; if missing, shows empty string. |
| 24 | `st.write(plane_context.get("meal_plan", "Plan not available"))` | Shows the meal plan text. |
| 28 | `.split('\n')` | Splits the considerations string into a list (one per line). |
| 30 | `if consideration.strip():` | Skips empty lines. |
| 31 | `st.warning(consideration)` | Shows a **yellow warning box** for each tip. |

**Layout:**
```
┌────────────────────────────┬──────────────┐
│ ### Why this plan works    │ ⚠️ Important │
│ <explanation text>         │ - Tip 1      │
│                            │ - Tip 2      │
│ ### Meal Plan              │ - Tip 3      │
│ <meal plan text>           │              │
└────────────────────────────┴──────────────┘
```

---

### 5.4 Helper Function: `display_fitness_plan` (lines 34–49)

Same pattern as the diet display, but for workout content:
- **Left column:** Goals + Exercise Routine
- **Right column:** Important Considerations (warnings)

**Why a separate function?**
Each plan has a different structure (diet has meal_plan, fitness has exercise_routine), so they need different rendering logic.

---

### 5.5 Main Function: `main()` (lines 52–217)

This is the heart of the app. Let's break it into logical blocks.

#### 5.5.1 Session State Initialization (lines 53–57)

```python
if "dietry_plan" not in st.session_state:
    st.session_state.dietry_plan = {}
    st.session_state.fitness_plan = {}
    st.session_state.qa_pairs = []
    st.session_state.plan_generated = False
```

**What is `st.session_state`?**
Streamlit **re-runs the entire script on every user interaction**. Without session state, all variables would reset to default each time. `st.session_state` persists data across reruns.

**Variables stored:**
| Key | Type | Purpose |
|---|---|---|
| `dietry_plan` | dict | The generated diet plan content |
| `fitness_plan` | dict | The generated workout plan content |
| `qa_pairs` | list | List of Q&A dicts (chat history) |
| `plan_generated` | bool | Flag — has the user generated a plan yet? |

**The `if "dietry_plan" not in st.session_state:` guard** ensures initialization happens **only once** (on the first run), not on every rerun.

---

#### 5.5.2 Title and Sidebar (lines 59–69)

```python
st.title("AI Health & Fitness Agent")

with st.sidebar:
    st.header("api configurations")
    gemini_api_key = st.text_input("Gemini API Key", type="password", ...)
    
    if not gemini_api_key:
        st.warning("Please enter your Gemini API key to enable the agent")
        return  # ← Stops execution here
```

- The title `"AI Health & Fitness Agent"` appears at the top.
- The **sidebar** contains the API key input.
- `type="password"` masks the key as the user types (dots instead of characters).
- If no key is provided, the app **stops early** with a warning. The `return` exits `main()` before any agent logic runs.

**Why ask for the API key in the UI (not in code)?**
- Safer — the key isn't hardcoded in the source.
- Each user can use their own key.
- No need for a `.env` file.

---

#### 5.5.3 Gemini Model Initialization (lines 72–77)

```python
if gemini_api_key:
    try:
        Gemini_model = Gemini(id="gemini-2.5-flash", api_key=gemini_api_key)
    except Exception as e:
        st.error(f"Error initializing Gemini model: {e}")
        return
    st.header("Agent is ready to use!")
```

- Creates a **Gemini model instance** with the user's API key.
- Model: `gemini-2.5-flash` — Google's fast, cost-effective model.
- If initialization fails (e.g., bad key, network issue), an error is shown and execution stops.

> ⚠️ **Note:** `gemini-2.5-flash` may not be available with all API keys. If you get a model-not-found error, change to `gemini-1.5-flash`.

---

#### 5.5.4 The Form: User Inputs (lines 81–110)

```python
col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, step=0.1)
    activity_level = st.selectbox("Activity Level", [...])
    dietry_preferences = st.selectbox("Dietry Preferences", [...])

with col2:
    weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, step=0.1)
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    fitness_goal = st.selectbox("Fitness Goal", [...])
```

A **two-column form** with input validation:
- `number_input` enforces min/max ranges (no impossible ages/heights).
- `selectbox` provides a fixed list of choices (no free-form typos).

**Inputs collected:**
| Field | Type | Valid Range/Options |
|---|---|---|
| `age` | int | 18–100 |
| `height` | float (cm) | 100.0–250.0 |
| `activity_level` | str | Sedentary / Lightly / Moderately / Very / Extremely Active |
| `dietry_preferences` | str | Vegan, Keto, Low Carb, Dairy Free, Vegetarian, Non-Vegetarian, Other |
| `weight` | float (kg) | 30.0–300.0 |
| `sex` | str | Male / Female / Other |
| `fitness_goal` | str | Weight Loss / Muscle Gain / Maintenance / Endurance / Strength |

---

#### 5.5.5 The "Generate Plan" Button + Agent Logic (lines 111–182)

This is the **core agent logic**.

```python
if st.button("Generate Plan"):
    with st.spinner("Generating your personalized plan..."):
        try:
            # === STEP 1: Build the Diet Agent ===
            dietry_plan = Agent(
                name="Dietry Plan Agent",
                model=Gemini_model,
                instructions=[
                    "Consider the user's input, including dietary restrictions and preferences.",
                    "Suggest a detailed meal plan for the day, including breakfast, lunch, dinner, and snacks.",
                    "Provide a brief explanation of why the plan is suited to the user's goals.",
                    "Focus on clarity, coherence, and quality of the recommendations.",
                ]
            )
            
            # === STEP 2: Build the Fitness Agent ===
            fitness_agent = Agent(
                name="Fitness Plan Agent",
                model=Gemini_model,
                instructions=[
                    "Provide exercises tailored to the user's goals.",
                    "Include warm-up, main workout, and cool-down exercises.",
                    "Explain the benefits of each recommended exercise.",
                    "Ensure the plan is actionable and detailed.",
                ]
            )
            
            # === STEP 3: Build the user profile string ===
            user_profile = f"""
            Age: {age}
            Weight: {weight}
            Height: {height}
            Activity Level: {activity_level}
            Dietry Preferences: {dietry_preferences}
            Gender: {sex}
            Fitness Goal: {fitness_goal}
            """
            
            # === STEP 4: Run Diet Agent ===
            dietry_plan_response = dietry_plan.run(user_profile)
            
            dietary_plan = {
                "why_this_plan_works": "High Protein, Healthy Fats, Moderate Carbohydrates, and Caloric Balance",
                "meal_plan": dietry_plan_response.content,
                "important_considerations": """
                - Hydration: Drink plenty of water throughout the day
                - Electrolytes: Monitor sodium, potassium, and magnesium levels
                - Fiber: Ensure adequate intake through vegetables and fruits
                - Listen to your body: Adjust portion sizes as needed
                """
            }
            
            # === STEP 5: Run Fitness Agent ===
            fitness_plan_response = fitness_agent.run(user_profile)
            fitness_plan = {
                "goals": "Build strength, improve endurance, and maintain overall fitness",
                "exercise_routine": fitness_plan_response.content,
                "important_considerations": """
                - Track your progress regularly
                - Allow proper rest between workouts
                - Focus on proper form
                - Stay consistent with your routine
                """
            }
            
            # === STEP 6: Save to session state ===
            st.session_state.dietary_plan = dietary_plan
            st.session_state.fitness_plan = fitness_plan
            st.session_state.plan_generated = True
            
            # === STEP 7: Render the plans ===
            display_diet_plan(dietary_plan)
            display_fitness_plan(fitness_plan)
        
        except Exception as e:
            st.error(f"Error generating plan: {e}")
            return
```

**What happens step by step:**

| Step | What happens |
|---|---|
| **Spinner** | Shows a "Generating…" animation while agents run. |
| **Build agents** | Two `Agent` objects are created with distinct instructions. They are **stateless definitions** — building them doesn't call the LLM. |
| **Build user_profile** | A plain text string combining all form inputs. This is the **only data** sent to the LLM. |
| **Run Diet Agent** | `dietry_plan.run(user_profile)` sends the profile + instructions to Gemini. Returns a response object with `.content` (the generated meal plan). |
| **Package result** | Hard-coded reasoning ("Why this plan works") and considerations + the agent's meal plan are combined into a dict. |
| **Run Fitness Agent** | Same pattern — separate agent, separate run. |
| **Save to session_state** | Stores both plans so they persist across reruns (e.g., when asking Q&A). |
| **Display** | Calls the helper functions to render the plans visually. |

**🔑 Key Insight — Multi-Agent Pattern:**
Notice that **two separate agents** are used, each with focused instructions. This is a deliberate design choice:
- A single agent would have to balance nutrition + fitness instructions.
- Separating them produces **more focused, higher-quality** outputs.
- Both run **sequentially** (not in parallel) using the same `user_profile`.

---
#### 5.5.6 Q&A Feature (lines 184–215)
```python
if st.session_state.plan_generated:
    st.header("Your Personalized Health & Fitness Plan")
    question_input = st.text_input("Ask me anything about your plan:")

if st.button("Ask Question"):
    if question_input:
        with st.spinner("Thinking..."):
            dietry_plan = st.session_state.dietary_plan
            fitness_plan = st.session_state.fitness_plan
            
            context = f"Dietary Plan: {dietry_plan.get('meal_plan', '')}\n\nFitness Plan: {fitness_plan.get('exercise_routine', '')}"
            full_context = f"{context}\nUser Question: {question_input}"
            try:
                agent = Agent(model=Gemini_model, debug_mode=True, markdown=True)
                Run_response = agent.run(full_context)
                
                if hasattr(Run_response, 'content'):
                    answer = Run_response.content
                else:
                    answer = "Sorry, I couldn't generate an answer."
                
                st.session_state.qa_pairs.append({"question": question_input, "answer": answer})
            except Exception as e:
                st.error(f"Error generating answer: {e}")
```

**How Q&A works:**

1. **Check the flag:** Only show the question input if a plan has been generated.
2. **User types a question.**
3. **Build a context string** that combines:
   - The diet plan (meal plan)
   - The fitness plan (exercise routine)
   - The user's question
4. **Send to a fresh `Agent`** — note this is a **third, different agent** (no specific name or instructions). It uses `debug_mode=True` for verbose logging and `markdown=True` to render formatted output.
5. **Extract the answer** from the response.
6. **Append to `qa_pairs`** in session state — this is the chat history.

**Then later:**
```python
if st.session_state.qa_pairs:
    st.header("Q&A History")
    for i, qa in enumerate(st.session_state.qa_pairs):
        st.subheader(f"Question {i+1}")
        st.write(f"**Q:** {qa['question']}")
        st.write(f"**A:** {qa['answer']}")
```

Iterates through the history and displays each Q&A pair.

---

#### 5.5.7 Script Entry Point (lines 218–219)

```python
if __name__ == "__main__":
    main()
```

Standard Python idiom — calls `main()` when the script is run directly.

---

## 🔄 6. End-to-End Execution Flow

When you run `streamlit run agent.py`:

```
1. Browser opens http://localhost:8501
2. Page config sets title, icon, layout
3. main() runs
4. session_state initialized (empty)
5. Title shown, sidebar appears
6. User pastes Gemini API key
7. If no key → warning + early return
8. If key → Gemini model is created
9. Form is shown (age, weight, etc.)
10. User fills form, clicks "Generate Plan"
11. Two agents are instantiated (in memory, not yet called)
12. user_profile string is built
13. dietry_plan.run(profile) → Gemini API call → meal plan
14. fitness_agent.run(profile) → Gemini API call → workout plan
15. Both responses are packaged into dicts
16. Saved to session_state
17. display_diet_plan() and display_fitness_plan() render the cards
18. Q&A input appears
19. User asks a question
20. "Ask Question" clicked
21. Context string built (plans + question)
22. Third agent.run() → answer from Gemini
23. Q&A appended to history
24. History displayed
```

---

## 🧬 7. How the "Agents" Work — Under the Hood

Many beginners wonder: *"What is an AI agent, really?"*

**Conceptually:**
```
Agent = LLM + System Prompt (instructions) + Optional Tools
```

**In this project:**

```python
Agent(
    name="Dietry Plan Agent",            # Just a label
    model=Gemini_model,                  # Which LLM to call
    instructions=[                       # The "system prompt" — a list of strings
        "Consider the user's input...",
        "Suggest a detailed meal plan...",
        "Provide a brief explanation...",
        "Focus on clarity...",
    ]
)
```

**What Agno does behind the scenes when you call `.run(user_profile)`:**

1. Builds the final prompt:
   ```
   SYSTEM: <joined instructions>
   USER:   <user_profile>
   ```
2. Sends it to Gemini's API.
3. Receives the response.
4. Wraps it in a `RunOutput` object (with `.content`, `.messages`, etc.).
5. Returns it.

**That's it.** Agno is a thin, elegant wrapper that:
- Manages the prompt construction.
- Handles API calls.
- Provides response objects.
- (Optionally) supports **tools** — letting agents call functions, search the web, query databases, etc. (Not used in this project.)

**Why is this "agentic"?**
In the broader AI world, "agent" can mean anything from a simple prompted LLM to a fully autonomous multi-step planner. This project uses the **simplest form** — a prompted LLM with a defined role. But the architecture (multiple specialized agents, separate concerns) is a step toward real agentic systems.

---

## 🛠️ 8. Setup & Run

### Prerequisites
- Python 3.10+
- A Google Gemini API key from https://aistudio.google.com/app/apikey

### Steps

```powershell
# 1. Navigate
cd "D:\Ai\Ai_agent\Agent_teams_LLm_app\ai_health_fitness_agent"

# 2. Create a fresh venv (only first time)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
python -m pip install -r requirements.txt

# 4. Run
python -m streamlit run agent.py
```

> ⚠️ Use `python -m streamlit` (not just `streamlit`) if you have path issues with the venv.

### Open
The browser opens at **http://localhost:8501**.

---

## ⚙️ 9. Tech Stack

| Layer | Tech | Purpose |
|---|---|---|
| **UI** | Streamlit | Web interface |
| **Agent Framework** | Agno | Define and run agents |
| **LLM** | Google Gemini 2.5 Flash | Text generation |
| **State** | `st.session_state` | Persist data across reruns |
| **Language** | Python 3.10+ | — |

---

## ✅ 10. Strengths of This Project

- ✅ **Single file** — easy to read, learn from, and modify.
- ✅ **Multi-agent design** — separation of concerns.
- ✅ **No hardcoded secrets** — API key entered in UI.
- ✅ **Graceful error handling** — `try/except` blocks.
- ✅ **Input validation** — bounded numeric inputs.
- ✅ **Session state** — plans persist across reruns.
- ✅ **Interactive Q&A** — extends beyond one-shot generation.
- ✅ **Visual design** — expanders, columns, warning boxes for nice UX.

## ⚠️ 11. Known Limitations & Possible Improvements

| Limitation | Improvement |
|---|---|
| Plans re-generated every button click | Cache results based on input hash |
| Hard-coded "why_this_plan_works" | Let the agent generate that too |
| No streaming — users wait 5–15s | Use `agent.print_response(stream=True)` |
| Single-turn Q&A (no conversation memory) | Store full message history in `session_state` |
| Agents run sequentially | Use `asyncio.gather` for parallelism |
| `RunOutput` imported but unused | Remove unused imports |
| API key not saved between sessions | Use `st.secrets` or local storage |
| `gemini-2.5-flash` may not be available | Add a model selector in the sidebar |
| No PDF/image input for body composition | Add file uploader |
| No persistence of past sessions | Add a database |

---

## 🎤 12. 60-Second Pitch (Memorize This)

> "I built a Streamlit app that uses AI agents to generate personalized diet and workout plans. The user enters their stats in a form, and two specialized Agno agents — a Diet Agent and a Fitness Agent — each call Google's Gemini LLM with the user's profile and their own role-specific instructions. The outputs are shown in expandable cards. After that, a third general agent answers follow-up questions about the plan, with the plans kept in session state as context. The whole thing is a single Python file and demonstrates the multi-agent pattern — using separate focused agents instead of one generalist."

---

## 🔑 13. Interview Questions You Might Be Asked

**Q: What is an AI agent?**
> An LLM wrapped with a system prompt (instructions) and optionally tools, designed to perform a specific role or task. Agents take input, reason over it, and produce output — sometimes taking actions in the process.

**Q: Why use multiple agents instead of one?**
> Specialization. A single agent with too many instructions may produce lower-quality output due to context dilution. Multiple focused agents each do one job well, and their results can be combined.

**Q: What is the role of `instructions`?**
> They form the **system prompt** — the persistent context that defines the agent's role, behavior, output format, and constraints. They're sent to the LLM on every call.

**Q: How does Streamlit's session state work?**
> Streamlit reruns the entire script on every interaction. `st.session_state` is a dictionary-like object that persists values across reruns for the same user session. Without it, all variables would reset on each click.

**Q: What model are you using and why?**
> Gemini 2.5 Flash — it's fast, cheap, and capable enough for structured generation tasks like meal/workout plans. For higher quality, you could switch to Gemini 2.5 Pro.

**Q: How would you add conversation memory?**
> Store all previous Q&A pairs in `session_state.qa_pairs`, and when generating a new answer, concatenate the history into the context string sent to the agent.

**Q: What if Gemini returns malformed JSON?**
> Add a parser with error handling, or use Agno's structured output feature with a Pydantic schema.

---

## 📚 14. Glossary

| Term | Meaning |
|---|---|
| **Agent** | LLM + instructions + optional tools |
| **System Prompt** | Persistent instructions given to the LLM |
| **Multi-agent** | Multiple specialized agents in one system |
| **Agno** | Python framework for building agents |
| **Gemini** | Google's LLM family |
| **Streamlit** | Python framework for building web UIs |
| **Session State** | Per-user persistent storage in Streamlit |
| **Spinner** | Loading indicator in Streamlit |
| **Expander** | Collapsible section in Streamlit |
| **Spinner** | Shows a "loading..." animation |
| **Warning** | Yellow highlighted message box |

---

## 🐞 15. Common Errors & Fixes

| Error | Cause | Fix |
|---|---|---|
| `Unable to create process using "D:\Ai_agent\..."` | Stale venv paths | Recreate venv: `Remove-Item -Recurse -Force .\venv; python -m venv venv` |
| `Model gemini-2.5-flash not found` | API key doesn't have access | Change to `gemini-1.5-flash` in [agent.py:74](agent.py#L74) |
| `ModuleNotFoundError: agno` | Missing dependency | `python -m pip install agno` |
| `No API key` warning | Key not entered | Paste key in sidebar |
| Slow first response | Gemini cold start | Normal — subsequent calls are faster |

---

## 🔗 Related Files

- [agent.py](agent.py) — The full application
- [requirements.txt](requirements.txt) — Dependencies

---

*Last updated: 2026-06-05*
*This document was generated by reading the actual `agent.py` source line by line.*
