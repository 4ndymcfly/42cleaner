# 42cleaner

42cleaner is a Python script designed to clean temp/cache files and unnecessary older versions from Snap.

It helps to free up disk space and maintain system performance.

Made for 42 students. Tested on **42 Málaga** school running **Linux/Ubuntu**. NOT for macOS.

<img src="assets/run2.png" alt="Script running" align="center" />

# Why?

Due to the limit of 5 GB size for 'home' directory and looking to provide a solution
for the problem with the Snap package manager which is not removing properly
old versions (revisions), this tool has born to solve that problem.

# Trash files

This tool removes the following files:

- Empties recycle bin (Trash).
- All .zcompdump files (A cache file used by compinit).
- All Cache files in our home (~/.cache)
- Cache files from vscode (~/.config/Code/Cache and ~/.config/Code/CachedData)
- Cache files from firefox (~/snap/firefox/common/.cache)
- Cache files from slack (~/snap/slack/common/.cache)
- All temp files created by Francinette. (~/francinette/temp)
- Older versions (revisions) from installed Snap packages.

# How to use

Clone this repository by using the following command:

```bash
git clone https://github.com/WildZarek/42cleaner.git
```

Then, move to the new downloaded folder:

```bash
cd 42cleaner
```

Finally, run the script (sudo permissions not needed):

```bash
python3 42cleaner.py
```

> [!NOTE]
> If the used space in your 'home' is under 60%, the tool doesn't do any operation.
>
> Otherwise, the tool performs the needed operations to free space.

# License

This work is published under the terms of **[42 Unlicense](https://github.com/gcamerli/42unlicense)**.
