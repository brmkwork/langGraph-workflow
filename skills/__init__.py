from skills.functional.retrieve_skill import skill as retrieve_skill
from skills.guardrails.pii_middleware import guardrail as pii_guardrail
from logger import log

#registered skills 
SKILLS = [
    retrieve_skill,
]

#registered guardrails 
GUARDRAILS = [
    pii_guardrail,
]


def get_tools() -> list:
    """
    Returns all tools — skills + guardrails combined.
    This is what gets bound to the LLM.
    Adding a new skill or guardrail to the lists above
    automatically makes it available to the agent.
    """
    skill_tools     = [s["tool"] for s in SKILLS]
    guardrail_tools = [g["tool"] for g in GUARDRAILS]
    all_tools       = skill_tools + guardrail_tools

    log("SKILL REGISTRY", "Tools loaded and ready", {
        "skills":     [s["name"] for s in SKILLS],
        "guardrails": [g["name"] for g in GUARDRAILS],
        "total":      len(all_tools),
    })

    return all_tools


def get_skill_descriptions() -> str:
    """
    Builds the SKILLS section of the agent system prompt.
    Each skill's description comes from its own file — 
    the registry just assembles them.
    """
    if not SKILLS:
        return "  None registered"
    return "\n".join([
        f"  - {s['tool'].name}: {s['description']}"
        for s in SKILLS
    ])


def get_guardrail_descriptions() -> str:
    """
    Builds the GUARDRAILS section of the agent system prompt.
    Guardrails are listed separately so the agent understands
    they carry a different expectation — apply them protectively,
    not just when convenient.
    """
    if not GUARDRAILS:
        return "  None registered"
    return "\n".join([
        f"  - {g['tool'].name}: {g['description']}"
        for g in GUARDRAILS
    ])


def get_skill_names() -> list:
    return [s["name"] for s in SKILLS]


def get_guardrail_names() -> list:
    return [g["name"] for g in GUARDRAILS]