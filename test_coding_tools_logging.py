"""
Test script to demonstrate the logging functionality for coding agent tools.

This script tests each coding tool individually to show how logging works.
Run this to verify that all coding tools are properly logging their calls and outputs.
"""

from tools.coding.code_analysis import analyze_python_file
from tools.coding.filesystem import list_files, read_files


def test_coding_tools():
    """Test all coding tools to demonstrate logging functionality."""
    
    print("\n" + "="*70)
    print("TESTING CODING TOOLS WITH LOGGING")
    print("="*70 + "\n")
    
    print("Check the logs/ directory for detailed log files!")
    print("Console output shows INFO level, files contain DEBUG level.\n")
    
    # Test 1: List Files
    print("\n[TEST 1] Testing list_files tool...")
    try:
        result = list_files.invoke({"directory": "."})
        print(f"✓ list_files completed - found items in current directory")
    except Exception as e:
        print(f"✗ list_files failed: {e}")
    
    # Test 2: List Files in subdirectory
    print("\n[TEST 2] Testing list_files for tools/ directory...")
    try:
        result = list_files.invoke({"directory": "tools"})
        print(f"✓ list_files completed for tools/ directory")
    except Exception as e:
        print(f"✗ list_files failed: {e}")
    
    # Test 3: List Files - Non-existent directory
    print("\n[TEST 3] Testing list_files with non-existent directory...")
    try:
        result = list_files.invoke({"directory": "non_existent_dir"})
        print(f"✓ list_files handled non-existent directory gracefully")
    except Exception as e:
        print(f"✗ list_files failed: {e}")
    
    # Test 4: Read Files - README
    print("\n[TEST 4] Testing read_files tool with README.md...")
    try:
        result = read_files.invoke({"file_path": "README.md"})
        print(f"✓ read_files completed - read README.md")
    except Exception as e:
        print(f"✗ read_files failed: {e}")
    
    # Test 5: Read Files - Python file
    print("\n[TEST 5] Testing read_files with config/settings.py...")
    try:
        result = read_files.invoke({"file_path": "config/settings.py"})
        print(f"✓ read_files completed - read config/settings.py")
    except Exception as e:
        print(f"✗ read_files failed: {e}")
    
    # Test 6: Read Files - Non-existent file
    print("\n[TEST 6] Testing read_files with non-existent file...")
    try:
        result = read_files.invoke({"file_path": "non_existent_file.py"})
        print(f"✓ read_files handled non-existent file gracefully")
    except Exception as e:
        print(f"✗ read_files failed: {e}")
    
    # Test 7: Analyze Python File - Valid file
    print("\n[TEST 7] Testing analyze_python_file with config/settings.py...")
    try:
        result = analyze_python_file.invoke({"file_path": "config/settings.py"})
        print(f"✓ analyze_python_file completed - analyzed config/settings.py")
    except Exception as e:
        print(f"✗ analyze_python_file failed: {e}")
    
    # Test 8: Analyze Python File - Another valid file
    print("\n[TEST 8] Testing analyze_python_file with main.py...")
    try:
        result = analyze_python_file.invoke({"file_path": "main.py"})
        print(f"✓ analyze_python_file completed - analyzed main.py")
    except Exception as e:
        print(f"✗ analyze_python_file failed: {e}")
    
    # Test 9: Analyze Python File - Non-existent file
    print("\n[TEST 9] Testing analyze_python_file with non-existent file...")
    try:
        result = analyze_python_file.invoke({"file_path": "non_existent.py"})
        print(f"✓ analyze_python_file handled non-existent file gracefully")
    except Exception as e:
        print(f"✗ analyze_python_file failed: {e}")
    
    # Test 10: Analyze Python File - Invalid syntax
    print("\n[TEST 10] Testing analyze_python_file with invalid Python syntax...")
    try:
        # Create a temporary file with invalid syntax
        with open("temp_invalid.py", "w") as f:
            f.write("def invalid_function(\n    # Missing closing parenthesis")
        
        result = analyze_python_file.invoke({"file_path": "temp_invalid.py"})
        print(f"✓ analyze_python_file handled syntax error gracefully")
        
        # Clean up
        import os
        os.remove("temp_invalid.py")
    except Exception as e:
        print(f"✗ analyze_python_file failed: {e}")
        # Clean up
        try:
            import os
            os.remove("temp_invalid.py")
        except:
            pass
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print("="*70)
    print("\nAll tool calls and outputs have been logged!")
    print("Check the logs/ directory for the complete log file.")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_coding_tools()
