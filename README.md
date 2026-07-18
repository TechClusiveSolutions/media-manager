# Mediman

Mediman is a cross-platform, accessibility-first desktop application for managing multiple social media accounts across multiple platforms from a single interface. It is built with wxPython and targets Windows, macOS, and Linux.

## Why Mediman exists

Most desktop and third-party clients for Mastodon, X, and Facebook are built sighted-first, with accessibility treated as an afterthought, if it's addressed at all: unlabeled controls, unpredictable focus order, custom widgets that don't expose the right roles to a screen reader, and visual-only notifications with no non-visual equivalent. For a screen reader user or someone with low vision, this ranges from a degraded experience to a client that simply doesn't work. Mediman exists to close that gap directly — accessibility is treated as a release gate here, not a feature to bolt on afterward, so that screen reader and low-vision users have a genuinely first-class multi-platform client rather than one they have to work around.

## What Mediman does

From one application, Mediman lets you:

* Authenticate multiple accounts, across multiple platforms, and view them individually, split by platform, or combined into a single unified feed.
* Compose a post once and cross-post it to several platforms/accounts at once, with per-platform constraint checking (e.g. character limits) and an optional AI-assisted condensing step when a platform's limits don't fit the original draft.
* Send and receive direct messages, with your choice of a unified inbox or separate inboxes per platform/account.
* Receive configurable notifications for platform events (mentions, replies, DMs, follows), per account and per event type.
* Optionally use an AI provider — your own cloud API key, or a local on-device model that needs no key and makes no network call — to draft posts from a prompt, and optionally (opt-in, per account) allow AI-authored posts to be sent without per-post confirmation, with every autonomous post recorded in a dedicated, reviewable audit log.

Supported platforms, in build order: **Mastodon** (first), **X (Twitter)** (second), **Facebook** (third). Each platform is built to full feature parity with the others to the extent that platform's own API allows.

## Project status

Mediman is in active design and pre-implementation. The product requirements, architecture, security posture, session-management design, and implementation/testing standards are fully written; application code has not yet been started. See `docs/index.md` for what's documented so far.

## Accessibility

Accessibility is a first-class requirement and a release gate, not a follow-up task. Every screen and control is designed to be fully operable with a screen reader, with sufficient contrast and sizing for low-vision users, and with a visual analog for every audible signal. Target compliance level is WCAG 2.0, validated against NVDA and JAWS on Windows, VoiceOver on macOS, and Orca on Linux.

## Credentials, privacy, and cost

Mediman is open source and does not bundle or manage credentials on your behalf. You register your own OAuth application with each platform you want to use, and supply your own API key if you choose to use a cloud AI provider (or use a local on-device model instead, which needs neither a key nor a network connection). Credentials are stored using your operating system's native secure credential storage — Windows Credential Manager, macOS Keychain, or Linux Secret Service/libsecret — never in a plain configuration file.

## Getting started

See `docs/USER_GUIDE.md` for installation instructions and a walkthrough of connecting your first Mastodon account.

## Contributing

Issues and project tracking live in the `TechClusiveSolutions/media-manager` GitHub repository and its "Media Manager Tracker" project. Feature branches are cut from `dev`; see the repository's operating instructions for the full branching, versioning, and release process.

**Primary contributor:** Jad Wauthier (the blind tech mage).

## License

Mediman is licensed under the [Apache License, Version 2.0](LICENSE).

Copyright © 2026 TechClusive Solutions.
