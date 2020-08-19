source ./bin/activate
python3 get_files_not_migrated.py > last_output
deactivate
cat last_output | mail -s "Last output of migration" stefan@schmidbauer.cz
