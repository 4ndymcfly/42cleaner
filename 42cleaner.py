#!/usr/bin/env python3

import os
import psutil
import subprocess
from glob import glob
from time import sleep
import argparse

# Color functions
def color(txt: str, code: str) -> str:
    return f"\033[{code}m{txt}\033[97m"

def show_banner() -> None:
    if not args.silent:
        banner = """\033[93m
  ____ ___      __
 / / /|_  |____/ /__ ___ ____  ___ ____
/_  _/ __// __/ / -_) _ `/ _ \\/ -_) __/
/_//____/\\__/_/\\__/\\_,_/_//_/\\__/_/
\033[91m                       by WildZarek

\033[94m42cleaner\033[96m | Cleaner script for 42 students.\033[97m

>> Run the script with -h or --help for more information.
"""
        os.system("clear")
        print(banner)

def parse_args():
    parser = argparse.ArgumentParser(description="Cleaner script for 42 students.")
    parser.add_argument("-s", "--silent", action="store_true", help="run the script in silent mode without prompts")
    return parser.parse_args()

args = parse_args()

def exec_command(command: list) -> str:
    return subprocess.run(command, stdout=subprocess.PIPE).stdout.decode().strip()

def show_space(usr: str) -> str:
    home = psutil.disk_usage(f"/home/{usr}/")
    used = round(home.percent)
    return f"{color(f'{used}%', '91')} {color('used', '91')} / {color(f'{100 - used}%', '92')} {color('free', '92')}"

def clean() -> None:
    usr = exec_command(["whoami"])

    # Check if cleanup is necessary
    if psutil.disk_usage(f"/home/{usr}/").percent <= 60:
        if not args.silent:
            print(f"\nNothing to clean.\nSpace: {show_space(usr)}")
            print(f"\nExiting...")
        return

    # Check for 'rm' binary
    rm_bin = exec_command(["which", "rm"])
    if not rm_bin:
        if not args.silent:
            print(f"{color('Error', '91')}: {color('rm binary not found.', '96')}")
        return

    # Paths for trash files
    trash_paths = [
        f"/home/{usr}/.local/share/Trash/*",
        f"/home/{usr}/.zcompdump*",
        f"/home/{usr}/.cache/*",
        f"/home/{usr}/.config/Code/Cache/*",
        f"/home/{usr}/.config/Code/CachedData/*",
        f"/home/{usr}/francinette/temp/*",
    ]

    snap_deleted_files_count = 0

    # Cleanup snap-related files
    for pkg in glob(f"/home/{usr}/snap/*"):
        if pkg.endswith("firefox") or pkg.endswith("slack"):
            cache_files = glob(f"{pkg}/common/.cache/*")
            snap_deleted_files_count += len(cache_files)
            os.system(f"rm -rf {pkg}/common/.cache/*")
        versions = [v for v in os.listdir(pkg) if v not in {"common", "current"}]
        if len(versions) > 1:
            for v in sorted(versions)[:-1]:
                snap_deleted_files_count += sum(len(f) for _, _, f in os.walk(f"{pkg}/{v}"))
                os.system(f"rm -rf {pkg}/{v}")

    # Count trash files
    trash_files_count = sum(len(glob(path)) for path in trash_paths)

    # Total files deleted
    total_deleted_files_count = snap_deleted_files_count + trash_files_count

    if total_deleted_files_count == 0:
        if not args.silent:
            print(f"[{color('i', '94')}] No trash files found.")
    else:
        if not args.silent:
            print(f"[{color('!', '93')}] Cleaning trash files...")
        for path in trash_paths:
            os.system(f"{rm_bin} -rf {path}")
        if not args.silent:
            sleep(2)
            print(f"[{color('-', '91')}] Deleted {color(str(total_deleted_files_count), '93')} files.")
            print(f"[{color('i', '94')}] Disk usage after clean: {show_space(usr)}")

def show_menu():
    print("Please choose an option:\n")
    print(f"1.{color(' Create a scheduled task', '94')}")
    print(f"2.{color(' Remove a scheduled task', '94')}")
    print(f"3.{color(' Run the script now', '94')}")
    print(f"q.{color(' Quit', '94')}")

    choice = input("\nEnter your choice (1/2/3/q): ").strip().lower()

    return choice

def schedule_task() -> None:
    if args.silent:
        return  # Skip task scheduling in silent mode

    choice = show_menu()

    usr = exec_command(["whoami"])
    script_path = os.path.abspath(__file__)
    cron_line = f"{script_path} --silent &> /dev/null"

    if choice == '1':
        current_cron = exec_command(["crontab", "-l"])
        if cron_line in current_cron:
            print(f"\n{color('Info', '94')}: A scheduled task already exists for this script.")
            return

        interval_options = {
            '1': "*/6 * * * *",
            '2': "*/8 * * * *",
            '3': "*/12 * * * *"
        }
        print("\nChoose an interval for the scheduled task:\n")
        print(f"1.{color(' Every 6 hours', '94')}")
        print(f"2.{color(' Every 8 hours', '94')}")
        print(f"3.{color(' Every 12 hours', '94')}")

        interval_choice = input("\nEnter your choice (1/2/3): ").strip()
        interval = interval_options.get(interval_choice)
        if not interval:
            print(f"\n{color('Error', '91')}: Invalid choice.")
            return

        full_cron_line = f"{interval} {cron_line}"
        os.system(f"(crontab -l; echo '{full_cron_line}') | crontab -")
        print(f"\n{color('Success', '92')}: Scheduled task created to run every {interval} hours.")

    elif choice == '2':
        current_cron = exec_command(["crontab", "-l"])
        if cron_line not in current_cron:
            print(f"\n{color('Info', '94')}: No scheduled task found for this script.")
        else:
            new_cron = "\n".join([line for line in current_cron.splitlines() if cron_line not in line])
            os.system(f"echo '{new_cron}' | crontab -")
            print(f"\n{color('Success', '92')}: Scheduled task removed.")

    elif choice == '3':
        clean()

    elif choice == 'q':
        print(f"\nBye!")

if __name__ == "__main__":
    show_banner()
    schedule_task()
