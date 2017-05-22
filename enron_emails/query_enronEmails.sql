# Step 1: Connect dornick (internal access only for NU students, faculty, and staff)


# Step 2: Connect to postgres database server:
psql -h 123.123.123.123 -U username -d postgres


# Step 3: connect to database
\list
\c enron_mail


# Step 4: create viewspsql -h 129.105.208.226 -U jjw4418 -d postgres
CREATE TEMP VIEW jjw4418prep AS
SELECT fromaddress,toaddress
FROM prep.messages_table
WHERE fromaddress <> toaddress
	AND fromaddress <> 'enron.announcements@enron.com'
	AND toaddress <> 'all.worldwide@enron.com'
	AND toaddress <> 'all.houston@enron.com'
	AND toaddress <> 'all.states@enron.com'
	AND toaddress <> 'all_ena_egm_eim@enron.com'
GROUP BY fromaddress,toaddress
ORDER BY count(*) DESC
LIMIT 50;


# Step 5: describe the views
\d jjw4418prep


#Step 6: copy to csv, limit 10 rows
\copy (SELECT * FROM jjw4418prep LIMIT 10) TO 'plot_input.csv' WITH DELIMITER ',' NULL AS '\n' CSV HEADER