---
name: bash-tool-is-not-zsh
description: "CC's Bash tool runs `bash`, NOT `zsh`. Smoke-testing zsh-specific features (chpwd hooks, precmd/preexec, zinit-sourced functions, zsh-only globbing) directly in Bash gives false negatives. Wrap such tests in `zsh -ic '<cmd>'` so ~/.zshrc actually sources."
metadata:
  node_type: memory
  type: feedback
---

The Bash tool's persistent shell is `bash`, which does NOT source `~/.zshrc`, does NOT install zsh hooks, and does NOT recognize zsh-only syntax (e.g., `typeset -gaU`, `chpwd_functions+=(...)`).

**Why:** Smoke-tested a new `chpwd_op_token` hook (added to `executable_dot_zshrc.tmpl`) by running `op vault list` in the Bash tool after `cd` to the OOM workspace. Saw JM's `homelab` vault instead of OOM's `dev`+`machine` — concluded the hook was broken. It wasn't; the Bash tool just never fired the hook because chpwd is a zsh thing.

**How to apply:**

- Smoke-tests for zsh hooks (chpwd, precmd, preexec, periodic, zshaddhistory) must use `zsh -ic '<cmd>'`. The `-i` flag forces interactive mode so `~/.zshrc` is sourced; the `-c` runs the command and exits.
- Pattern that works (verified 2026-05-20 on `jm/workspace-aware-op-token`):

  ```
  zsh -ic 'cd ~/Documents/local/oneonme-platform; op vault list 2>&1 | head -5'
  ```

  Inside that subshell, `cd` fires chpwd_op_token, which re-exports `OP_SERVICE_ACCOUNT_TOKEN`. Then `op vault list` runs in the same subshell with the routed token.

- Token-length / env-var smoke tests run in plain Bash will report the *Bash-tool's* env (inherited from CC parent, often the ambient SA from when CC was launched). They do not reflect what an interactive zsh in the same dir would do. If you need to compare ambient state, run BOTH probes through `zsh -ic`.

- Same rule applies to any feature that lives in a zsh-only sourced file: bashrc-equivalent assumptions (precmd hooks, zsh modules, prompt functions, zinit-managed plugins). Verifying any of these in Bash returns a false reading.

## Related

- [[reference_rg_aliased_in_cc_shell]] — sibling case of CC tool environment masking expected CLI behavior.
- [[project_op_token_routing]] — the chpwd hook that motivated this lesson.
