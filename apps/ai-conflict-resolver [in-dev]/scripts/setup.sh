#!/bin/bash

# AI Conflict Resolver Setup Script
# This script helps set up the AI Conflict Resolver service

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🤖 AI Conflict Resolver Setup"
echo "============================="

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command_exists node; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ npm is not installed. Please install npm"
    exit 1
fi

if ! command_exists docker; then
    echo "⚠️  Docker is not installed. You won't be able to build Docker images"
fi

if ! command_exists kubectl; then
    echo "⚠️  kubectl is not installed. You won't be able to deploy to Kubernetes"
fi

echo "✅ Prerequisites check complete"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
cd "$PROJECT_DIR"
npm install

# Set up environment file
echo ""
echo "🔧 Setting up environment configuration..."

if [ ! -f "$PROJECT_DIR/.env" ]; then
    cp "$PROJECT_DIR/env.template" "$PROJECT_DIR/.env"
    echo "✅ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and add your credentials:"
    echo "   - GitHub App credentials"
    echo "   - Claude API key"
    echo "   - JIRA credentials"
    echo "   - Slack/Email settings (optional)"
    echo ""
    read -p "Press Enter to open .env in your editor..."
    ${EDITOR:-nano} "$PROJECT_DIR/.env"
else
    echo "✅ .env file already exists"
fi

# Validate environment
echo ""
echo "🔍 Validating environment configuration..."

required_vars=(
    "GITHUB_APP_ID"
    "GITHUB_PRIVATE_KEY"
    "GITHUB_CLIENT_ID"
    "GITHUB_CLIENT_SECRET"
    "CLAUDE_API_KEY"
    "JIRA_BASE_URL"
    "JIRA_EMAIL"
    "JIRA_API_TOKEN"
)

missing_vars=()
source "$PROJECT_DIR/.env"

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "❌ Missing required environment variables:"
    printf '%s\n' "${missing_vars[@]}"
    echo ""
    echo "Please edit .env and add the missing values"
    exit 1
fi

echo "✅ Environment configuration valid"

# GitHub App setup instructions
echo ""
echo "📱 GitHub App Setup"
echo "==================="
echo ""
echo "If you haven't created a GitHub App yet:"
echo "1. Go to: https://github.com/settings/apps/new"
echo "2. Set the following:"
echo "   - Webhook URL: https://your-domain.com/webhook"
echo "   - Webhook secret: (generate a random string)"
echo "   - Permissions:"
echo "     • Repository: Contents (Read & Write)"
echo "     • Repository: Pull requests (Read & Write)"
echo "     • Repository: Issues (Read & Write)"
echo "     • Repository: Checks (Read & Write)"
echo "   - Subscribe to events:"
echo "     • Pull request"
echo "     • Pull request review"
echo "     • Issue comment"
echo "3. Generate and download the private key"
echo "4. Install the app on your repository"
echo ""

# Test run
echo "🧪 Running tests..."
npm test || echo "⚠️  Some tests failed. Please check the output above."

# Build Docker image (optional)
if command_exists docker; then
    echo ""
    read -p "Build Docker image? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🐳 Building Docker image..."
        docker build -t ai-conflict-resolver "$PROJECT_DIR"
        echo "✅ Docker image built successfully"
    fi
fi

# Kubernetes deployment (optional)
if command_exists kubectl; then
    echo ""
    read -p "Deploy to Kubernetes? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "☸️  Setting up Kubernetes deployment..."
        
        # Create namespace
        kubectl create namespace ai-tools --dry-run=client -o yaml | kubectl apply -f -
        
        # Create secrets
        kubectl create secret generic ai-conflict-resolver-secrets \
            --from-env-file="$PROJECT_DIR/.env" \
            --namespace=ai-tools \
            --dry-run=client -o yaml | kubectl apply -f -
        
        # Apply deployment
        kubectl apply -f "$PROJECT_DIR/k8s/deployment.yaml"
        
        echo "✅ Deployed to Kubernetes"
        echo ""
        echo "Check deployment status:"
        echo "  kubectl get pods -n ai-tools"
        echo "  kubectl logs -n ai-tools -l app=ai-conflict-resolver"
    fi
fi

# Start locally
echo ""
echo "🚀 Setup complete!"
echo ""
echo "To start the service locally:"
echo "  npm start"
echo ""
echo "To start in development mode:"
echo "  npm run dev"
echo ""
echo "To run with Docker:"
echo "  docker run -p 3000:3000 --env-file .env ai-conflict-resolver"
echo ""
echo "📖 See README.md for more information"
