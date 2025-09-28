export PGPASSWORD='1234'

# In zsh chmod +x script_import.sh and run ./script_import.sh

# the code -c "TRUNCATE shop2_coursesession;" will delete all records 
# in the table before importing


echo "Start import"

# Truncate tables with CASCADE
echo "Truncating tables..."
psql -U dbadmin -h localhost -d geostar_db -c "TRUNCATE TABLE socialaccount_socialapp_sites CASCADE;"
psql -U dbadmin -h localhost -d geostar_db -c "TRUNCATE TABLE django_site CASCADE;"
psql -U dbadmin -h localhost -d geostar_db -c "TRUNCATE TABLE socialaccount_socialapp CASCADE;"

# Importing data

echo "Importing data into django_site"
psql -U dbadmin -h localhost -d geostar_db -c "\COPY django_site FROM 'output_file_django_site.csv' WITH (FORMAT csv, HEADER);"

echo "Importing data into socialaccount_socialapp"
psql -U dbadmin -h localhost -d geostar_db -c "\COPY socialaccount_socialapp FROM 'output_file_socialaccount_socialapp.csv' WITH (FORMAT csv, HEADER);"

echo "Importing data into socialaccount_socialapp_sites"
psql -U dbadmin -h localhost -d geostar_db -c "\COPY socialaccount_socialapp_sites FROM 'output_file_socialaccount_socialapp_sites.csv' WITH (FORMAT csv, HEADER);"


echo "Import completed."