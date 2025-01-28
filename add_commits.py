#!/usr/bin/env python3
import os
import sys
from datetime import datetime
import subprocess

def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        print("Incorrect date format, should be YYYY-MM-DD")
        sys.exit(1)

def create_commits(date, num_commits):
    # Ensure the date is in the correct format
    date_obj = validate_date(date)
    date_str = date_obj.strftime('%Y-%m-%d')
    
    for i in range(num_commits):
        # Create a new file or modify existing one
        timestamp = datetime.now().timestamp()
        with open('commit.txt', 'w') as f:
            f.write(f'Commit {i+1} at {timestamp}')
        
        # Stage the file
        subprocess.run(['git', 'add', 'commit.txt'])
        
        # Create the commit with the specified date
        env = os.environ.copy()
        env['GIT_AUTHOR_DATE'] = f'{date_str}T12:00:00'
        env['GIT_COMMITTER_DATE'] = f'{date_str}T12:00:00'
        
        subprocess.run(['git', 'commit', '-m', f'Update {i+1} for {date_str}'], env=env)

def main():
    # Get user input
    date = input("Enter the date for commits (YYYY-MM-DD): ")
    while True:
        try:
            num_commits = int(input("How many commits do you want to add? "))
            if num_commits > 0:
                break
            print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")

    # Create the commits
    create_commits(date, num_commits)
    
    print(f"\nCreated {num_commits} commits for {date}")
    print("\nTo push changes:")
    print("git push origin master")

if __name__ == "__main__":
    main()