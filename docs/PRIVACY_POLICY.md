# Mediman Privacy Policy

**Status: Draft — pending legal review. Not yet in effect until reviewed by qualified legal counsel and dated below.**

Last updated: [DATE PENDING LEGAL REVIEW]

## 1. Who This Policy Covers

Mediman is open source software distributed by Tech-Clusive Solutions, LLC. This policy describes how Mediman, the application itself, handles your data. It does not describe how Mastodon, X, Facebook, or any AI provider you connect to Mediman handles your data — each of those is a separate service with its own privacy policy, and you should review theirs directly.

## 2. The Short Version

Mediman does not operate a server that collects, stores, or transmits your data on your behalf. Mediman runs on your own device. Your account credentials, posts, drafts, and messages are stored locally on your device, encrypted where noted below, and are sent only to the platforms and AI providers you yourself choose to connect. Mediman's developers do not receive a copy of your content, your credentials, or your usage activity.

This will change for the paid Subscription Services described in Section 8, once those launch — see that section for what will be different.

## 3. What Mediman Stores, and Where

* **Platform account credentials** (OAuth tokens, and the Client Key/Secret you register with each platform): stored using your operating system's native secure credential storage — Windows Credential Manager, macOS Keychain, or Linux Secret Service/libsecret. These are never written to a plain configuration file, and never transmitted anywhere other than the platform they authenticate you to.
* **Cloud AI provider API keys** (if you choose to use a cloud AI provider rather than an on-device model): stored the same way, in OS-native secure credential storage.
* **Post and DM content, drafts**: stored locally in Mediman's own local application data, encrypted at rest using a per-install encryption key that is itself stored in OS-native secure credential storage. Whether this content is retained in Mediman's local log at all is controlled by a setting you control (off by default).
* **Application log**: records what happened (event types, which account, timestamps, success/failure) for troubleshooting. Message content is not included in the log unless you explicitly enable that, and when enabled, it is encrypted the same way as stored drafts. OAuth tokens and AI API keys are never written to the log, under any setting.
* **Configuration**: your settings (feed layout, notification preferences, keyboard shortcuts, autonomous-posting opt-ins) are stored in a local configuration file on your device, which you can locate and edit directly.

## 4. What Mediman Sends, and to Whom

* **To the social platforms you connect** (Mastodon, X, Facebook): whatever you explicitly send — posts, replies, boosts, favorites, DMs — is sent only to that platform's own API, using your own registered OAuth application and your own account. Mediman does not relay this data anywhere else.
* **To your chosen AI provider**, only if you use AI-assisted drafting, condensing, or autonomous posting features:
  * **If you choose a cloud AI provider**, the draft text you're working on (and, for image alt-text generation, the image) is sent to that provider's API using your own API key. Mediman's settings screen tells you this at the point you choose a cloud provider — it is not something you have to go find in this document.
  * **If you choose an on-device AI model**, nothing leaves your device for that feature. No network call is made.
  * Mediman does not silently switch between providers on failure — a failed cloud AI call is reported to you as an error, never retried automatically against a different provider you didn't select for that action.
* **To Mediman's developers**: nothing, by default. Mediman does not phone home, does not include analytics or telemetry, and does not transmit crash reports, logs, or usage data automatically. If you choose to report a bug (for example, by opening a GitHub issue), any information you include in that report is only what you choose to share.

## 5. Federated and Third-Party Content

Mediman displays content — posts, profile information, media — originating from other people's accounts on federated or third-party platforms (in particular, Mastodon's federated network, where content can originate from a server neither you nor Mediman's developers control). This content is not vetted by Mediman before being displayed to you; it is handled per the content-safety rules in `docs/SECURITY.md` (rendered as plain text, links opened only on your explicit action, media fetched only from the platform's own supplied URLs). Mediman is not responsible for the content of posts, messages, or media originating from other users or instances.

## 6. Your Choices and Controls

* You choose which platforms to connect, and can disconnect any account at any time from within Mediman, which removes its stored credentials from OS-native secure storage.
* You choose whether to use AI features at all, and if so, whether to use a cloud provider (with your own key) or an on-device model (no network call).
* You control whether message content is retained in the local log (off by default).
* Because Mediman stores everything locally, deleting the application's local data directory removes all locally-stored Mediman data. This does not delete anything from the platforms themselves (a boosted post, a sent DM) — those remain governed by that platform's own policies.

## 7. Children's Privacy

Mediman is not directed at children and is not designed for use by children under the age of 13 (or the relevant minimum age in your jurisdiction). Mediman does not knowingly collect data from children, consistent with Section 2 above — it does not collect data from anyone, since it runs entirely on your own device.

## 8. Subscription Services (Planned — Not Yet Available)

Mediman's developers plan to offer optional paid subscription features in the future, after the current proof-of-concept phase is complete. **This section is a placeholder.** Once subscription features are built, this policy will be updated — before those features launch, not after — to describe, at minimum:

* What account or billing information is collected to support a subscription (e.g. an email address, a billing relationship with a payment processor).
* Whether any subscription-related data is processed by Mediman's developers or a third-party billing provider, and which one.
* How this interacts with the local-only data model described above for the free/core features, which are expected to remain locally-stored regardless of subscription status.

No subscription features exist today. Nothing in this section authorizes or describes any data collection currently in effect.

## 9. Changes to This Policy

If this policy changes, the "Last updated" date at the top will change, and material changes will be called out in Mediman's release notes.

## 10. Contact

Questions about this Privacy Policy can be sent to info@TechClusiveSolutions.com.
