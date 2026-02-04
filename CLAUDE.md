# Claude Code Project Preferences

## Git Commits
- Do NOT include "Co-Authored-By" in commit messages
- Keep commit messages concise and descriptive

## Environment Variables
- Never hardcode project IDs or API keys in source files
- Always use environment variables for sensitive configuration
- GOOGLE_CLOUD_PROJECT must be set via .env file
- .env files are gitignored and should never be committed

## Project Structure
- Vendors are in vendors/ directory (restaurant, electronics, travel)
- Concierge orchestrator is in concierge/ directory
- Common utilities are in common/ directory
- All agents use Vertex AI via GOOGLE_GENAI_USE_VERTEXAI=TRUE
