"""
Test simple del sistema DHL
"""
print("🚚 DHL Order Processing System v2.0")
print("💻 Created by Lucas Gnemmi")
print("🧪 Testing imports...")

try:
    import tkinter as tk
    print("✅ tkinter - OK")
except Exception as e:
    print(f"❌ tkinter - Error: {e}")

try:
    import pandas as pd
    print("✅ pandas - OK")
except Exception as e:
    print(f"❌ pandas - Error: {e}")

try:
    import openpyxl
    print("✅ openpyxl - OK")
except Exception as e:
    print(f"❌ openpyxl - Error: {e}")

try:
    import fitz  # PyMuPDF
    print("✅ PyMuPDF - OK")
except Exception as e:
    print(f"❌ PyMuPDF - Error: {e}")

try:
    import xlwings as xw
    print("✅ xlwings - OK")
except Exception as e:
    print(f"❌ xlwings - Error: {e}")

print("\n🔧 System test completed!")
print("👨‍💻 If all imports show OK, the system is ready to use.")