# About
A Python3 script to get info about repositories in https://github.com/github. It results in csv-file, containing
- Name of a repo
- Short description
- Url
- Programming language
- List of tags

![Image](https://raw.githubusercontent.com/SvyatSheypak/webscrapping_github/master/screenshot.png)

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
It creates a `out.csv` file. 

# Options
`-f, --file` 
        
   Output file name or path to output file (all directories should already exist). Default: `out.csv`
        
`-u, --url`
        
   Url to scrap, no guarantee on urls other than https://github.com/github

`-h, --help`

   Display this help and exit
