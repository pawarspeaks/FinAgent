import sys
print(f"Python version: {sys.version}")

try:
    import numpy as np
    print(f"NumPy version: {np.__version__}")
    print("NumPy imported successfully")
    
    # Try a simple NumPy operation
    arr = np.array([1, 2, 3, 4, 5])
    print(f"NumPy array: {arr}")
    print(f"Mean of array: {np.mean(arr)}")
except ImportError as e:
    print(f"Failed to import NumPy: {e}")
except Exception as e:
    print(f"An error occurred: {e}")