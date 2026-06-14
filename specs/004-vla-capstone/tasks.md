---
description: "Task list for Module 4 — Vision-Language-Action (VLA) Capstone"
---

# Tasks: Module 4 — Vision-Language-Action (VLA) Capstone

**Input**: Design documents from `/specs/004-vla-capstone/`
**Prerequisites**: spec.md ✅ | plan.md — not present (tasks derived directly from spec.md user stories)

**Tests**: No test tasks — content feature validated by Docusaurus build check, word-count checks, prohibited-term grep, and manual cross-reference verification (not TDD — no application logic to test-drive).

**Organization**: Tasks grouped by user story (P1 → P4, mapping to Chapters 13–16) to enable independent chapter authoring and validation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no shared dependencies)
- **[Story]**: Which user story this task belongs to (US1–US4)
- Exact file paths included in every task description

## Path Conventions

- Content: `frontend/docs/module-4/`
- Sidebar: `frontend/sidebars.ts`
- RagChatbot component: `frontend/src/components/RagChatbot.jsx` (already exists — do not modify)

---

## Phase 1: Setup

**Purpose**: Create the module-4 directory before any chapter files can be written.

- [x] T001 Create directory `frontend/docs/module-4/` — confirm it does not already exist, then run `mkdir -p frontend/docs/module-4/`

**Checkpoint**: `frontend/docs/module-4/` directory exists.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Verify shared infrastructure is intact before writing any chapter content.

**⚠️ CRITICAL**: No chapter can be build-verified until these pass.

- [x] T002 Verify `frontend/src/components/RagChatbot.jsx` has a valid default export — confirm file exists and exports a React component; if missing, create a minimal stub: `export default function RagChatbot({ context }) { return <div>RAG [{context}] — pending</div>; }`
- [x] T003 Verify `frontend/sidebars.ts` is syntactically valid and Module 1, 2, and 3 entries are intact — open `frontend/sidebars.ts` and confirm the file has exactly three category entries (Module 1, Module 2, Module 3) before any modification; do NOT edit it yet

**Checkpoint**: `RagChatbot.jsx` confirmed importable; `sidebars.ts` confirmed valid with 3 existing categories.

---

## Phase 3: User Story 1 — Chapter 13: The VLA Paradigm (Priority: P1) 🎯 MVP

**Goal**: Deliver a fully renderable Chapter 13 that permanently establishes the three-tier VLA architecture (Perception / Cognition / Action) and explains why classical isolated-loop pipelines are insufficient for open-ended humanoid tasks. A student who reads only this chapter can assign any named system component to its correct tier.

**Independent Test**: Open `http://localhost:3000` after `cd frontend && npm start`. Navigate to Chapter 13. Ask the student: "Where does the LLM's role end in a VLA pipeline?" — they must correctly identify that the LLM produces structured instructions consumed by the Action tier, not raw motor commands. A 5-question tier-matching quiz embedded or referenced in the chapter is verifiable independently.

### Implementation for User Story 1

