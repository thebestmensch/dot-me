# Privacy Policy

`dot-me` does not collect, transmit, or share any data.

## What `dot-me` does

The format is a folder at `~/.me/` containing four plain-text files (`identity.yaml`, `voice.md`, `preferences.yaml`, `working-style.yaml`). These files live on your machine and are read by consumer tools (Claude Code, Codex CLI, Cursor, Gemini CLI) that you install yourself.

The Claude Code reference consumer (this plugin) reads `~/.me/identity.yaml` at session start, injects the content into the local Claude Code session, and exposes the `/me` slash command for editing the files. It performs no network calls, sends no telemetry, and writes nothing outside of `~/.me/` and standard Claude Code session state.

## What `dot-me` does not do

- No analytics or telemetry. The plugin makes no outbound HTTP requests.
- No third-party services. The plugin does not call any external API.
- No data sharing. The contents of `~/.me/` never leave your machine via this plugin.

Whatever your AI tool of choice does with the content once loaded into its session is governed by that tool's own privacy policy. `dot-me` itself is local-only.

## Hardening

The plugin ships SessionStart hooks that scrub `~/.me/` content from runtime tool surfaces (filesystem-readable paths, MCP resources) once it has been injected at startup. This mitigates exfiltration via prompt injection from a malicious project's `CLAUDE.md` or `AGENTS.md`. See [SECURITY.md](SECURITY.md) for the full threat model.

## Contact

Questions: james@jamesmensch.com.
