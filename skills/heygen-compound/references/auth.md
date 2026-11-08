# HeyGen auth: which ledger, which command, which trap

Snapshot of `docs/auth.md` from the private `superwebpros/heygen-production` repo; the repo
wins if they disagree. No credential value belongs in any file, payload, command line, or log.
Reference secrets by path and env var name only.

## Two ledgers, one sanctioned

| | Sanctioned | Deprecated |
|---|---|---|
| Mechanism | OAuth, stored by the `heygen` CLI in its credentials file | `HEYGEN_API_KEY` env var |
| Ledger | Subscription plan, premium credits | Pay-as-you-go API wallet (unfunded) |
| Renders? | Yes, the only render path | No: returns `402 insufficient_credit` |

`HEYGEN_API_KEY` may still exist in project env files for non-render API use. Treat it as
the dead wallet for rendering.

## The override trap

The CLI documents that **`HEYGEN_API_KEY` in the environment always takes priority over any
stored credential.** So in any shell that has loaded a project env containing it, a bare
`heygen video create` silently bills the empty wallet and fails with `402`, even though the
OAuth session is still valid. This is the most common failure in the pipeline.

- `heygen-render` scrubs `HEYGEN_API_KEY` from every `heygen` subprocess it spawns.
- A bare `heygen` call does not. Unset it first:

```bash
env -u HEYGEN_API_KEY heygen video create ...   # or: unset HEYGEN_API_KEY
heygen auth status                              # which credential is active
```

## Checking status

```bash
heygen user me get --human   # plan, billing type, remaining premium credits
heygen auth status           # api_key vs OAuth
```

`Billing Type: subscription` is what you want. `api` means the trap has fired.

## Refreshing

```bash
heygen auth login --oauth    # browser OAuth (subscription credits)
heygen auth login --device   # attended remote/headless terminal
heygen auth logout
```

Always pass `--oauth` explicitly. Plain `heygen auth login` defaults to the API-key path
(and in non-interactive shells runs it outright).

**`auth login` replaces, it does not add.** The credentials file holds at most one of
`api_key` / `oauth`. Logging in with an API key destroys the OAuth session, stranding every
render on the dead wallet until someone re-runs `--oauth`.

OAuth tokens are short-lived (about a week). `heygen-render` checks expiry before spending
anything: it exits `3` with the remediation command on an expired token and warns within
24 hours of expiry.

## Pinned CLI version

The renderer wraps the `heygen` CLI (pinned at `v0.8.1` at time of writing) and warns when
`heygen --version` differs. On that warning, re-check `heygen video create --request-schema`
before trusting a render.

## MCP tools

Fine for read-only queries (list avatars, voices, videos; check render status; account
info). Not for final renders: they cannot express `voice_settings.engine_settings`, so
`eleven_v3` is never selected and audio tags are spoken aloud. The old "use MCP and strip
tags" guidance is obsolete; the OAuth CLI gives both subscription credits and tags.
