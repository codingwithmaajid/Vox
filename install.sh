#!/bin/bash

echo "Installing Vox..."

# Check Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is required but not installed."
    echo "Install it from https://python.org"
    exit 1
fi


# Clone the repo
git clone https://github.com/codingwithmaajid/Vox.git
cd vox


# Install dependencies
pip install -r requirements.txt

# Install vox as a command
pip install -e .

echo ""
echo "vox installed successfully!"
echo ""
echo "Get your free API key at https://console.groq.com"
echo "Then run: export VOX_GROQ_API_KEY=your-key-here"
echo ""
echo "Usage: vox --help"