#!/bin/bash
# Test runner script for the PII redaction function app.
# Provides easy commands to run different types of tests.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Change to the project root directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    print_status "Virtual environment activated"
else
    print_error "Virtual environment not found. Run: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Parse command line arguments
case "${1:-help}" in
    "pii")
        print_status "Running PII detection module tests..."
        cd tests && python test_pii_module.py
        ;;
    "function")
        print_status "Running HTTP function endpoint tests..."
        print_warning "Make sure the Azure Functions host is running: func host start"
        cd tests && python test_function.py
        ;;
    "all")
        print_status "Running all tests..."
        echo
        print_status "1. Testing PII detection module..."
        cd tests && python test_pii_module.py
        echo
        print_status "2. Testing HTTP function endpoint..."
        print_warning "Make sure the Azure Functions host is running: func host start"
        python test_function.py
        ;;
    "help"|*)
        echo "Usage: $0 [command]"
        echo
        echo "Commands:"
        echo "  pii       Test the PII detection module only"
        echo "  function  Test the HTTP function endpoint (requires running host)"
        echo "  all       Run all tests"
        echo "  help      Show this help message"
        echo
        echo "Prerequisites:"
        echo "  - Virtual environment activated"
        echo "  - Dependencies installed: pip install -r requirements.txt"
        echo "  - Azure AI Language configured (for real PII detection)"
        echo "  - Azurite running (for function tests): azurite --location ./azurite"
        echo "  - Functions host running (for function tests): func host start"
        ;;
esac