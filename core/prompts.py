"""
Centralized prompt storage for Agno Agent.
"""

# --- Agent Instructions ---
DEFAULT_AGENT_INSTRUCTIONS = [
    "Bạn là một trợ lý AI giúp tôi giải quyết thắc mắc"
]

# --- Training Prompts ---
INITIAL_TRAINING_PROMPT = """Bạn là một trợ lý AI giúp tôi giải quyết thắc mắc"""

# --- Grading Prompts ---
GRADER_AGENT_INSTRUCTIONS = [
    "Evaluate the agent response against the ground truth and return only a numerical score between 0.0 and 1.0."
]

GRADING_PROMPT_TEMPLATE = """
### ROLE
You are an expert evaluator. Grade the AGENT RESPONSE against the USER QUESTION.

### CONTEXT
User Question: {question}
Agent Response: {agent_response}

### GRADING CRITERIA (0.0 to 1.0)
- 1.0: Perfect. The response is accurate, helpful, and completely answers the user's question.
- 0.8-0.9: Correct info but could be more concise or better phrased.
- 0.5-0.7: Partially correct. Got the main idea but missed some details, made minor errors, or didn't fully address all parts of the question.
- 0.0-0.4: Wrong, irrelevant, or fails to address the question.

### OUTPUT FORMAT
Respond with ONLY the numerical score (e.g., "0.8"). No explanation.
"""
# Gradient computed with gpt-4o-mini has result: ## Critique of the Prompt

# ### 1. Structural Issues
# - **Missing goal**: The prompt does not clearly define the overall goal. While the task is to assist with math problems, it lacks a summarizable output goal that conveys what "success" looks like.
  
# ### 2. Instruction Quality
# - **Vague verbs**: Phrases like "be accurate and precise" are too vague without specifying what accuracy or precision means in context. More concrete instructions are needed.
# - **Lack of hierarchy**: All instructions appear equal, which makes it unclear whether it is more important to show work or to provide a final answer. Establishing precedence could clarify this.
# - **Mixed abstraction**: The request to "show your work" intermixed with "provide the final answer clearly" complicates the structure, blending high-level goals with detailed steps. Clear separation is needed.
  
# ### 3. Control and Behavior
# - **No tool limits**: The prompt mentions using available tools but does not set boundaries on their use, such as frequency or types of tools allowed.
# - **Unclear uncertainty handling**: There is no guidance provided about how to handle situations where the math problem is unclear or ambiguous—should the assistant ask for clarification?

# ### 4. Input and Output Specification
# - **Output schema missing**: While the prompt instructs to show work and provide a final answer, it does not specify the format (e.g., how to format the answer).
# - **No validation**: Lacks clear instructions regarding verifying intermediate steps or results before presenting the final answer.

# ### 5. Scope and Safety
# - **No error handling**: There is no instruction about what to do if a calculation fails or is incomplete. This is important for user safety and assurance of accuracy.

# ### 6. Efficiency and Maintainability
# - **Overexplained**: The instructions could be more concise; the repeated emphasis on precision could be shortened or integrated with other points.
# - **Poor auditability**: The prompt doesn't have clear section markers or a structured layout for easy reviewing.

# ### Summary
# - **Structure**: Incomplete; lacks overall goal clarity.
# - **Control**: Needs more boundaries on tool usage and handling ambiguity.
# - **Scope**: Acceptable but lacks error handling.
# - **Format**: Output requirements are unclear, lacking a defined schema.
# - **Safety**: Potential concerns with no guidance on error handling.

# Overall, the prompt requires refinement for clarity, precision, and completeness to improve its effectiveness in delivering math assistance.