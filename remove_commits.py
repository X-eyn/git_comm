#!/usr/bin/env python3
import subprocess
import random
from datetime import datetime

def get_commits_for_date(date_str):
    # Get all commits for the specified date
    cmd = ['git', 'log', '--format=%H', f'--before={date_str}T23:59:59', f'--after={date_str}T00:00:00']
    result = subprocess.run(cmd, capture_output=True, text=True)
    commits = result.stdout.strip().split('\n')
    return [c for c in commits if c]  # Remove empty strings

def remove_commits(date, num_commits_to_remove):
    # Format date
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        date_str = date_obj.strftime('%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD")
        return

    # Get commits for the date
    commits = get_commits_for_date(date_str)
    
    if not commits:
        print(f"No commits found for date {date_str}")
        return
    
    total_commits = len(commits)
    if num_commits_to_remove > total_commits:
        print(f"Can only remove {total_commits} commits from {date_str}")
        num_commits_to_remove = total_commits
    
    # Sort commits chronologically (oldest first)
    commits.reverse()
    
    # Keep the first (oldest) commits and remove the rest
    commits_to_keep = commits[:total_commits - num_commits_to_remove]
    
    if commits_to_keep:
        # Reset to the last commit we want to keep
        last_keep_commit = commits_to_keep[-1]
        subprocess.run(['git', 'reset', '--hard', last_keep_commit])
    else:
        # If removing all commits for that day, reset to the day before
        cmd = ['git', 'log', '--format=%H', '--reverse', f'--before={date_str}T00:00:00', '-1']
        result = subprocess.run(cmd, capture_output=True, text=True)
        previous_commit = result.stdout.strip()
        if previous_commit:
            subprocess.run(['git', 'reset', '--hard', previous_commit])
    
    print(f"\nSuccessfully removed {num_commits_to_remove} commits from {date_str}")
    print(f"Remaining commits for this date: {total_commits - num_commits_to_remove}")
    print("\nTo update GitHub, run:")
    print("git push origin master --force")

def main():
    date = input("Enter the date to remove commits from (YYYY-MM-DD): ")
    while True:
        try:
            num_commits = int(input("How many commits do you want to remove? "))
            if num_commits > 0:
                break
            print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")

    remove_commits(date, num_commits)

if __name__ == "__main__":
    main()