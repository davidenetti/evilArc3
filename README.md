# evilArc3
A Python3 porting of evilArc, an historic tool to create ZIP which contains a file that could be able to exploit a zip slip vulnerability.


# Usage
- "-p / --path"     Custom traversal path to prepend (e.g. "../../../../test")
- "-t / --target"   File to which the traversal path is applied
-  "-f / --output"   Output archive name
files...        One or more files to include in the archive

# Usage example
`python3 evilArc3.py -p "../../../../../ -t test.sh -f malicious.zip file1 file2"`

This will create a new ZIP file called "malicious.zip" which contains file1, file2 and the file ../../../../../test.sh.
