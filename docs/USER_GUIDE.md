# Mediman User Guide: Setup

This guide covers the two things a new user needs before Mediman is usable: installing the application, and registering and connecting your own Mastodon account. Mediman does not ship with any platform credentials built in — as an open source project, every user registers their own connection to each platform they want to use.

This guide will be extended with feature documentation (feeds, composing, direct messages, notifications, AI-assisted drafting) as those features ship. For now it covers only what's needed to get a working Mastodon connection.

## 1. Installing Mediman

Mediman's packaged installer format (Windows/macOS/Linux) has not been finalized yet. Until a packaged release is available, Mediman is run from source:

1. Install Python 3.13 or later from python.org, or your operating system's package manager.
2. Install Poetry, the tool Mediman uses to manage its dependencies, following the instructions at python-poetry.org.
3. Download or clone the Mediman source code.
4. From the Mediman folder, run: `poetry install`. This downloads and installs everything Mediman needs to run.
5. Run Mediman with: `poetry run mediman` (or the equivalent command documented in the project's `README.md` at the time you install it, since this may change before the first packaged release).

If you use a screen reader, Mediman is designed to be fully operable with one from first launch — every screen and control should be reachable and clearly labeled. If you find a control that isn't, please open an issue against the project.

## 2. Setting Up Your Mastodon Account

Mastodon requires every application to register itself with each Mastodon server (also called an "instance") it connects to. This is a one-time setup step per Mastodon account you want to use in Mediman.

### Step 1: Know which Mastodon instance you're on

Every Mastodon account lives on a specific server, for example `mastodon.social` or `fosstodon.org`. You'll need this address for the next step. If you're not sure, it's the part of your Mastodon profile address after the `@` — for an account like `@yourname@example.social`, the instance is `example.social`.

### Step 2: Register Mediman as an application on your instance

1. Log into your Mastodon account in a web browser.
2. Go to your instance's settings. The path is typically: Preferences, then Development, then "New Application." If your instance's menu wording differs, look for a section about "Applications" or "Third-party apps."
3. Give the application a name you'll recognize, such as "Mediman."
4. For the redirect URI (sometimes called "callback URL"), enter the value Mediman's settings screen shows you when you start adding a Mastodon account — this is generated per-attempt for security reasons and will be different each time you go through this process, so use the value shown to you at the time, not one from a previous attempt or from this guide.
5. Select the scopes (permissions) the application needs: at minimum `read`, `write`, and `follow`. If Mediman's settings screen requests additional scopes for a specific feature (for example, streaming or push notifications), it will tell you at that point.
6. Submit the form. Your instance will show you a **Client Key** and **Client Secret** — sometimes labeled "Client ID" and "Client Secret." Keep this page open, or copy both values somewhere temporarily; you'll need them in the next step.

### Step 3: Connect the account in Mediman

1. In Mediman, open Settings and choose to add a new Mastodon account.
2. Enter your instance address (from Step 1).
3. Enter the Client Key and Client Secret from Step 2.
4. Mediman will open your browser to complete the authorization on your instance. Log in if prompted, and approve the request.
5. Once approved, you'll be returned to Mediman, and the account will show as connected.

Your Client Key, Client Secret, and the token Mediman receives after authorization are stored using your operating system's secure credential storage (Windows Credential Manager, macOS Keychain, or Linux Secret Service/libsecret) — never in a plain configuration file, and never sent anywhere other than your chosen Mastodon instance.

### If something goes wrong

* **"Invalid redirect URI" or similar error from your instance:** the redirect URI you entered in Step 2 must match exactly what Mediman showed you for that specific connection attempt. If you started over, get the redirect URI again from Mediman's current screen rather than reusing an old one.
* **Mediman reports the account needs to be reconnected after working previously:** this means your instance revoked or expired the connection. Repeat Step 3 to reconnect; you do not need to re-register the application in Step 2 unless you also revoked the application itself on your instance.
* **You want to disconnect Mediman entirely:** you can revoke Mediman's access from your Mastodon instance's Settings/Authorized Applications page at any time, in addition to removing the account from Mediman's own settings.
