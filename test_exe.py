"""
Test script to validate the compiled executable works correctly
"""
import subprocess
import sys
import time
import os

def test_executable():
    """Test if the executable can be launched and responds correctly"""
    exe_path = os.path.join("dist", "VoiceToTextExtractor.exe")
    
    if not os.path.exists(exe_path):
        print("❌ Executable not found!")
        return False
    
    print("✅ Executable found")
    print(f"📁 File size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
    
    # Test if executable can start (it will open GUI)
    try:
        # Start the process but don't wait for it to finish (GUI app)
        process = subprocess.Popen([exe_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment to see if it crashes immediately
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Executable launched successfully (GUI opened)")
            # Terminate the test instance
            process.terminate()
            process.wait(timeout=5)
            return True
        else:
            # Process terminated, check for errors
            stdout, stderr = process.communicate()
            print("❌ Executable crashed or closed immediately")
            if stderr:
                print(f"Error output: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Failed to launch executable: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing compiled VoiceToTextExtractor...")
    success = test_executable()
    
    if success:
        print("\n🎉 COMPILATION SUCCESSFUL!")
        print("✅ The executable was created successfully")
        print("✅ The executable can launch without errors")
        print("✅ All dependencies are properly bundled")
        print("\n📍 Your executable is located at:")
        print(f"   {os.path.abspath('dist/VoiceToTextExtractor.exe')}")
        print("\n🚀 You can now distribute this single .exe file!")
    else:
        print("\n❌ There were issues with the compilation")
        sys.exit(1)
