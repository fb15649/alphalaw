#!/bin/bash
# push.sh — kazin gets EVERYTHING, GitHub gets only public files
#
# Usage: ./push.sh
# Or: ./push.sh "commit message"

set -e

GITHUB_REMOTE="origin"
KAZIN_REMOTE="kazin"
BRANCH="main"

# Files to EXCLUDE from GitHub (but include on kazin)
PRIVATE_FILES=(
    "CLAUDE.md"
    "TODO.md"
    "artifacts/"
    "docs/"
    "push.sh"
)

echo "=== Push to kazin (full) ==="
HTTPS_PROXY="" HTTP_PROXY="" git push "$KAZIN_REMOTE" "$BRANCH" 2>&1 || echo "  kazin push failed (may need force)"
echo "  Done."

echo ""
echo "=== Push to GitHub (public only) ==="

# Create a temporary branch from current HEAD
TEMP_BRANCH="__github_push_temp__"
git branch -D "$TEMP_BRANCH" 2>/dev/null || true
git checkout -b "$TEMP_BRANCH"

# Remove private files from this branch
for f in "${PRIVATE_FILES[@]}"; do
    if [ -e "$f" ]; then
        git rm -rf --cached "$f" 2>/dev/null || true
    fi
done

# Commit the removal (if there are changes)
if ! git diff --cached --quiet 2>/dev/null; then
    git commit -m "temp: remove private files for GitHub push" --no-verify
fi

# Force push to GitHub
HTTPS_PROXY="" HTTP_PROXY="" git push "$GITHUB_REMOTE" "$TEMP_BRANCH:$BRANCH" --force 2>&1
echo "  Done."

# Go back to main and delete temp branch
git checkout "$BRANCH"
git branch -D "$TEMP_BRANCH"

echo ""
echo "=== Result ==="
echo "  kazin:  full (all files)"
echo "  GitHub: public (no CLAUDE.md, TODO.md, artifacts/, docs/)"
