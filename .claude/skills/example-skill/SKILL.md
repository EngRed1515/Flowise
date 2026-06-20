---
# `name`: lowercase, hyphenated. This is how the skill is invoked: /example-skill
name: example-skill
# `description` is the TRIGGER. Claude matches the user's request against this
# text to decide whether to load the skill. Be specific and start with what it
# does, then "Use when the user ...". This is the single most important field.
description: A template you can copy to create your own skill. Use when the user asks to see how skills are structured or wants to scaffold a new skill.
---

# Example Skill

Everything below the frontmatter is the **instruction body**. It is loaded into
context only when the skill is triggered, so you can be as detailed as you want
without bloating every conversation.

## How to write a good skill

1. **One job per skill.** Keep each skill focused on a single workflow.
2. **Write imperative steps.** Tell Claude exactly what to do, in order.
3. **Reference real commands and paths** from this repo so they actually run.
4. **Bundle helpers if needed.** You can put scripts, templates, or reference
   files in this folder and point to them, e.g. `./scripts/do-thing.sh`.

## Example body

When triggered, do the following:

1. Explain what you are about to do.
2. Run the relevant command(s).
3. Report the result.

## Where skills live

- Project (shared via git): `<repo>/.claude/skills/<name>/SKILL.md`
- Personal (all your projects): `~/.claude/skills/<name>/SKILL.md`

Copy this folder, rename it, edit the `name`/`description`, and you have a new
skill. Invoke it by typing `/<name>` or just by asking for the task in the
description.
