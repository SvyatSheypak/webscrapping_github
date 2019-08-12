# About
A Python3 script to get info about repositories in https://github.com/github. It results in csv-file, containing
- Name of a repo
- Short description
- Url
- Programming language
- List of tags

This script goes through all the pages of https://github.com/github and parses them.

# Requirements
Script requires Python3 with modules `bs4` and `requests` installed. It also uses  `argparse` and `contextlib`, but they should be installed by default.
```
pip3 install bs4
pip3 install requests
```

# Run
```
python3 webscrap.py
```
It creates a `out.csv` file. You can write in a custom file using `-f` option. Link https://github.com/github can be substituted by any link via `-u` option, however, there is no guarantees on performance of the script in this case.