- [x] T004 [US1] Write `frontend/docs/module-4/chapter-13-vla-convergence.mdx` with the following exact structure and content:

  **Frontmatter + import**:
  ```
  ---
  title: "Chapter 13 — The Vision-Language-Action Paradigm"
  ---

  import RagChatbot from '@site/src/components/RagChatbot';
  ```

  **H1**: `# Chapter 13 — The Vision-Language-Action Paradigm`

  **## Learning Objectives** (must be first H2):
  - 5 bullets: explain why classical isolated-loop robotics pipelines fail on open-ended tasks; identify the three tiers of a VLA architecture (Perception, Cognition, Action) and the data type that crosses each tier boundary; name at least two embodied foundation models (RT-2, PaLM-E) and contrast their multi-modal approaches; describe why separating the three tiers makes each independently debuggable; read a system block diagram and assign every component to the correct tier.

  **## The Limits of Classical Robotics Pipelines**:
  Open with a concrete failure scenario: a warehouse robot is programmed to "pick the red box from Shelf A." Classical isolated-loop design gives it: a vision module that detects the red box, a planning module that computes a grasp trajectory, and a control module that executes the arm motion. Each module is a separate program talking over fixed message queues. The scenario works — until a human moves the box to the floor, or the box is partially obscured, or the instruction changes mid-task to "actually, pick the blue box." In each case, the rigid coupling between modules forces a full pipeline restart, a hard-coded exception handler, or a human operator. The robot has no mechanism to reason about intent — it can only execute the pre-specified task. Use a `:::note` admonition: "This is not a failure of individual algorithms. Each module — the detector, the planner, the controller — may be technically excellent. The failure is architectural: three separate programs with no shared language for intent, context, or ambiguity."

  Detail three structural weaknesses of isolated-loop design: (1) **Fixed task vocabulary** — the planner can only handle tasks it was explicitly programmed for; "bring me the thing next to the lamp" is meaningless to a program that expects structured goal coordinates. (2) **Silent failure propagation** — if the vision module misidentifies the object, the planning module receives a confident but wrong goal and proceeds without awareness that the upstream input was incorrect. (3) **No replanning from natural language** — if a human says "stop, I changed my mind," the robot must halt completely; it cannot re-reason from the natural-language correction because no module in the pipeline processes language.

  **## The Three-Tier VLA Architecture**:
  Introduce VLA as the architectural response to classical pipeline limitations. The core insight: treat the robot's intelligence as three separable, independently debuggable tiers, each with a well-defined input type and output type. Present the three tiers as clearly labelled prose:

  - **Tier 1 — Perception**: Receives raw sensory input (audio bytes from a microphone, pixel arrays from cameras). Outputs a natural-language string. This is the tier that transforms the physical world into language the Cognition tier can reason about. The primary tool in this module is Whisper (for audio) and camera-based vision encoders (for visual input). Perception's output boundary: a clean natural-language string exits this tier.
  - **Tier 2 — Cognition**: Receives the natural-language string from Perception. Outputs a structured JSON array of primitive skill invocations. This is the tier where a Large Language Model acts as a reasoning engine — understanding the intent of the instruction, planning a multi-step response, and encoding that response as structured data the Action tier can execute. Cognition's output boundary: a validated JSON action array exits this tier.
  - **Tier 3 — Action**: Receives the JSON action array from Cognition. Outputs ROS 2 action calls — Nav2 navigation goals, MoveIt trajectory requests, gripper commands. This tier translates structured data back into physical robot motion. Action's output boundary: robot joint states and movements exit this tier.

  Include a tier-boundary diagram using a Docusaurus code block formatted as a text diagram:
  ```
  ┌──────────────────────────────────────────────────────────────┐
  │  Tier 1: PERCEPTION                                          │
  │  Input:  Raw audio bytes / camera pixels                     │
  │  Tool:   Whisper (audio) + Vision Encoder (visual)           │
  │  Output: Natural-language string ──────────────────────────► │
  └──────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ (natural-language string)
  ┌──────────────────────────────────────────────────────────────┐
  │  Tier 2: COGNITION                                           │
  │  Input:  Natural-language string                             │
  │  Tool:   Large Language Model (LLM)                          │
  │  Output: JSON action array ─────────────────────────────────►│
  └──────────────────────────────────────────────────────────────┘
                                    │
                                    ▼ (JSON action array)
  ┌──────────────────────────────────────────────────────────────┐
  │  Tier 3: ACTION                                              │
  │  Input:  JSON action array                                   │
  │  Tool:   ROS 2 Action Bridge → Nav2 / MoveIt / Grippers      │
  │  Output: Robot joint states and physical movement            │
  └──────────────────────────────────────────────────────────────┘
  ```

  Explain why tier separation is architecturally valuable: if the robot misexecutes a grasp, a developer can isolate the failure to one of three causes — did Perception produce the wrong string? Did Cognition produce a valid JSON plan for that string? Did Action execute the plan incorrectly? With isolated-loop architecture, the failure could be anywhere in an undifferentiated pile of code. With three-tier VLA, each tier has a testable contract.

  **## Embodied Foundation Models: RT-2 and PaLM-E**:
  Contrast two landmark embodied foundation models to show how the field has converged on multi-modal LLM-driven control:

  - **RT-2 (Robotics Transformer 2, Google DeepMind)**: A vision-language-action model that takes camera images and natural-language instructions as input and outputs robot control tokens directly. RT-2 is trained jointly on web-scale language and visual data alongside robot demonstration data. Its key characteristic: the model outputs low-level action tokens (motor commands) directly — it collapses the Cognition and Action tiers into one model. This enables impressive generalisation but makes the action component opaque and hard to debug; a developer cannot inspect the "plan" before it executes.
  - **PaLM-E (Google, 2023)**: A multi-modal language model that ingests text, images, and sensor readings as a unified sequence. PaLM-E separates language reasoning from motor execution — it reasons about what to do in natural language, then delegates the execution to lower-level controllers. This maps more naturally to the three-tier VLA architecture described above: PaLM-E occupies the Cognition tier, while perception and action remain distinct components.

  Draw the comparison clearly: RT-2 collapses tiers for end-to-end simplicity; PaLM-E separates cognition from action for debuggability. Neither is universally superior — the right architecture depends on the deployment environment, safety requirements, and team capability. Include a `:::tip` admonition: "In this textbook, the three-tier architecture is used because it matches the learning arc — each tier (Whisper in Chapter 14, LLM planning in Chapter 15, ROS 2 execution in Chapter 16) is independently teachable and independently inspectable."

  **## Why This Architecture Matters for Humanoid Robots**:
  Connect the three-tier model back to humanoid-specific requirements. A humanoid operating in a home or hospital must: (1) understand spoken commands from non-technical users — raw audio in, language understanding out (Perception tier); (2) convert a vague instruction like "help me clean up" into a specific, sequenced plan — natural language in, ordered action steps out (Cognition tier); (3) execute complex multi-step physical actions — action plan in, coordinated robot movement out (Action tier). The architecture is not just theoretically elegant — it is operationally necessary. A system that cannot decompose a vague instruction into specific steps will either refuse every ambiguous command or execute dangerous defaults. Include a `:::warning` admonition: "The Cognition tier does not have eyes — it reasons only from the string that Perception hands it. If Perception transcribes 'pick up the glass' as 'pick up the grass', Cognition will plan to interact with vegetation. Perception quality is the foundation of the entire system."

  **## Summary** (must be last H2 before component):
  4-sentence recap: (1) Classical isolated-loop robotics pipelines fail on open-ended tasks because they encode fixed task vocabularies and cannot reason about intent or recover from natural-language corrections. (2) The three-tier VLA architecture separates Perception (raw input → natural-language string), Cognition (string → JSON action plan), and Action (JSON → ROS 2 execution) as independently debuggable components with clear data-type contracts at each boundary. (3) Embodied foundation models RT-2 and PaLM-E illustrate the spectrum: RT-2 collapses tiers for simplicity, while PaLM-E's cognitive separation aligns with the debuggable three-tier model used in this textbook. (4) Chapters 14, 15, and 16 implement each tier in sequence — Whisper for Perception, an LLM cognitive planner for Cognition, and a ROS 2 Action Bridge for Action — building toward the complete capstone integration in Chapter 16.

  **Final line**: `<RagChatbot context="module-4" />`

- [x] T005 [US1] Run quality checks on `frontend/docs/module-4/chapter-13-vla-convergence.mdx`:
  - Word count: `wc -w frontend/docs/module-4/chapter-13-vla-convergence.mdx` — must be ≤ 4,500 total file words
  - Prohibited terms: `grep -in "neural network weights\|backpropagation\|gradient descent\|loss function\|softmax\|cross-entropy" frontend/docs/module-4/chapter-13-vla-convergence.mdx` — must return zero results
  - Tier boundary check: `grep -in "Perception\|Cognition\|Action" frontend/docs/module-4/chapter-13-vla-convergence.mdx` — must return multiple lines confirming all three tier names appear
  - RagChatbot check: `grep "RagChatbot" frontend/docs/module-4/chapter-13-vla-convergence.mdx` — must return exactly one line: `<RagChatbot context="module-4" />`
  - Confirm 5+ H2 sections and at least one `:::` admonition present in file

**Checkpoint**: Chapter 13 file passes all quality checks. Build check deferred to Phase 7.

---

## Phase 4: User Story 2 — Chapter 14: Voice-to-Action via Whisper (Priority: P2)

**Goal**: Deliver Chapter 14 that enables a student to trace the complete path of a spoken command — from raw audio bytes, through Whisper's transcription pipeline, to a clean natural-language string — without running any code. The chapter must identify at least two failure modes and explain how downstream tiers detect and recover from them.

**Independent Test**: After reading only Chapter 14, a student should be able to draw a block diagram of the audio ingestion pipeline and correctly label: (1) audio chunking, (2) spectrogram generation, (3) token decoding. The chapter's own block diagram serves as the answer key. A student who accesses the RAG chatbot with "how does Whisper handle background noise?" must receive a relevant excerpt.

### Implementation for User Story 2

