"""
AudioDotTurn is a tool for formatting and organizing audio files with little to no metadata available. It provides a solution
for situations where there are tons of unstandardized, unorganized files with little to no metadata, and sorting via metadata
is not an option. With AudioDotTurn, users can quickly format a single file or a whole directory/subdirectories to the style of
their choosing. 

The tool creates a database for the user, which can be accessed via AudioDotTurn or any program that will interpret sql .db files.
The database will be updated as new files are formatted as long as the db file is selected as the default db or selected at runtime.

Usage:
- Users can change settings via CLI
- AudioDotTurn uses pretty output via rich for visually appealing output
- Dry run mode available for seeing results of a run without making any actual changes
- When formatting an entire directory, users can produce a report of the results in an MD file or simply print them to the console if either are desired.

TODO:
- Add more detailed information regarding how to use AudioDotTurn.
"""
__version__ = VERSION = '0.4.0'
