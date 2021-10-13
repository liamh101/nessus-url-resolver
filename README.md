# Nessus Resolver

This script takes .nessus xml files and turns short urls normally seen in `<also seen>` section and resolves them to their full length equivalent.

# How to use

Pass .nessus file location into script.

`python3 resolver.py test.nessus`

The script will run and output the number of found references, the current reference it has resolved, replacing found references and removing invalid references. 

After the script has run it will output a copy of the original file with the new references. The script will **not** replace your original file.

## Feedback And Future Features

Please feel free to leave feedback, bugs and feature requests. 

Currently I'd like to add the following:

- [] Improve reference regex
- [] Script outputs copy of file with original filename referenced
- [] optional verbose levels
