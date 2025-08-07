#!/bin/bash

# Simple test script to verify table format generation
echo "🧪 Testing Table Format Generation"
echo "================================="

# Create session directory
SESSION_DIR="02-analysis/sessions/test_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$SESSION_DIR"

# Check which prompt will be used
if [ -f "02-analysis/prompts/table-format-test-generation.txt" ]; then
    echo "✅ Using improved table-format prompt"
    TEST_GEN_PROMPT=$(cat 02-analysis/prompts/table-format-test-generation.txt)
elif [ -f "02-analysis/prompts/style-aware-test-generation.txt" ]; then
    echo "⚠️  Falling back to style-aware prompt"
    TEST_GEN_PROMPT=$(cat 02-analysis/prompts/style-aware-test-generation.txt)
else
    echo "⚠️  Using basic test generation prompt"
    TEST_GEN_PROMPT=$(cat 02-analysis/prompts/test-generation.txt)
fi

echo "📝 Generating test plan with Claude..."

# Generate test plan
claude --print "$TEST_GEN_PROMPT" > "${SESSION_DIR}/test-plan-raw.md" 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Test plan generated successfully"
    
    # Check if it contains the correct table format
    if grep -q "| Test Steps | Expected Results |" "${SESSION_DIR}/test-plan-raw.md"; then
        echo "🎉 SUCCESS: Test plan contains correct table format!"
        echo "📋 Copying to final location..."
        cp "${SESSION_DIR}/test-plan-raw.md" "02-test-planning/test-plan.md"
        
        echo ""
        echo "📖 Preview of generated content:"
        echo "================================"
        head -30 "${SESSION_DIR}/test-plan-raw.md"
        echo "... (truncated)"
        
    else
        echo "❌ FAILED: Test plan does not contain correct table format"
        echo "📖 Generated content preview:"
        head -20 "${SESSION_DIR}/test-plan-raw.md"
    fi
else
    echo "❌ Test plan generation failed"
    cat "${SESSION_DIR}/test-plan-raw.md"
fi

echo ""
echo "🔍 Session files created in: $SESSION_DIR"