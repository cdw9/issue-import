# Issue Import

Script to import Game Plans into GitHub Issues

Note: script is meant to be run once. Running again against the same data will result in duplicate Issues.

## 1. Prepare the data

* From the Game Plan, export as CSV. From Google, File > Download > CSV
* Edit the CSV
  * Remove the first few lines. The first line should be the column headings (Component, User Story, Requirements, etc)
  * Remove all lines after the last estimate
  * Remove any lines that should not be made into an Issue
* **Make sure the columns are in this order!** The script will currently assume the order, regardless of headings. Any further columns will be ignored.
  * Component
  * User Story
  * Requirements
  * Tasks
  * Complexity Points

See sample.csv for an example

## 2. Prepare the Project

The issues will need to be attached to a GitHub Project. You will need to set up the Project prior to importing.

* Set a workflow on the Project so Issues from your repo will be automatically added
* Make sure all necessary fields are available (Estimated Remaining, Time Spent, etc). This should be the case if you created the Project from the Six Feet Up Template. These field names are used in fields.py
* Make sure the Components in the Game Plan match the components in the Project
* Default values for the fields are set in fields.py

## 3. Run the import

* `url` will be for the Repository where the Issues will live. ex: <https://github.com/sixfeetup/pmtest>
* `csv` will be the path to the csv on your machine

```
$ env/bin/python import.py [url] [csv]
```

# Initial Script Setup

You can create a GitHub token at <https://github.com/settings/tokens>.


```
$ python -m venv env
$ env/bin/pip install -r requirements.txt
$ cp env.py.example env.py  # edit to add GitHub key
```
