#!/bin/bash
# PythonAnywhere Setup Script - Copy paste this entire file!

echo "=========================================="
echo "🚀 Setting up Supplier Collector App"
echo "=========================================="

# Step 1: Clone repository
echo "📥 Cloning repository..."
cd ~
git clone https://github.com/shuvo8220/supplier-collector.git
cd supplier-collector

# Step 2: Install dependencies
echo "📦 Installing packages..."
pip3.10 install --user flask openpyxl

# Step 3: Create data directory
echo "📁 Creating data folder..."
mkdir -p data

# Step 4: Test if everything works
echo "✅ Testing imports..."
python3.10 -c "import flask; import openpyxl; print('✓ All packages working!')"

echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Go to Web tab"
echo "2. Add new web app → Manual configuration → Python 3.10"
echo "3. Set WSGI file (see WSGI_CONFIG.txt)"
echo "4. Set paths:"
echo "   Source: /home/YOUR_USERNAME/supplier-collector"
echo "   Working: /home/YOUR_USERNAME/supplier-collector"
echo "5. Click Reload button"
echo ""
