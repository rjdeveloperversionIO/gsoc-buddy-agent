#!/bin/bash

# github-api.sh - Reusable GitHub API interaction script
# Usage: ./github-api.sh <endpoint> [method] [data]
# Example: ./github-api.sh /repos/zulip/zulip/issues GET

# Configuration
API_BASE="https://api.github.com"
MAX_RETRIES=3
RETRY_DELAY=5

# Check if GITHUB_TOKEN is set
if [ -z "$GITHUB_TOKEN" ]; then
  echo "Error: GITHUB_TOKEN environment variable is not set"
  exit 1
fi

# Parse arguments
ENDPOINT=$1
METHOD=${2:-GET}
DATA=${3:-""}

# Function to make API request with retries and rate limit handling
github_api_request() {
  local endpoint=$1
  local method=$2
  local data=$3
  local retry_count=0
  local response=""
  
  while [ $retry_count -lt $MAX_RETRIES ]; do
    # Check rate limit before making request
    local rate_limit=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                      "$API_BASE/rate_limit" | jq -r '.rate.remaining')
    
    # If rate limit is low, wait until reset
    if [ "$rate_limit" -lt 10 ]; then
      local reset_time=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
                        "$API_BASE/rate_limit" | jq -r '.rate.reset')
      local current_time=$(date +%s)
      local wait_time=$((reset_time - current_time + 10))
      
      echo "Rate limit almost reached ($rate_limit remaining). Waiting $wait_time seconds..."
      sleep $wait_time
    fi
    
    # Make the API request
    if [ "$method" = "GET" ]; then
      response=$(curl -s -w "\n%{http_code}" -H "Authorization: token $GITHUB_TOKEN" \
                "$API_BASE$endpoint")
    else
      response=$(curl -s -w "\n%{http_code}" -X "$method" -H "Authorization: token $GITHUB_TOKEN" \
                -H "Content-Type: application/json" -d "$data" \
                "$API_BASE$endpoint")
    fi
    
    # Extract HTTP status code and response body
    local status_code=$(echo "$response" | tail -n1)
    local body=$(echo "$response" | sed '$d')
    
    # Check for success
    if [ "$status_code" -ge 200 ] && [ "$status_code" -lt 300 ]; then
      echo "$body"
      return 0
    fi
    
    # Handle specific error cases
    if [ "$status_code" -eq 403 ] && echo "$body" | grep -q "API rate limit exceeded"; then
      local reset_time=$(echo "$body" | jq -r '.rate.reset')
      local current_time=$(date +%s)
      local wait_time=$((reset_time - current_time + 10))
      
      echo "Rate limit exceeded. Waiting $wait_time seconds..."
      sleep $wait_time
      continue
    fi
    
    if [ "$status_code" -eq 401 ]; then
      echo "Error: Authentication failed. Check your token."
      echo "$body"
      return 1
    fi
    
    # For other errors, retry after delay
    echo "Request failed with status $status_code. Retrying in $RETRY_DELAY seconds..."
    echo "$body"
    sleep $RETRY_DELAY
    retry_count=$((retry_count + 1))
  done
  
  echo "Error: Maximum retries reached. Last response:"
  echo "$body"
  return 1
}

# Make the API request
github_api_request "$ENDPOINT" "$METHOD" "$DATA"