- [x] T006 [P] [US2] Write `frontend/docs/module-4/chapter-14-voice-whisper.mdx` with the following exact structure and content:

  **Frontmatter + import**:
  ```
  ---
  title: "Chapter 14 — Voice-to-Action: Parsing Spoken Commands with Whisper"
  ---

  import RagChatbot from '@site/src/components/RagChatbot';
  ```

  **H1**: `# Chapter 14 — Voice-to-Action: Parsing Spoken Commands with Whisper`

  **## Learning Objectives** (first H2):
  - 5 bullets: describe what Whisper is and why it is suited for robotics voice interfaces; name the three stages that transform raw audio into a text string (audio chunking, spectrogram, token decoding); explain what data type exits the Perception tier (natural-language string, not audio bytes or JSON); identify at least two failure modes in voice transcription (background noise, homophone ambiguity) and describe how downstream tiers detect them; explain why voice is the primary human-robot interface in the capstone architecture.

  **## Why Voice is the Natural Human-Robot Interface**:
  Motivate the chapter with the interface design choice: a humanoid robot operating in a home, hospital, or warehouse must accept instructions from non-technical users. A touchscreen requires the user to be nearby; a mobile app requires the user to have the app installed and know how to use it; a keyboard is impractical for a user carrying items or in an emergency. Voice is the natural, hands-free, low-latency interface that requires no training and no hardware beyond a microphone. Frame Whisper as the mechanism that bridges the physical world (sound waves) and the digital world (text strings). Include a `:::note` admonition: "Whisper is an automatic speech recognition (ASR) model developed by OpenAI. It is trained on hundreds of thousands of hours of multilingual audio and is designed to be robust to diverse accents, speaking speeds, and acoustic environments — properties that make it suitable for deployment in variable real-world conditions."

  **## What Whisper Receives: Raw Audio Bytes**:
  Describe the physical signal: a microphone converts air pressure variations into an electrical signal, which is digitised into a stream of audio samples — typically 16,000 samples per second (16 kHz sampling rate), each represented as a signed integer. This raw stream is what the robot's software system receives. It has no inherent linguistic structure — it is a sequence of numbers representing air pressure at each millisecond. Whisper's job is to find the linguistic structure hidden in those numbers. Use the analogy: "Raw audio bytes are to Whisper what raw pixels are to a vision model. Just as a vision model sees intensity values at grid positions and infers objects, Whisper sees amplitude values at time positions and infers words."

  **## Stage 1 — Audio Chunking**:
  Explain that Whisper does not process an unlimited audio stream in one pass. Instead, it divides the audio into fixed-length windows — typically 30-second chunks. This is a practical engineering choice: processing smaller, bounded chunks limits memory usage and enables real-time transcription of long inputs. For robotics, this means a command longer than 30 seconds is handled in segments. Within each chunk, Whisper needs to convert the time-domain signal (amplitude over time) into a form that reveals frequency structure — which leads to the spectrogram stage. Include a `:::tip` admonition: "A 30-second audio chunk at 16 kHz = 480,000 audio samples. Even a short spoken command ('Bring me the red mug from the kitchen') takes only 3–4 seconds — well within one chunk."

  **## Stage 2 — Spectrogram Generation**:
  Describe the spectrogram transformation conceptually. Human speech is composed of multiple frequency components simultaneously — the vowel sound in "bring" has energy at different frequencies than the consonant sound in "b." A raw audio waveform (amplitude vs. time) shows *when* sounds occur but not *which frequencies* are present at each moment. A spectrogram is a different view of the same data: it shows *frequency vs. time*, with brightness indicating how much energy is present at each frequency at each instant. Whisper converts each 30-second audio chunk into an 80-channel log-mel spectrogram — a standardised representation that captures the frequency content of speech in a form suited to pattern matching. Do not describe the Fourier transform mathematically — instead, use this analogy: "Think of a spectrogram as a musical score for the sound. The score does not tell you the raw air pressure at every millisecond — it tells you which notes (frequencies) are being played at each point in time. Whisper reads this score and finds the word patterns within it."

  **## Stage 3 — Token Decoding**:
  Describe how Whisper produces a text string from the spectrogram. The model generates the transcript one token at a time — a token being a text segment (roughly a syllable or short word). At each step, the model predicts the most likely next token given all the spectrogram data and all the tokens generated so far. When the model predicts the end-of-sequence token, transcription is complete. The output is a UTF-8 text string — the natural-language representation of what the model believes was spoken. Reinforce the tier boundary: "The string that exits Stage 3 is what crosses the Perception-Cognition tier boundary. From this point forward, the system works with language, not audio." Include a `:::note` admonition: "Whisper's output is not annotated with confidence scores in its standard interface — it returns a string. Downstream systems must infer confidence from indirect signals (does the string parse into a valid command?) rather than from Whisper's internal probabilities."

  **## Failure Modes in the Perception Tier**:
  Identify two primary failure modes and explain how they propagate and are detected:

  **Failure Mode 1 — Background Noise**:
  In environments with competing audio sources (TV playing, machinery running, multiple people talking), Whisper may transcribe ambient sounds as words, or may fail to correctly identify a command word that is partially masked by noise. The failure is silent — Whisper still produces a string, but the string may be garbled or incomplete. Detection strategy: the Cognition tier (Chapter 15) validates that its JSON output conforms to a known schema. If the transcribed string is "bring me thum" instead of "bring me the mug", the LLM may produce a malformed or empty JSON array, which triggers the retry-with-feedback loop. The failure is discovered at the Cognition output boundary, not at the Perception stage.

  **Failure Mode 2 — Homophone Ambiguity**:
  English is full of homophones — words that sound identical but have different meanings ("bear" / "bare", "meet" / "meat", "to" / "two"). In a robotics context, "bring me the flower vase" and "bring me the flour base" could sound identical. Whisper selects the most probable interpretation based on linguistic context, but it cannot know the robot's physical environment — it has no visual context to disambiguate. Detection strategy: the Cognition tier may detect the ambiguity if the resulting action plan references objects that do not match the robot's known object list. The system can also use a visual confirmation step — the robot's camera checks whether the intended object is present before executing — but this is an Action tier responsibility, not a Perception tier responsibility.

  Use a `:::warning` admonition: "Neither failure mode is a defect in Whisper — they are inherent properties of speech as a communication channel. Robust voice interfaces always include downstream validation layers; the three-tier architecture exists precisely to catch these failures at well-defined boundaries."

  **## From Audio to String: A Complete Trace**:
  Synthesise the three stages into a single, numbered end-to-end trace using the example command "Bring me the red mug from the kitchen":
  1. Microphone captures 3.2 seconds of audio → 51,200 samples at 16 kHz
  2. Audio is packaged into a 30-second chunk (padded with silence to fill the window)
  3. The chunk is converted to an 80-channel log-mel spectrogram
  4. Whisper decodes the spectrogram token-by-token, generating the string: `"Bring me the red mug from the kitchen."`
  5. The string is passed to the Cognition tier (Chapter 15) as the sole input

  End with: "At step 5, the Perception tier's job is complete. No audio bytes cross the tier boundary — only the string. The Cognition tier never knows whether the instruction was spoken, typed, or received from a different source."

  **## Summary** (last H2):
  4-sentence recap: (1) Whisper transforms raw audio bytes into a natural-language string through three stages: audio chunking (dividing the stream into processable windows), spectrogram generation (converting amplitude-over-time into frequency-over-time), and token decoding (predicting the transcript word by word). (2) The string that exits Whisper is the sole input to the Cognition tier — the Perception-Cognition tier boundary is a clean data-type handoff, not a shared system. (3) Two primary failure modes — background noise and homophone ambiguity — produce plausible-looking but incorrect strings; detection and recovery happen at the Cognition tier output boundary, not at the Perception stage. (4) Chapter 15 takes this string and shows how an LLM breaks it down into a structured JSON action plan that the robot can execute.

  **Final line**: `<RagChatbot context="module-4" />`

