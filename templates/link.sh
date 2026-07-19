#!/usr/bin/env bash
# link.sh — wire every AI tool's config file to a project's shared AGENTS.md.
#
# Run from a project root that contains AGENTS.md. Idempotent and non-destructive:
# any real file it would replace is backed up to <file>.bak first.
#
# Usage:
#   bash link.sh [--dry-run] [--force] [--agents] [--skills] [--configs] [--workflow-foundations]
#     --dry-run   show what would happen, change nothing
#     --force     overwrite existing .bak backups instead of skipping
#     --agents    also install the AI_ONBOARD reference subagents (Claude Code + Codex)
#     --skills    also install the standard AI_ONBOARD skills (Claude Code + Codex)
#     --configs   add conservative project configs for Claude Code, Codex, and OpenCode
#     --workflow-foundations
#                 install the optional goal-contract + grill-requirements skills
#
# Wires: Claude Code (CLAUDE.md import), Gemini CLI (GEMINI.md symlink),
#        GitHub Copilot (.github/copilot-instructions.md symlink), Aider (.aider.conf.yml).
# Codex, OpenCode, Cursor, Zed, and Jules read AGENTS.md natively — nothing to wire for them.
# With --agents, the reference subagents from AI_ONBOARD/agents/ are copied into
# .claude/agents/ (*.md) and .codex/agents/ (*.toml).
# With --skills, each standard skill folder from AI_ONBOARD/skills/ is copied into
# .claude/skills/ (Claude Code) and .agents/skills/ (Codex — the vendor-neutral path,
# not .codex/skills). Optional workflow foundations require --workflow-foundations.
set -euo pipefail

DRY_RUN=0
FORCE=0
INSTALL_AGENTS=0
INSTALL_SKILLS=0
INSTALL_CONFIGS=0
INSTALL_WORKFLOW_FOUNDATIONS=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --force)   FORCE=1 ;;
    --agents)  INSTALL_AGENTS=1 ;;
    --skills)  INSTALL_SKILLS=1 ;;
    --configs) INSTALL_CONFIGS=1 ;;
    --workflow-foundations) INSTALL_WORKFLOW_FOUNDATIONS=1 ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

# Where this script lives, so --agents/--skills can find the repo's reference material whether
# link.sh is run from inside an AI_ONBOARD clone (templates/link.sh) or copied elsewhere.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(cd "$SCRIPT_DIR/.." 2>/dev/null && pwd)"
AGENTS_SRC="$REPO_DIR/agents"
SKILLS_SRC="$REPO_DIR/skills"
CONFIGS_SRC="$REPO_DIR/templates/configs"

say()  { printf '%s\n' "$*"; }
run()  { if [ "$DRY_RUN" -eq 1 ]; then say "  [dry-run] $*"; else eval "$*"; fi; }
skip() { say "  ✓ $1 — already wired, skipping"; }

if [ ! -f AGENTS.md ]; then
  echo "No AGENTS.md in $(pwd). Create one first (see AI_ONBOARD/templates/AGENTS.md)." >&2
  exit 1
fi

say "Legacy copy mode: link.sh does not track upgrades or uninstall ownership."
say "For managed installs, use: python3 scripts/ai_onboard.py install --help"

backup() { # $1 = path to a real (non-symlink) file to preserve
  local f="$1" quoted_f quoted_backup
  if [ -e "$f" ] && [ ! -L "$f" ]; then
    if [ -e "$f.bak" ] && [ "$FORCE" -eq 0 ]; then
      say "  ! $f.bak exists — leaving $f untouched (use --force to overwrite the backup)"
      return 1
    fi
    printf -v quoted_f '%q' "$f"
    printf -v quoted_backup '%q' "$f.bak"
    run "cp -p $quoted_f $quoted_backup"
    say "  ↳ backed up existing $f → $f.bak"
  fi
  return 0
}

install_agent_copy() {
  local source="$1" target="$2" quoted_source quoted_target
  if [ -L "$target" ]; then
    say "  ! $target is a symlink — preserving it"
    return
  fi
  if [ -e "$target" ]; then
    backup "$target" || return
  fi
  printf -v quoted_source '%q' "$source"
  printf -v quoted_target '%q' "$target"
  run "cp $quoted_source $quoted_target"
}

# symlink $2 -> $1 (target is relative to the link's directory).
# Symlink creation is treated as non-fatal: on Windows without Developer Mode `ln -s`
# fails, and we warn + continue rather than aborting the whole run (set -e).
make_symlink() {
  local target="$1" link="$2"
  if [ -L "$link" ] && [ "$(readlink "$link")" = "$target" ]; then skip "$link"; return; fi
  backup "$link" || return
  run "rm -f '$link'"
  if [ "$DRY_RUN" -eq 1 ]; then say "  [dry-run] ln -s '$target' '$link'"; return; fi
  if ln -s "$target" "$link" 2>/dev/null; then
    say "  → $link ⇒ $target"
  else
    say "  ! could not create symlink for $link (Windows without Developer Mode?) — skipped."
    say "    Enable Developer Mode, or point the tool at AGENTS.md directly."
  fi
}

