# Broken-Link-Checker
A quick python script that uses a breadth-first search to check if links are broken on any given site.

Only Supports Python3 with the lxml, requests, and HttpNtlmAuth properly installed with pip.

Use the console to type the first page of the site (typically landing page).
The script will use this text to determine if a link is apart of the site you are testing.

It will ask for a domain\name and a password. Leave blank if it is not applicable.

Script will execute and store any pages that returned an error code of 400 or higher in "BrokenLinksBFS.txt"

Script will store any pages that caused the script to crash (typically pages that timed out or denied access) in "ConnectionFailuresVFS.txt"

Feel free to edit the script in any way shape or form to facilitate your need.

This script does not account for anchors, _layouts, or any javascript files.
