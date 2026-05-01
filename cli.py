"""forge — agent-first CLI for the Eidos forge ecosystem.

Generated per the cli-forge Agent-First CLI Contract:
- --json on every command (default ON when stdout is not a TTY)
- --quiet for piping
- --help is the schema
- Non-interactive (no prompts)
- Fast failure with actionable errors
- Progressive reveal: `forge` with no args shows commands; typos suggest

Examples:
  forge                              # progressive reveal — show available commands
  forge find "test my API" --json    # find best forge by task description
  forge list                         # list all forges
  forge list --type tool             # only tool-type forges
  forge info ml-forge                # full details on one forge
  forge how cli-forge                # invocation instructions
  forge for-project --path .         # recommendations for the current project
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys

import lib

VERSION = "0.2.0"


def _shared_flags() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit a single JSON object/array on stdout. Default when stdout is not a TTY.",
    )
    p.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Bare values, one per line. For piping.",
    )
    return p


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="forge",
        description="Route agents to the right Eidos forge.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"forge {VERSION}")

    sub = parser.add_subparsers(dest="cmd", required=False, metavar="COMMAND")
    shared = _shared_flags()

    find_p = sub.add_parser(
        "find",
        parents=[shared],
        help="Find the best forge for a task.",
        description="Match a plain-English task description against the registry; return ranked forges.",
    )
    find_p.add_argument("query", help='Task description, e.g. "test my API".')
    find_p.add_argument(
        "--top-k", type=int, default=3, dest="top_k", help="Max results to return (default 3)."
    )

    list_p = sub.add_parser(
        "list",
        parents=[shared],
        help="List all forges in the ecosystem.",
        description="Print every forge in registry.yaml. Optionally filter by type.",
    )
    list_p.add_argument(
        "--type",
        default="",
        dest="type_filter",
        choices=["", "knowledge", "tool"],
        help="Filter by forge type ('knowledge' or 'tool'). Default: all.",
    )

    info_p = sub.add_parser(
        "info",
        parents=[shared],
        help="Full details on a specific forge.",
        description="Look up a forge by name; return everything registry.yaml says about it.",
    )
    info_p.add_argument("name", help="Forge name, e.g. 'ml-forge'.")

    how_p = sub.add_parser(
        "how",
        parents=[shared],
        help="How to use a specific forge right now (clone/install/invoke steps).",
        description="Return ready-to-run invocation steps for the named forge.",
    )
    how_p.add_argument("name", help="Forge name, e.g. 'cli-forge'.")

    for_proj_p = sub.add_parser(
        "for-project",
        parents=[shared],
        help="Recommend forges for the current (or named) project.",
        description=(
            "Look at the project's filesystem (pyproject.toml, LICENSE, tests/, etc.) "
            "and recommend forges that would help."
        ),
    )
    for_proj_p.add_argument("--path", default=".", help="Project root path (default: cwd).")
    for_proj_p.add_argument(
        "--description", default="", help="Optional project description for finer recommendations."
    )

    return parser


def _emit(
    *,
    json_payload: object,
    plain: str,
    quiet_text: str,
    json_output: bool,
    quiet: bool,
) -> None:
    if json_output:
        print(json.dumps(json_payload, ensure_ascii=False))
    elif quiet:
        print(quiet_text)
    else:
        print(plain)


def _suggest_command(typo: str, valid: list[str]) -> str | None:
    matches = difflib.get_close_matches(typo, valid, n=1, cutoff=0.6)
    return matches[0] if matches else None


def _format_find(result: dict) -> tuple[str, str]:
    """Return (plain, quiet) text rendering for find_forges output."""
    if "error" in result:
        return result["error"], ""
    matches = result.get("matches", [])
    if not matches:
        return result.get("hint", "No matches."), ""
    plain_lines = [f'forges matching: "{result.get("query", "")}"']
    quiet_lines = []
    for m in matches:
        plain_lines.append(
            f"  {m['name']:24} {m.get('match_score', 0):.2f}  {m.get('description', '')}"
        )
        quiet_lines.append(m["name"])
    return "\n".join(plain_lines), "\n".join(quiet_lines)


def _format_list(result: dict) -> tuple[str, str]:
    forges = result.get("forges", [])
    plain_lines = [f"{result.get('count', 0)} forges:"]
    quiet_lines = []
    for f in forges:
        plain_lines.append(
            f"  {f['name']:24} [{f.get('type', '?')}]  {f.get('description', '')}"
        )
        quiet_lines.append(f["name"])
    return "\n".join(plain_lines), "\n".join(quiet_lines)


def _format_info(result: dict) -> tuple[str, str]:
    if "error" in result:
        return result["error"], ""
    name = result.get("name", "")
    parts = [
        f"name:        {name}",
        f"type:        {result.get('type', '')}",
        f"description: {result.get('description', '')}",
        f"repo:        {result.get('repo', '')}",
    ]
    if result.get("skills"):
        parts.append("skills:")
        for s in result["skills"]:
            if isinstance(s, dict):
                for k, v in s.items():
                    parts.append(f"  {k}: {v}")
            else:
                parts.append(f"  {s}")
    if result.get("tools"):
        parts.append("tools:")
        for t in result["tools"]:
            if isinstance(t, dict):
                for k, v in t.items():
                    parts.append(f"  {k}: {v}")
            else:
                parts.append(f"  {t}")
    return "\n".join(parts), name


def _format_how(result: dict) -> tuple[str, str]:
    if "error" in result:
        return result["error"], ""
    parts = [
        f"forge: {result.get('name')}",
        f"description: {result.get('description', '')}",
        f"invocation: {result.get('invocation', '')}",
        "",
        "quick_start:",
        result.get("quick_start", ""),
    ]
    return "\n".join(parts), result.get("name", "")


def _format_for_project(result: dict) -> tuple[str, str]:
    parts = [f"project: {result.get('project', '')}"]
    rec = result.get("recommended", [])
    if rec:
        parts.append("recommended:")
        for r in rec:
            mark = "✓" if r.get("installed") else " "
            parts.append(f"  [{mark}] {r['name']:20} — {r['reason']}")
    opt = result.get("optional", [])
    if opt:
        parts.append("optional:")
        for o in opt:
            mark = "✓" if o.get("installed") else " "
            parts.append(f"  [{mark}] {o['name']:20} — {o['reason']}")
    quiet_lines = [r["name"] for r in rec]
    return "\n".join(parts), "\n".join(quiet_lines)


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    if argv and argv[0] not in {"-h", "--help", "--version"}:
        # Detect typos before argparse explodes.
        first = argv[0]
        valid = {"find", "list", "info", "how", "for-project"}
        if first not in valid and not first.startswith("-"):
            suggestion = _suggest_command(first, list(valid))
            print(f"Error: unknown command {first!r}.", file=sys.stderr)
            if suggestion:
                print(f"Did you mean 'forge {suggestion}'?", file=sys.stderr)
            print("Run `forge` to see available commands.", file=sys.stderr)
            return 2

    parser = _build_parser()

    # `forge` with no args = `forge --help`. Single discovery surface.
    if not argv:
        parser.print_help()
        return 0

    args = parser.parse_args(argv)

    if args.cmd is None:
        parser.print_help()
        return 0

    explicit_json = getattr(args, "json_output", False)
    quiet = getattr(args, "quiet", False)
    auto_json = not sys.stdout.isatty() and not quiet
    json_output = explicit_json or auto_json

    if args.cmd == "find":
        result = lib.find_forges(args.query, args.top_k)
        plain, quiet_text = _format_find(result)
        _emit(
            json_payload=result,
            plain=plain,
            quiet_text=quiet_text,
            json_output=json_output,
            quiet=quiet,
        )
        return 0 if "error" not in result and result.get("matches") else 1

    if args.cmd == "list":
        result = lib.list_forges(args.type_filter)
        plain, quiet_text = _format_list(result)
        _emit(
            json_payload=result,
            plain=plain,
            quiet_text=quiet_text,
            json_output=json_output,
            quiet=quiet,
        )
        return 0

    if args.cmd in ("info", "how"):
        if args.cmd == "info":
            result = lib.get_forge_info(args.name)
            plain, quiet_text = _format_info(result)
        else:
            result = lib.get_forge_how(args.name)
            plain, quiet_text = _format_how(result)
        if "error" in result:
            valid_names = lib.all_forge_names()
            suggestion = _suggest_command(args.name, valid_names)
            if suggestion:
                if json_output:
                    result["did_you_mean"] = suggestion
                else:
                    plain += f"\nDid you mean '{suggestion}'?"
            _emit(
                json_payload=result,
                plain=plain,
                quiet_text="",
                json_output=json_output,
                quiet=quiet,
            )
            return 2
        _emit(
            json_payload=result,
            plain=plain,
            quiet_text=quiet_text,
            json_output=json_output,
            quiet=quiet,
        )
        return 0

    if args.cmd == "for-project":
        result = lib.recommend_for_project(args.path, args.description)
        plain, quiet_text = _format_for_project(result)
        _emit(
            json_payload=result,
            plain=plain,
            quiet_text=quiet_text,
            json_output=json_output,
            quiet=quiet,
        )
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
