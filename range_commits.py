#!/usr/bin/env python3
import subprocess
import random
from datetime import datetime, timedelta
import math

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD")
        return None

def is_weekend(date):
    return date.weekday() >= 5

def distribute_commits(start_date, end_date, total_commits):
    date_range = (end_date - start_date).days + 1
    if date_range <= 0:
        print("End date must be after start date")
        return None
    
    # Calculate working days and weekend days
    working_days = sum(1 for i in range(date_range) if not is_weekend(start_date + timedelta(days=i)))
    weekend_days = date_range - working_days
    
    # Allocate more commits to working days (70-30 ratio)
    weekday_commits = int(total_commits * 0.7)
    weekend_commits = total_commits - weekday_commits
    
    # Create daily commit distribution
    daily_commits = {}
    current_date = start_date
    
    # First pass: distribute base commits
    while current_date <= end_date:
        is_weekend_day = is_weekend(current_date)
        if is_weekend_day and weekend_commits > 0:
            # Weekend days get fewer commits
            base_commits = max(1, min(3, weekend_commits // (weekend_days or 1)))
            daily_commits[current_date] = base_commits
            weekend_commits -= base_commits
            weekend_days = max(1, weekend_days - 1)
        elif not is_weekend_day and weekday_commits > 0:
            # Weekdays get more commits
            base_commits = max(1, min(5, weekday_commits // (working_days or 1)))
            daily_commits[current_date] = base_commits
            weekday_commits -= base_commits
            working_days = max(1, working_days - 1)
        current_date += timedelta(days=1)
    
    # Second pass: distribute remaining commits randomly but weighted
    remaining_commits = weekday_commits + weekend_commits
    dates_list = list(daily_commits.keys())
    
    while remaining_commits > 0:
        # Weight selection towards days with fewer commits
        weights = [1.0 / (daily_commits[date] + 1) for date in dates_list]
        total_weight = sum(weights)
        weights = [w/total_weight for w in weights]
        
        selected_date = random.choices(dates_list, weights=weights)[0]
        daily_commits[selected_date] += 1
        remaining_commits -= 1
    
    return daily_commits

def create_commit(date, commit_number):
    timestamp = date.strftime('%Y-%m-%d %H:%M:%S')
    hour = random.randint(9, 17)  # Commits between 9 AM and 5 PM
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    
    # Create a unique commit message and content
    with open('commit.txt', 'w') as f:
        f.write(f'Update for {timestamp} - {commit_number}')
    
    # Stage and commit with the specified date
    subprocess.run(['git', 'add', 'commit.txt'])
    commit_date = f"{date.strftime('%Y-%m-%d')} {hour:02d}:{minute:02d}:{second:02d}"
    env = {
        **os.environ,
        'GIT_AUTHOR_DATE': commit_date,
        'GIT_COMMITTER_DATE': commit_date
    }
    subprocess.run(['git', 'commit', '-m', f'Update {commit_number} for {date.strftime("%Y-%m-%d")}'], env=env)

def main():
    print("Enter date range (YYYY-MM-DD):")
    start_date_str = input("Start date: ")
    end_date_str = input("End date: ")
    
    start_date = parse_date(start_date_str)
    end_date = parse_date(end_date_str)
    
    if not start_date or not end_date:
        return
    
    while True:
        try:
            total_commits = int(input("How many commits to add? "))
            if total_commits > 0:
                break
            print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")
    
    # Get commit distribution
    distribution = distribute_commits(start_date, end_date, total_commits)
    if not distribution:
        return
    
    # Create commits according to distribution
    total_created = 0
    for date, num_commits in sorted(distribution.items()):
        for i in range(num_commits):
            create_commit(date, total_created + 1)
            total_created += 1
    
    print(f"\nSuccessfully created {total_created} commits across {len(distribution)} days")
    print("\nCommit distribution:")
    for date, count in sorted(distribution.items()):
        print(f"{date.strftime('%Y-%m-%d')}: {count} commits")
    
    print("\nTo update GitHub, run:")
    print("git push origin master --force")

if __name__ == "__main__":
    import os
    main()