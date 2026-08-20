# Add dotenv to deps
uv add python-dotenv

# Create .env at project root (not committed to git)
touch .env

# Create .env.example (committed to git, shows required vars)
touch .env.example

# Make sure .env is gitignored
echo ".env" >> .gitignore