install_agents() {
  say
  say "Reference subagents (--agents):"
  if [ ! -d "$AGENTS_SRC" ]; then
    say "  ! source not found at $AGENTS_SRC"
    say "    Run link.sh from an AI_ONBOARD clone, or copy manually:"
    say "      cp <AI_ONBOARD>/agents/*.md .claude/agents/       # Claude Code"
    say "      cp <AI_ONBOARD>/agents/codex/*.toml .codex/agents/ # Codex"
    return
  fi
  run "mkdir -p .claude/agents .codex/agents .opencode/agents"
  local f base
  for f in "$AGENTS_SRC"/*.md; do
    base="$(basename "$f")"
    [ "$base" = "README.md" ] && continue   # docs, not an agent definition
    install_agent_copy "$f" ".claude/agents/$base"
  done
  say "  → Claude Code: reference subagents copied into .claude/agents/"
  if [ -d "$AGENTS_SRC/codex" ]; then
    for f in "$AGENTS_SRC"/codex/*.toml; do
      base="$(basename "$f")"
      install_agent_copy "$f" ".codex/agents/$base"
    done
    say "  → Codex: reference subagents copied into .codex/agents/"
  fi
  if [ -d "$AGENTS_SRC/opencode" ]; then
    for f in "$AGENTS_SRC"/opencode/*.md; do
      base="$(basename "$f")"
      [ "$base" = "README.md" ] && continue
      install_agent_copy "$f" ".opencode/agents/$base"
    done
    say "  → OpenCode: reference subagents copied into .opencode/agents/"
  fi
}

install_config_file() {
  local source="$1" target="$2" quoted_source quoted_target quoted_parent
  if [ -e "$target" ]; then
    say "  ✓ $target exists — preserving it; merge the template manually if needed"
    return
  fi
  printf -v quoted_source '%q' "$source"
  printf -v quoted_target '%q' "$target"
  printf -v quoted_parent '%q' "$(dirname "$target")"
  run "mkdir -p $quoted_parent"
  run "cp $quoted_source $quoted_target"
  say "  → created $target"
}

install_configs() {
  say
  say "Harness project configs (--configs):"
  if [ ! -d "$CONFIGS_SRC" ]; then
    say "  ! source not found at $CONFIGS_SRC"
    return
  fi
  install_config_file "$CONFIGS_SRC/claude.settings.json" ".claude/settings.json"
  install_config_file "$CONFIGS_SRC/codex.config.toml" ".codex/config.toml"
  install_config_file "$CONFIGS_SRC/opencode.json" "opencode.json"
  say "  ↳ no provider, model, credential, or personal UI setting is installed"
}

install_skill_copy() {
  local source_dir="$1" destination_parent="$2"
  local target quoted_source quoted_parent
  target="$destination_parent/$(basename "$source_dir")"
  if [ -e "$target" ]; then
    say "      ✓ $target already exists — preserving the local copy"
    return
  fi
  printf -v quoted_source '%q' "$source_dir"
  printf -v quoted_parent '%q' "$destination_parent/"
  run "cp -R $quoted_source $quoted_parent"
}

install_skills() {
  say
  say "Skills (--skills):"
  if [ ! -d "$SKILLS_SRC" ]; then
    say "  ! source not found at $SKILLS_SRC"
    say "    Run link.sh from an AI_ONBOARD clone, or copy manually:"
    say "      cp -R <AI_ONBOARD>/skills/<name> .claude/skills/   # Claude Code"
    say "      cp -R <AI_ONBOARD>/skills/<name> .agents/skills/   # Codex (.agents, not .codex)"
    return
  fi
  run "mkdir -p .claude/skills .agents/skills"
  # Discover skills at any depth — flat (skills/foo/) or grouped (skills/cloudflare/foo/).
  # A skill is any directory containing a SKILL.md; README/NOTICE/LICENSE are skipped naturally.
  local skfile d name
  find "$SKILLS_SRC" -type f -name SKILL.md 2>/dev/null | sort | while IFS= read -r skfile; do
    d="$(dirname "$skfile")"
    case "$d" in
      "$SKILLS_SRC/workflow-foundations/"*)
        [ "$INSTALL_WORKFLOW_FOUNDATIONS" -eq 1 ] || continue
        ;;
    esac
    name="$(basename "$d")"
    install_skill_copy "$d" ".claude/skills"
    install_skill_copy "$d" ".agents/skills"
    say "    • $name"
  done
  say "  → skills copied into .claude/skills/ (Claude Code) and .agents/skills/ (Codex)"
  if [ "$INSTALL_WORKFLOW_FOUNDATIONS" -eq 0 ]; then
    say "  ↳ optional goal-contract + grill-requirements skipped (add --workflow-foundations)"
  fi
}

install_workflow_foundations() {
  say
  say "Optional workflow foundations (--workflow-foundations):"
  if [ ! -d "$SKILLS_SRC/workflow-foundations" ]; then
    say "  ! source not found at $SKILLS_SRC/workflow-foundations"
    return
  fi
  run "mkdir -p .claude/skills .agents/skills"
  local skfile d name
  find "$SKILLS_SRC/workflow-foundations" -type f -name SKILL.md 2>/dev/null | sort | while IFS= read -r skfile; do
    d="$(dirname "$skfile")"
    name="$(basename "$d")"
    install_skill_copy "$d" ".claude/skills"
    install_skill_copy "$d" ".agents/skills"
    say "    • $name"
  done
  say "  → optional workflow foundations copied into both harness skill directories"
}

say "Wiring AI tools in $(pwd) to AGENTS.md"
[ "$DRY_RUN" -eq 1 ] && say "(dry run — no changes will be made)"

# --- Claude Code: CLAUDE.md imports AGENTS.md (import, not symlink — keeps room for
#     Claude-only notes and works cross-platform, per Anthropic's guidance) -----------
say
say "Claude Code (CLAUDE.md):"
if [ -L CLAUDE.md ]; then
  say "  ! CLAUDE.md is a symlink — preserving it"
elif [ -f CLAUDE.md ] && grep -qE '^\s*@AGENTS\.md\s*$' CLAUDE.md; then
  skip "CLAUDE.md"
elif [ -f CLAUDE.md ]; then
  backup CLAUDE.md && {
    run "printf '@AGENTS.md\n\n%s\n' \"\$(cat CLAUDE.md)\" > CLAUDE.md.new && mv CLAUDE.md.new CLAUDE.md"
    say "  → prepended '@AGENTS.md' import to existing CLAUDE.md"
  }
else
  run "printf '@AGENTS.md\n' > CLAUDE.md"
  say "  → created CLAUDE.md with '@AGENTS.md' import"
fi

# --- Gemini CLI: GEMINI.md symlink -------------------------------------------
say
say "Gemini CLI (GEMINI.md):"
make_symlink "AGENTS.md" "GEMINI.md"

# --- GitHub Copilot: .github/copilot-instructions.md symlink -----------------
say
say "GitHub Copilot (.github/copilot-instructions.md):"
run "mkdir -p .github"
make_symlink "../AGENTS.md" ".github/copilot-instructions.md"

# --- Aider: .aider.conf.yml reads AGENTS.md ----------------------------------
say
say "Aider (.aider.conf.yml):"
if [ -f .aider.conf.yml ] && grep -qE 'AGENTS\.md' .aider.conf.yml; then
  skip ".aider.conf.yml"
elif [ -f .aider.conf.yml ]; then
  say "  ! .aider.conf.yml exists without an AGENTS.md reference — add manually:"
  say "      read:\n        - AGENTS.md"
else
  run "printf 'read:\n  - AGENTS.md\n' > .aider.conf.yml"
  say "  → created .aider.conf.yml reading AGENTS.md"
fi

# --- Reference subagents + skills (opt-in) -----------------------------------
[ "$INSTALL_AGENTS" -eq 1 ] && install_agents
[ "$INSTALL_SKILLS" -eq 1 ] && install_skills
[ "$INSTALL_CONFIGS" -eq 1 ] && install_configs
if [ "$INSTALL_WORKFLOW_FOUNDATIONS" -eq 1 ] && [ "$INSTALL_SKILLS" -eq 0 ]; then
  install_workflow_foundations
fi

say
say "Done. Codex, OpenCode, Cursor, Zed, and Jules read AGENTS.md natively."
if [ "$INSTALL_AGENTS" -eq 0 ] || [ "$INSTALL_SKILLS" -eq 0 ] || [ "$INSTALL_CONFIGS" -eq 0 ]; then
  say "Tip: add --agents, --skills, and/or --configs for the portable runtime layers."
fi
if [ "$INSTALL_WORKFLOW_FOUNDATIONS" -eq 0 ]; then
  say "Optional: add --workflow-foundations for native-first GOAL + explicit GRILL fallbacks."
fi
[ "$DRY_RUN" -eq 1 ] && say "(dry run — re-run without --dry-run to apply)"
exit 0