- [x] T007 [US2] Run quality checks on `frontend/docs/module-4/chapter-14-voice-whisper.mdx`:
  - Word count: `wc -w frontend/docs/module-4/chapter-14-voice-whisper.mdx` — must be ≤ 4,500 total words
  - Stage headings check: `grep -n "## Stage" frontend/docs/module-4/chapter-14-voice-whisper.mdx` — must return 3 lines (Stages 1, 2, and 3)
  - Failure modes check: `grep -in "Failure Mode" frontend/docs/module-4/chapter-14-voice-whisper.mdx` — must return at least 2 results
  - Prohibited math terms: `grep -in "fourier transform\|FFT\|matrix\|neural network weights" frontend/docs/module-4/chapter-14-voice-whisper.mdx` — zero results
  - RagChatbot context check: `grep "context=" frontend/docs/module-4/chapter-14-voice-whisper.mdx` — must return `context="module-4"`

**Checkpoint**: Chapter 14 contains Stage 1/2/3 as standalone H2 sections, two named failure modes, and passes all quality checks.

---

## Phase 5: User Story 3 — Chapter 15: Cognitive LLM Planning (Priority: P3)

**Goal**: Deliver Chapter 15 that teaches prompt engineering for structured output using a concrete worked example, defines the minimal JSON action schema (`skill`, `target`, `parameters`), and shows the retry-with-feedback loop. A student who reads only Chapters 13–15 can produce a valid JSON action array for a novel command without reading Chapter 16.

**Independent Test**: Present a student with the novel command "Bring me a glass of water." After reading Chapter 15, they can produce a 3–5 step JSON action array using the schema (`skill`, `target`, `parameters`) referencing `navigate_to`, `grasp`, and `return_to` primitives. The worked example in the chapter is self-contained enough to serve as the answer key.

### Implementation for User Story 3

