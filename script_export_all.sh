export PGPASSWORD='1234'

echo "start export"

echo "django_site"
psql -U dbadmin -h localhost -d geostar_db -c "COPY (SELECT * FROM django_site) TO STDOUT WITH CSV HEADER" > output_file_django_site.csv;

echo "socialaccount_socialapp"
psql -U dbadmin -h localhost -d geostar_db -c "COPY (SELECT * FROM socialaccount_socialapp) TO STDOUT WITH CSV HEADER" > output_file_socialaccount_socialapp.csv;

echo "socialaccount_socialapp_sites"
psql -U dbadmin -h localhost -d geostar_db -c "COPY (SELECT * FROM socialaccount_socialapp_sites) TO STDOUT WITH CSV HEADER" > output_file_socialaccount_socialapp_sites.csv;


echo "completed"