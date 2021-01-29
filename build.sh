#!/usr/bin/env bash
set -e
echo ""
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "🔥Formatting code.🔥" 
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo ""
black --line-length 80 sureconnect.py
echo ""
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "🔥 Checking types.🔥" 
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo ""
echo "Skipping: mypy sureconnect.py"
echo ""
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "🔥Linting styles. 🔥" 
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo ""
echo "Skipping: pylint sureconnect.py"
echo ""
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "🔥 Running tests. 🔥" 
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo ""
python sureconnect.py
echo ""
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo "🔥  Build passed! 🔥" 
echo "🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥"
echo ""
echo " ✅ Light is green!"
echo " ✅ Build ran clean!"
echo " ✅ All the code"
echo "        is"
echo "   Lean and mean!"
echo ""