- [x] T008 [P] [US3] Write `frontend/docs/module-4/chapter-15-cognitive-llm-planning.mdx` with the following exact structure and content:

  **Frontmatter + import**:
  ```
  ---
  title: "Chapter 15 — Cognitive LLM Planning: From Language to Executable JSON"
  ---

  import RagChatbot from '@site/src/components/RagChatbot';
  ```

  **H1**: `# Chapter 15 — Cognitive LLM Planning: From Language to Executable JSON`

  **## Learning Objectives** (first H2):
  - 5 bullets: explain the role of the Cognition tier in the three-tier VLA architecture; design a system prompt that includes a role definition, schema injection, and output-format constraint; trace a high-level command through the LLM decomposition process to a complete JSON action array; identify the three fields of the minimal JSON action schema (`skill`, `target`, `parameters`); describe the retry-with-feedback loop for recovering from malformed LLM output.

  **## The Cognition Tier's Role: From Vague to Executable**:
  Open with the problem: the Perception tier (Chapter 14) hands the Cognition tier a natural-language string. That string might be "Clean the room." It might be "Help me." It might be "The thing by the window." None of these are directly executable by a robot — they are intent descriptions, not instructions. The Cognition tier's job is to take that intent description and produce a precisely structured action plan that the Action tier can execute without further interpretation. The tool for this is a Large Language Model, prompted with careful instructions that constrain its output to a machine-readable format.

  Use a `:::note` admonition: "The LLM in the Cognition tier is not controlling the robot directly. It is reasoning about what should be done and encoding that reasoning as data. The Action tier is what actually sends commands to the robot. This separation is deliberate: it lets you swap the LLM for a different model, upgrade it, or add safety filters — all without touching the Action tier."

  **## Prompt Engineering for Structured Output**:
  Introduce the three components of a structured-output system prompt:

  **### Component 1 — Role Definition**:
  The system prompt begins by telling the LLM what it is and what it is responsible for. This scopes its reasoning. Example: "You are a robot task planner for a humanoid robot assistant. Your job is to translate high-level human instructions into an ordered sequence of primitive robot skills. You must not generate explanations, questions, or commentary — only the JSON action array." Explain why role definition matters: an LLM without role context may generate conversational responses ("That sounds like a great idea! Here is how the robot might approach...") rather than structured output. The role definition primes the model to behave as a planning engine, not a conversational assistant.

  **### Component 2 — Schema Injection**:
  The system prompt provides the exact structure the LLM must produce. Define the minimal JSON action schema:
  ```json
  {
    "skill": "string — the name of a primitive robot skill (e.g., navigate_to, grasp, place, return_to)",
    "target": "string — the object or location the skill acts on",
    "parameters": "object — optional key-value pairs for skill configuration"
  }
  ```
  The full response must be a JSON array where each element conforms to this schema. The schema is injected directly into the system prompt so the model has it available at every inference step. Explain the available primitive skills: `navigate_to` (move to a location), `grasp` (pick up an object), `place` (put an object down at a target), `return_to` (navigate back to a home or previous position), `wait` (pause for a specified duration), `scan` (survey the environment for a target object).

  **### Component 3 — Output-Format Constraint**:
  The system prompt explicitly forbids non-JSON output: "Your response MUST be a valid JSON array. Do not include any text outside the JSON array. Do not use markdown code fences. Do not add explanations." This constraint is necessary because LLMs default to generating human-readable text. Without an explicit constraint, the model may wrap its JSON in explanatory prose ("Here is the plan:"), which breaks downstream JSON parsing. Include a `:::warning` admonition: "Even with an explicit output-format constraint, LLMs occasionally produce malformed JSON — a missing bracket, an extra comma, an unescaped character. This is not a failure of the approach; it is a known property of probabilistic text generation. The retry-with-feedback loop (described later in this chapter) handles it."

  **## A Complete Worked Example**:
  **(MANDATORY standalone H2 — do not nest inside another section)**

  Present the full decomposition of one command, step by step:

  **Input command (from Perception tier)**: `"Clean the room."`

  **Step 1 — Intent decomposition (LLM reasoning, not part of output)**:
  "Clean the room" implies: identifying objects that are out of place, moving each to its correct location, and returning to a neutral position. Decompose into discrete steps: scan the environment to identify items on the floor, navigate to each item, pick it up, place it in the correct location, repeat, then return to home position.

  **Step 2 — JSON output (the actual LLM response)**:
  ```json
  [
    {
      "skill": "scan",
      "target": "room",
      "parameters": { "mode": "floor_items" }
    },
    {
      "skill": "navigate_to",
      "target": "item_1",
      "parameters": {}
    },
    {
      "skill": "grasp",
      "target": "item_1",
      "parameters": { "grip_type": "pinch" }
    },
    {
      "skill": "place",
      "target": "item_1_home_location",
      "parameters": {}
    },
    {
      "skill": "return_to",
      "target": "home_position",
      "parameters": {}
    }
  ]
  ```

  **Step 3 — Validation**:
  The Action tier's JSON parser validates: (1) the response is a valid JSON array; (2) each element contains `skill`, `target`, and `parameters` keys; (3) the `skill` value is a recognised primitive (not a made-up skill name). All three checks pass — the plan is forwarded to the Action tier for execution.

  Follow the worked example with: "Notice what the JSON array does NOT contain: no motor torques, no joint angles, no ROS 2 topic names. The Cognition tier works entirely in the language of high-level intent. The Action tier (Chapter 16) translates each skill into the specific hardware commands required to execute it."

  **## The Retry-with-Feedback Loop**:
  Describe the recovery mechanism for malformed JSON output using a text-based flowchart:

  ```
  LLM generates response
          │
          ▼
  JSON parser validates response
          │
    ┌─────┴─────┐
   VALID      INVALID
    │              │
    ▼              ▼
  Forward to   Append error to LLM context:
  Action tier  "Your previous response was invalid JSON.
                Error: [parser error message].
                Please regenerate the JSON array only."
                   │
                   ▼
              LLM regenerates response
                   │
                   ▼
           (retry validation, max 3 attempts)
                   │
              if still INVALID after 3 attempts:
                   │
                   ▼
         Log failure, return error to user:
         "I could not understand that instruction.
          Please rephrase."
  ```

  Explain the design rationale: the error message fed back to the LLM includes the specific parse error (e.g., "Unexpected token '}' at position 47") so the model has precise information to correct. Simply saying "invalid" gives the model no information to act on. The 3-attempt cap prevents infinite loops. The human-readable failure message maintains a safe user experience — the robot does not silently fail or execute a partially-parsed plan.

  **## Why the Cognition Tier Cannot Be Simpler**:
  Address the natural question: "Why not hard-code a list of command → JSON mappings?" Explain three limitations of a lookup-table approach: (1) **Vocabulary explosion** — the number of valid natural-language commands for a humanoid robot is effectively infinite; a lookup table that covers all variations of "bring me X" ("fetch X", "get X", "grab X", "can you get X", "I need X") would require thousands of entries and would still miss novel phrasings. (2) **Context insensitivity** — a table cannot handle "bring me the other one" because "the other one" has no fixed referent; it requires reasoning about conversational context. (3) **Compositional commands** — "clean the living room and then bring me tea" is a multi-step command that requires decomposition into a sequential plan; no lookup table can decompose compound instructions into ordered action sequences.

  Include a `:::tip` admonition: "The LLM does not need to be large to perform well in the Cognition tier. The task — structured decomposition of short commands into 3–8 step action arrays — is a well-defined, narrow reasoning task. A small, instruction-tuned model (7B–13B parameters) fine-tuned on action sequence data can outperform a general-purpose large model for this specific role."

  **## Summary** (last H2):
  4-sentence recap: (1) The Cognition tier uses a Large Language Model prompted with three components — role definition, schema injection, and output-format constraint — to decompose high-level natural-language commands into ordered JSON action arrays conforming to the `skill`/`target`/`parameters` schema. (2) The minimal action schema (`skill`, `target`, `parameters`) defines the contract between the Cognition and Action tiers: the LLM never references motor hardware, and the Action tier never parses natural language. (3) The retry-with-feedback loop handles the inevitable cases of malformed LLM output by feeding the specific parse error back to the model for correction, with a 3-attempt cap and a human-readable failure message. (4) Chapter 16 wires the Cognition tier's JSON output to the ROS 2 Action Bridge and shows how each primitive skill maps to a Nav2 goal or MoveIt trajectory in the complete capstone system.

  **Final line**: `<RagChatbot context="module-4" />`

- [x] T009 [US3] Run quality checks on `frontend/docs/module-4/chapter-15-cognitive-llm-planning.mdx`:
  - Word count: `wc -w frontend/docs/module-4/chapter-15-cognitive-llm-planning.mdx` — must be ≤ 4,500 total words
  - Mandatory worked example check: `grep -n "## A Complete Worked Example" frontend/docs/module-4/chapter-15-cognitive-llm-planning.mdx` — must return exactly one line
  - JSON schema check: `grep -n '"skill"' frontend/docs/module-4/chapter-15-cognitive-llm-planning.mdx` — must return multiple lines (schema definition + worked example)
  - Retry loop check: `grep -in "retry\|feedback loop" frontend/docs/module-4/chapter-15-cognitive-llm-planning.mdx` — must return at least 3 results
  - Prohibited terms: `grep -in "gradient\|backpropagation\|loss function\|neural network weights" frontend/docs/module-4/chapter-15-cognitive-llm-planning.mdx` — zero results
  - RagChatbot context check: `grep "context=" frontend/docs/module-4/chapter-15-cognitive-llm-planning.mdx` — must return `context="module-4"`

**Checkpoint**: Chapter 15 contains the mandatory worked example H2, the JSON schema with `skill`/`target`/`parameters` fields, the retry flowchart, and passes all quality checks.

---

## Phase 6: User Story 4 — Chapter 16: Capstone: Autonomous Humanoid (Priority: P4)

**Goal**: Deliver Chapter 16 that embeds the Mermaid pipeline diagram, contains explicit cross-references to all three prior modules (Module 1 Chapter 2, Module 2 Chapters 5–8, Module 3 Chapter 12), presents a numbered capstone assembly blueprint, and describes the ROS 2 Action Bridge interface in full. A student with all four modules read can walk through the Mermaid diagram and name the specific chapter where each node was introduced.

**Independent Test**: A student who reads Chapter 16 before reading Chapters 13–15 must still be able to navigate the integration map, because the chapter includes a brief recap paragraph at the start and numbered cross-references to earlier chapters. Verify manually that the Mermaid diagram renders in the local dev server and that the surrounding prose is sufficient to understand the pipeline without the diagram.

### Implementation for User Story 4

