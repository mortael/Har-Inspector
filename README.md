<div align="center">
<img width="1200" height="475" alt="GHBanner" src="https://github.com/user-attachments/assets/0aa67016-6eaf-458a-adb2-6e31a0763ed6" />
</div>

# Run and deploy your AI Studio app

This contains everything you need to run your app locally.

View your app in AI Studio: https://ai.studio/apps/5a5a1cae-77d2-4b56-8675-e6c9be4344db

## Run Locally

**Prerequisites:**  Node.js


1. Install dependencies:
   `npm install`
2. Set the `GEMINI_API_KEY` in [.env.local](.env.local) to your Gemini API key
3. Run the app:
   `npm run dev`

## Desktop App (Python)

A native desktop build is available in `desktop/` using `customtkinter`:

- Run: `cd desktop && python -m venv .venv && . .venv/bin/activate && python -m pip install -e . && python -m har_inspector_desktop`
- Build EXE + installer: see `desktop/README.md`
