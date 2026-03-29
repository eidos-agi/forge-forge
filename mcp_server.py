"""forge-forge MCP server — route agents to the right forge.

Tools:
  forge_find  — "I need to do X" → here's the forge for that
  forge_list  — list all forges (optionally filter by type)
  forge_info  — full details on a specific forge

Matching: L0 keyword + token-overlap scoring against registry.yaml.
No ML, no embeddings, no external deps beyond PyYAML + MCP.
"""

import re
from pathlib import Path

import yaml
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("eidos-forge-forge")

# ---------------------------------------------------------------------------
# Registry loader
# ---------------------------------------------------------------------------

_registry: list[dict] | None = None


def _load_registry() -> list[dict]:
    """Load forges from registry.yaml (cached after first call)."""
    global _registry
    if _registry is not None:
        return _registry

    registry_path = Path(__file__).parent / "registry.yaml"
    with open(registry_path) as f:
        data = yaml.safe_load(f)

    _registry = data.get("forges", [])
    return _registry


# ---------------------------------------------------------------------------
# Scoring — pure L0 token overlap
# ---------------------------------------------------------------------------

_STOP_WORDS = frozenset(
    "a an the is are was were be been being have has had do does did "
    "will would shall should may might can could i me my we our you your "
    "it its he she they them this that these those of in to for on with "
    "at by from as into about and or but not no nor so yet both each "
    "how what which who whom when where why all any some".split()
)


# Synonyms: maps common words to the tokens that appear in forge descriptions.
# This is the L0 escape hatch — when a user says "safer" we expand to "security".
_SYNONYMS: dict[str, list[str]] = {
    "safe": ["security", "audit", "vulnerability"],
    "safer": ["security", "audit", "vulnerability"],
    "secure": ["security", "audit", "vulnerability"],
    "harden": ["security", "hardening"],
    "vuln": ["vulnerability", "security"],
    "deal": ["underwriting", "deal", "conviction"],
    "invest": ["underwriting", "deal", "conviction"],
    "diligence": ["underwriting", "deal"],
    "etl": ["elt", "pipeline", "extract", "load", "transform"],
    "data": ["elt", "pipeline", "data"],
    "ingest": ["elt", "pipeline", "extract"],
    "picture": ["image", "generation"],
    "photo": ["image", "generation"],
    "image": ["image", "generation"],
    "images": ["image", "generation"],
    "generate": ["generation", "generate"],
    "deploy": ["deploy", "railway", "shipping"],
    "release": ["release", "pypi", "foss"],
    "migrate": ["refactor", "migration", "port"],
    "rewrite": ["refactor", "port", "migration"],
    "meal": ["shopping", "meal", "grocery"],
    "grocery": ["shopping", "grocery", "meal"],
    "video": ["video", "cinematic", "production"],
    "brand": ["brand", "identity", "visuals"],
    "market": ["marketing", "campaign", "distribution"],
}


def _tokenize(text: str) -> set[str]:
    """Lowercase, split on non-alpha, drop stop words and short tokens."""
    tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
    tokens = tokens - _STOP_WORDS - {t for t in tokens if len(t) < 3}

    # Expand synonyms
    expanded = set(tokens)
    for t in tokens:
        if t in _SYNONYMS:
            expanded.update(_SYNONYMS[t])
    return expanded


def _build_forge_tokens(forge: dict) -> set[str]:
    """Build the full token set for a forge — name, description, skills/tools."""
    parts = [forge.get("name", ""), forge.get("description", "")]

    for skill in forge.get("skills", []):
        if isinstance(skill, dict):
            for k, v in skill.items():
                parts.extend([k, str(v)])
        else:
            parts.append(str(skill))

    for tool in forge.get("tools", []):
        if isinstance(tool, dict):
            for k, v in tool.items():
                parts.extend([k, str(v)])
        else:
            parts.append(str(tool))

    return _tokenize(" ".join(parts))


def _score(query_tokens: set[str], forge: dict) -> float:
    """Score a forge against query tokens. Returns 0.0-1.0."""
    forge_tokens = _build_forge_tokens(forge)
    if not forge_tokens or not query_tokens:
        return 0.0

    # Jaccard-ish: intersection over query size (recall-oriented)
    overlap = query_tokens & forge_tokens
    if not overlap:
        return 0.0

    # Bonus: if query token appears in forge name, weight it higher
    name_tokens = _tokenize(forge.get("name", ""))
    name_hits = query_tokens & name_tokens
    score = (len(overlap) + len(name_hits)) / len(query_tokens)
    return min(score, 1.0)


def _format_forge(forge: dict, score: float | None = None) -> dict:
    """Format a forge entry for tool output."""
    result = {
        "name": forge.get("name"),
        "type": forge.get("type"),
        "description": forge.get("description"),
        "repo": forge.get("repo"),
    }
    if forge.get("skills"):
        result["skills"] = forge["skills"]
    if forge.get("tools"):
        result["tools"] = forge["tools"]
    if score is not None:
        result["match_score"] = round(score, 3)
    return result


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def forge_find(query: str, top_k: int = 3) -> dict:
    """Find the best forge for a task.

    Args:
        query: What you need to do, in plain language.
              Examples: "test my API", "release on PyPI", "write a book"
        top_k: Number of results to return (default 3).
    """
    forges = _load_registry()
    query_tokens = _tokenize(query)

    if not query_tokens:
        return {"error": "Query too short or all stop words. Be more specific."}

    scored = [(f, _score(query_tokens, f)) for f in forges]
    scored.sort(key=lambda x: x[1], reverse=True)

    # Filter to non-zero matches
    matches = [(f, s) for f, s in scored[:top_k] if s > 0]

    if not matches:
        return {
            "matches": [],
            "hint": "No forges matched. Try different keywords. "
            "Use forge_list to see all available forges.",
        }

    return {
        "query": query,
        "matches": [_format_forge(f, s) for f, s in matches],
    }


@mcp.tool()
def forge_list(type_filter: str = "") -> dict:
    """List all forges in the Eidos ecosystem.

    Args:
        type_filter: Optional — "knowledge" or "tool" to filter by type.
    """
    forges = _load_registry()

    if type_filter:
        forges = [f for f in forges if f.get("type") == type_filter]

    return {
        "count": len(forges),
        "forges": [_format_forge(f) for f in forges],
    }


@mcp.tool()
def forge_info(name: str) -> dict:
    """Get full details on a specific forge.

    Args:
        name: Forge name (e.g. "test-forge", "ml-forge").
    """
    forges = _load_registry()
    clean = name.lower().strip()

    for f in forges:
        if f.get("name", "").lower() == clean:
            return _format_forge(f)

    # Fuzzy: check if query is substring of name
    for f in forges:
        if clean in f.get("name", "").lower():
            return _format_forge(f)

    return {
        "error": f"No forge named '{name}'. Use forge_list to see all forges.",
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main():
    mcp.run()


if __name__ == "__main__":
    main()
