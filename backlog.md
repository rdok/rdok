# Backlog

- ~~Brainstorm effective ways to handle expired tokens (e.g. GitHub PAT in Vercel/AWS)~~
- Eliminate Vercel from rdok/rdok stats pipeline: run github-readme-stats locally inside GitHub Actions using the auto-provided GITHUB_TOKEN (rotates every run, never expires). Removes dependency on Vercel stored PAT entirely.
