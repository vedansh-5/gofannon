#!/bin/bash  
set -euo pipefail  
  
# Get parameters from environment  
AUTHOR="$1"  
PR_NUMBER="$2"  
REPO="$3"  
GITHUB_TOKEN="$4"  
  
# Search for merged PRs by this author  
SEARCH_URL="https://api.github.com/search/issues?q=is:merged+is:pr+author:${AUTHOR}+repo:${REPO}"  
echo "Checking for merged PRs: ${SEARCH_URL}"  
  
# Make API request  
RESPONSE=$(curl -s -H "Authorization: token ${GITHUB_TOKEN}" -H "Accept: application/vnd.github.v3+json" "${SEARCH_URL}")  
  
# Parse response  
COUNT=$(echo "$RESPONSE" | jq -r '.total_count')  
  
if [ "$COUNT" -eq 0 ]; then  
    echo "First-time contributor detected! Adding label..."  
    curl -s -X POST \  
        -H "Authorization: token ${GITHUB_TOKEN}" \  
        -H "Accept: application/vnd.github.v3+json" \  
        "https://api.github.com/repos/${REPO}/issues/${PR_NUMBER}/labels" \  
        -d '{"labels":["first time contributor"]}'  
else  
    echo "User has ${COUNT} merged PRs - not a first-time contributor"  
fi  
