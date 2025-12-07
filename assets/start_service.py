#!/usr/bin/env python3
import subprocess
import sys

def run_command(cmd, cwd='.'):
    """Execute shell command and handle errors."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        return False

def main():
    print("🛑 Stopping all running Docker containers...")
    if not run_command("docker compose down -v"):
        sys.exit(1)
    
    print("\n🐳 Building and starting Docker services...")
    if not run_command("docker compose up --build -d --remove-orphans"):
        sys.exit(1)
    
    print("\n✅ Services started successfully!")

if __name__ == "__main__":
    main()