- [x] T010 [US4] Write `frontend/docs/module-4/chapter-16-capstone-autonomous-humanoid.mdx` with the following exact structure and content:

  **Frontmatter + import**:
  ```
  ---
  title: "Chapter 16 — Capstone: Building an Autonomous Humanoid"
  ---

  import RagChatbot from '@site/src/components/RagChatbot';
  ```

  **H1**: `# Chapter 16 — Capstone: Building an Autonomous Humanoid`

  **## Non-Linear Reading Note** (second section, immediately after H1, before Learning Objectives):
  A brief paragraph for students who arrive at this chapter without completing the previous chapters: "This chapter is the integration capstone for the entire textbook. Each section references specific earlier chapters where the building blocks were introduced. If you have not read the prior chapters, the cross-references will guide you to the relevant context. The Mermaid pipeline diagram below and the surrounding prose are written to be understandable in both reading orders."

  **## Learning Objectives** (first H2 after the non-linear note):
  - 5 bullets: trace the complete system from voice input to robot movement through the five-node pipeline (Voice → Whisper → LLM → ROS 2 Bridge → Nav2 / Motor); identify which prior module and chapter introduced each pipeline component; explain the ROS 2 Action Bridge interface — how it consumes the JSON action array and maps each skill to a Nav2 goal or MoveIt trajectory; describe how the LLM receives feedback from the Action tier for replanning; articulate why the capstone architecture is a synthesis of all four modules, not an extension of Module 4 alone.

  **## The Full System Pipeline**:
  Open with the integration framing: this chapter assembles the components from all four modules into a single coherent system. Briefly recap each module's contribution (one sentence each): Module 1 introduced ROS 2 as the communication backbone — topics, nodes, and the pub/sub architecture that wires the components together (Chapter 2). Module 2 introduced Gazebo and Isaac Sim as the digital twin environments where the complete system can be tested without hardware risk (Chapters 5–8). Module 3 introduced Nav2 and the perception stack that gives the robot its spatial awareness (Chapter 12). Module 4 (Chapters 13–15) introduced the three-tier VLA architecture: Whisper for Perception, the LLM for Cognition, and the ROS 2 Action Bridge for Action.

  **## The Pipeline Diagram**:
  **(MANDATORY standalone H2 — do not nest inside another section)**

  Present the Mermaid diagram:

  ```mdx
  ```mermaid
  graph LR
      A["🎤 Voice Input<br/>(Microphone)"] --> B["Whisper ASR<br/>(Perception Tier)"]
      C["📷 Vision Input<br/>(Stereo Camera)"] --> D["Vision Encoder<br/>(Perception Tier)"]
      B --> E["LLM Cognitive Planner<br/>(Cognition Tier)"]
      D --> E
      E --> F["ROS 2 Action Bridge<br/>(Action Tier)"]
      F --> G["Nav2 Path Planner<br/>(Module 3 / Ch.12)"]
      F --> H["MoveIt Arm Controller<br/>(Action Tier)"]
      G --> I["🦿 Motor Commands<br/>(Robot Execution)"]
      H --> I
      I -.->|"Feedback: execution status"| E
  ```
  ```

  Follow the diagram immediately with a node-by-node text description (so the pipeline is understandable without the diagram if rendering fails):
  - **Voice Input (Microphone)**: The human's spoken command enters the system as raw audio bytes.
  - **Whisper ASR (Perception Tier)**: Introduced in Chapter 14. Converts audio to a natural-language string.
  - **Vision Input (Stereo Camera)**: The robot's camera provides visual context — object positions, room layout.
  - **Vision Encoder (Perception Tier)**: Converts the camera feed into a visual representation consumed by the LLM alongside the text string.
  - **LLM Cognitive Planner (Cognition Tier)**: Introduced in Chapter 15. Receives the text string and visual context, produces a JSON action array.
  - **ROS 2 Action Bridge (Action Tier)**: The focus of this chapter. Consumes the JSON array and translates each skill into ROS 2 action calls.
  - **Nav2 Path Planner (Module 3 / Chapter 12)**: Cross-reference to Module 3. Receives navigation goals from the Action Bridge, plans footstep sequences.
  - **MoveIt Arm Controller**: Receives manipulation goals from the Action Bridge, plans arm trajectories.
  - **Motor Commands**: The physical output — joint torques and positions that make the robot move.
  - **Feedback (dashed arrow)**: Execution status is returned from the motor layer back to the LLM for replanning if a skill fails.

  **## The ROS 2 Action Bridge**:
  Describe the Action Bridge as the component that translates the LLM's JSON output into concrete ROS 2 calls. It performs three functions:

  **### JSON Parsing and Validation**: The bridge receives the JSON action array from the Cognition tier. It parses the array and validates each element against the schema (`skill`, `target`, `parameters`). Invalid elements trigger the retry-with-feedback loop from Chapter 15. Valid arrays proceed to execution.

  **### Skill Dispatch**: For each element in the array, the bridge maps the `skill` field to a specific ROS 2 interface. The dispatch table:
  - `navigate_to` → sends a `NavigateToPose` action goal to Nav2 (see Module 3, Chapter 12 for Nav2's bipedal planning)
  - `grasp` → sends a `MoveGroup` goal to MoveIt with the target object's pose
  - `place` → sends a `MoveGroup` goal with a release pose at the target location
  - `return_to` → sends a `NavigateToPose` goal to the robot's home or previously saved position
  - `scan` → triggers a point-cloud sweep and an object detection inference pass
  - `wait` → pauses execution for the duration specified in `parameters.duration`

  **### Feedback Collection**: After each skill executes, Nav2 and MoveIt return completion status (succeeded, failed, preempted). The bridge aggregates these statuses and, if a skill fails, feeds the failure context back to the LLM: "Skill `grasp(red_mug)` failed: object not found at expected position. Please regenerate the plan." The LLM then produces a revised JSON array. This closes the feedback loop shown by the dashed arrow in the pipeline diagram.

  **## Cross-Module Integration References**:
  **(MANDATORY standalone H2 — contains the three numbered cross-references required by FR-013)**

  Present three numbered integration points:

  **1. Module 1, Chapter 2 — ROS 2 Topics and Nodes**:
  Every communication link in the pipeline diagram is a ROS 2 topic, service, or action. The ROS 2 Action Bridge is itself a ROS 2 node — it subscribes to a topic that carries the JSON action array and publishes to the `NavigateToPose` and `MoveGroup` action servers. Chapter 2 introduced the pub/sub node architecture; the capstone system is a direct application of that architecture at scale. Students who completed Module 1 will recognise the `/cmd_vel`, `/goal_pose`, and `/joint_states` topics as the same interfaces they first encountered in Chapter 2.

  **2. Module 2, Chapters 5–8 — Gazebo and Isaac Sim as Test Environments**:
  The complete capstone system — all five pipeline nodes — can be deployed inside the Gazebo or Isaac Sim digital twin environments introduced in Module 2. Testing in simulation before hardware deployment is not optional: a bug in the Action Bridge that sends an invalid MoveIt goal could cause a physical robot arm to move unsafely. Chapters 5 (Gazebo physics) and 8 (sensor simulation) introduced the environments where such failures can be caught safely. In the capstone simulation, Gazebo provides the physics engine that executes Nav2's footstep plans and simulates the arm movements MoveIt commands.

  **3. Module 3, Chapter 12 — Nav2 Bipedal Path Planning**:
  The `navigate_to` and `return_to` skills in the JSON action schema are fulfilled by Nav2 — the same navigation middleware introduced in Chapter 12. Nav2 receives a `NavigateToPose` goal from the ROS 2 Action Bridge and produces a footstep plan that respects the three bipedal constraints (centre-of-mass stability, footstep placement, gait cycle timing) described in Chapter 12. Students who completed Module 3 can trace the complete path from "LLM decides to navigate to the kitchen" → "ROS 2 Action Bridge sends NavigateToPose goal" → "Nav2 plans a footstep sequence respecting balance constraints" → "motor controller executes each step."

  **## Capstone Assembly Blueprint**:
  **(MANDATORY standalone H2 — numbered assembly sequence)**

  Present a step-by-step numbered walkthrough of how the complete system processes a single command, "Bring me the red mug from the kitchen":

  1. **Voice capture**: The microphone records the spoken command. Raw audio bytes are streamed to the Whisper ASR node.
  2. **Whisper transcription (Perception tier)**: Whisper processes the audio through chunking, spectrogram generation, and token decoding. Output: `"Bring me the red mug from the kitchen."` — a clean natural-language string passed to the LLM node.
  3. **Visual context capture (Perception tier)**: The stereo camera captures the current scene. The vision encoder converts the camera feed into a visual context representation fed to the LLM alongside the text.
  4. **LLM planning (Cognition tier)**: The LLM receives the text string and visual context. Using the system prompt (role definition, schema injection, output-format constraint), it generates a JSON action array: `[navigate_to(kitchen), scan(red_mug), navigate_to(red_mug), grasp(red_mug), return_to(user_position), place(red_mug, user_table)]`.
  5. **JSON validation (Action Bridge)**: The ROS 2 Action Bridge parses and validates the JSON array. All elements conform to the schema. Execution begins.
  6. **Navigation to kitchen (Action Bridge → Nav2)**: The bridge sends a `NavigateToPose` goal to Nav2. Nav2 plans a footstep sequence to the kitchen respecting bipedal stability constraints (Module 3, Chapter 12). The motor controller executes the steps.
  7. **Object scan**: The bridge triggers a point-cloud sweep. The vision system identifies the red mug at position `(x: 1.2, y: 0.3, z: 0.8)` relative to the robot.
  8. **Navigation to mug and grasp**: The bridge sends a `NavigateToPose` goal to the mug's position, followed by a `MoveGroup` goal to MoveIt for the grasp. The arm moves to the mug and closes the gripper.
  9. **Return and place**: The bridge sends `NavigateToPose` to the user's position and `MoveGroup` to release the mug on the table.
  10. **Completion and feedback**: Each action returns a `succeeded` status. The bridge aggregates results and sends a completion message. The LLM receives: "All actions succeeded." The task is complete.

  Include a `:::note` admonition: "Steps 6–9 happen sequentially — the robot completes each skill before the bridge dispatches the next. This sequential execution model is the default; parallel skill execution (e.g., moving the arm while walking) requires additional coordination logic in the Action Bridge beyond this capstone scope."

  **## Summary** (last H2):
  4-sentence recap: (1) The capstone system assembles all four modules: ROS 2 communication backbone from Module 1, digital twin simulation from Module 2, Nav2 bipedal navigation from Module 3, and the three-tier VLA architecture from Module 4 — Whisper for Perception, the LLM for Cognition, and the ROS 2 Action Bridge for Action. (2) The ROS 2 Action Bridge is the integration keystone: it translates the Cognition tier's JSON action array into concrete ROS 2 action calls, dispatches them to Nav2 and MoveIt, and feeds execution status back to the LLM for replanning. (3) The capstone blueprint for "Bring me the red mug from the kitchen" demonstrates all 10 steps of the end-to-end pipeline — from microphone capture through bipedal navigation, arm grasping, and return — as an inspectable, tier-by-tier trace. (4) With Chapter 16 complete, the textbook has delivered a complete conceptual framework for building autonomous humanoid systems: the nervous system, the digital twin, the AI brain, and the voice-driven action pipeline — a foundation for the next generation of Physical AI.

  **Final line**: `<RagChatbot context="module-4" />`

- [x] T011 [US4] Run quality checks on `frontend/docs/module-4/chapter-16-capstone-autonomous-humanoid.mdx`:
  - Word count: `wc -w frontend/docs/module-4/chapter-16-capstone-autonomous-humanoid.mdx` — must be ≤ 5,000 total words (longer than other chapters due to integration scope)
  - Mermaid diagram check: `grep -n "mermaid" frontend/docs/module-4/chapter-16-capstone-autonomous-humanoid.mdx` — must return at least 2 lines (opening and closing fences)
  - Cross-reference check: `grep -in "Module 1\|Module 2\|Module 3" frontend/docs/module-4/chapter-16-capstone-autonomous-humanoid.mdx` — must return at least 3 lines, one per prior module
  - Pipeline diagram H2 check: `grep -n "## The Pipeline Diagram" frontend/docs/module-4/chapter-16-capstone-autonomous-humanoid.mdx` — must return exactly one line
  - Capstone blueprint H2 check: `grep -n "## Capstone Assembly Blueprint" frontend/docs/module-4/chapter-16-capstone-autonomous-humanoid.mdx` — must return exactly one line
  - Integration references H2 check: `grep -n "## Cross-Module Integration References" frontend/docs/module-4/chapter-16-capstone-autonomous-humanoid.mdx` — must return exactly one line
  - RagChatbot context check: `grep "context=" frontend/docs/module-4/chapter-16-capstone-autonomous-humanoid.mdx` — must return `context="module-4"`

**Checkpoint**: Chapter 16 contains the Mermaid diagram, three cross-module references, the capstone assembly blueprint, and passes all quality checks.

---

## Phase 7: Navigation Integration & Verification

**Purpose**: Wire all four chapters into the sidebar, run quality sweeps, and verify the complete Module 4 experience end-to-end.

- [x] T012 Update `frontend/sidebars.ts` — open the file and append the following category object as the fourth entry in the `tutorialSidebar` array, after the Module 3 category closing brace:
  ```typescript
  {
    type: 'category',
    label: 'Module 4: Vision-Language-Action',
    collapsed: false,
    items: [
      'module-4/chapter-13-vla-convergence',
      'module-4/chapter-14-voice-whisper',
      'module-4/chapter-15-cognitive-llm-planning',
      'module-4/chapter-16-capstone-autonomous-humanoid',
    ],
  },
  ```
  Verify the existing Module 1, Module 2, and Module 3 entries are unchanged.

- [x] T013 [P] Run cross-chapter quality sweep:
  - `grep -rh "RagChatbot" frontend/docs/module-4/` — must return exactly 4 lines, each `<RagChatbot context="module-4" />`
  - `grep -rin "neural network weights\|backpropagation\|gradient descent\|fourier transform formula" frontend/docs/module-4/` — zero results
  - `grep -n "## " frontend/docs/module-4/chapter-13-vla-convergence.mdx` — confirm 5+ H2 sections
  - `grep -n "## A Complete Worked Example" frontend/docs/module-4/chapter-15-cognitive-llm-planning.mdx` — confirm line exists
  - `grep -n "## The Pipeline Diagram" frontend/docs/module-4/chapter-16-capstone-autonomous-humanoid.mdx` — confirm line exists
  - `grep -n "## Capstone Assembly Blueprint" frontend/docs/module-4/chapter-16-capstone-autonomous-humanoid.mdx` — confirm line exists

- [x] T014 Run the Docusaurus production build: `cd frontend && npm run build` — must complete with zero errors; any build error reveals a broken import, malformed MDX, or invalid sidebar entry; the Mermaid diagram in Chapter 16 must not cause a build failure

- [x] T015 Start the local dev server: `cd frontend && npm start` — navigate to `http://localhost:3000`; verify:
  - "Module 4: Vision-Language-Action" appears in the left sidebar
  - All four chapter links are visible and navigable (Chapters 13–16)
  - The Mermaid diagram in Chapter 16 renders correctly
  - The RagChatbot stub appears at the bottom of each chapter page
  - Module 1, Module 2, and Module 3 sidebar entries are unchanged and in correct order

**Checkpoint — Definition of Done**:
- `frontend/docs/module-4/` contains exactly 4 `.mdx` files
- `frontend/sidebars.ts` has exactly 4 category entries
- `npm run build` exits with code 0
- All four chapters visible and navigable in local dev server
- Mermaid diagram in Chapter 16 renders without error
- Cross-chapter quality sweep passes all grep checks

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all chapter work
- **US1 Chapter 13 (Phase 3)**: Depends on Phase 2
- **US2 Chapter 14 (Phase 4)**: Depends on Phase 2; can run in parallel with Phase 3
- **US3 Chapter 15 (Phase 5)**: Depends on Phase 2; can run in parallel with Phases 3 and 4
- **US4 Chapter 16 (Phase 6)**: Should be written after Chapters 13–15 are drafted, since it references their content in cross-references and the capstone blueprint
- **Navigation + Verification (Phase 7)**: Depends on all four chapters being complete

### User Story Dependencies

- **US1 (P1, Chapter 13)**: No story dependencies — can start after Phase 2
- **US2 (P2, Chapter 14)**: No story dependencies — can start after Phase 2 in parallel with US1
- **US3 (P3, Chapter 15)**: No story dependencies — can start after Phase 2 in parallel with US1/US2
- **US4 (P4, Chapter 16)**: Should be written after US1–US3 are drafted, since it contains explicit cross-references to content defined in Chapters 13–15

### Within Each Story

- Write content task (T004/T006/T008/T010) → then quality-check task (T005/T007/T009/T011)
- Quality check must pass before the chapter is considered story-complete

### Parallel Opportunities

- T006 (Ch14) and T008 (Ch15) can be written in parallel with T004 (Ch13) — different files, no shared dependencies
- T013 (cross-chapter grep sweep) and T012 (sidebar update) can begin as soon as all four chapter files are complete
- T014 (build) must follow T012 and T013

---

## Parallel Example: Content Writing Sprint

```bash
# After Phase 2 completes, all three of these can start simultaneously:
Task T004: Write chapter-13-vla-convergence.mdx
Task T006: Write chapter-14-voice-whisper.mdx
Task T008: Write chapter-15-cognitive-llm-planning.mdx

# After those are drafted:
Task T010: Write chapter-16-capstone-autonomous-humanoid.mdx (references all above)

# After all four chapters exist:
Task T012: Update sidebars.ts
Task T013: Run cross-chapter quality sweep [P with T012]
Task T014: Run npm run build (depends on T012)
Task T015: Manual dev-server verification (depends on T014)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only — Chapter 13)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3 (T004 + T005): Chapter 13 only
4. Add Chapter 13 alone to `sidebars.ts` temporarily and run `npm run build`
5. **STOP and VALIDATE**: Chapter 13 renders, three-tier diagram visible, RagChatbot stub at bottom, no build errors
6. Proceed to remaining chapters

### Full Delivery Order (Priority Sequence)

1. Phase 1 + Phase 2 → Foundation ready
2. Phase 3 (Ch13) → VLA architecture foundation complete (MVP)
3. Phase 4 (Ch14) → Whisper Perception tier complete
4. Phase 5 (Ch15) → Cognition LLM planning complete; worked example self-contained
5. Phase 6 (Ch16) → Full capstone integration complete; Mermaid diagram and cross-references verified
6. Phase 7 → Build verified, sidebar live, Module 4 shipped; textbook complete

---

## Notes

- No new React components required — `RagChatbot.jsx` already exists from prior modules
- Sidebar file is `frontend/sidebars.ts` (TypeScript) — NOT `sidebars.js`
- Content goes in `frontend/docs/module-4/` — NOT `docs/module-4/` at repo root
- Each chapter must have `import RagChatbot from '@site/src/components/RagChatbot';` as line 1 after frontmatter
- `## A Complete Worked Example` in Chapter 15 MUST be a standalone H2 (not nested inside another section) — required for RAG chunk isolation
- `## The Pipeline Diagram` in Chapter 16 MUST be a standalone H2 (not nested) — required for RAG chunk isolation
- Chapter 16's Mermaid diagram uses the `graph LR` layout; the node labels include emoji for visual clarity in the rendered output
- The JSON action schema uses exactly three fields: `skill`, `target`, `parameters` — do not add fields (consistency with Chapter 16's Action Bridge description)
- Chapter 16 cross-references: Module 1 Ch.2, Module 2 Ch.5–8, Module 3 Ch.12 — all three are required for SC-004
- Prohibited in all chapters: neural network weights, backpropagation, gradient descent, loss functions, Jacobians, covariance matrices, pseudocode
