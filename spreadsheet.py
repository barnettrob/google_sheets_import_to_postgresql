import gspread
from oauth2client.service_account import ServiceAccountCredentials
import psycopg2
from itertools import islice

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("Repositories Decoder").sheet1

# data warehouse postgres db.
dbhost = 'localhost' # replace if different
dbuser = 'dbuser' # replace with actual database user
dbpass = 'dbpassword' # replace with actual database password
database = 'mydb' # replace with actual database name

# port is 5432 by default.  So if different then specify port.
dwarehouse_conn = psycopg2.connect(dbname=database, user=dbuser, host=dbhost, password=dbpass, port='5432')
cursor = dwarehouse_conn.cursor()

# Get number of rows in PostgreSQL table.
repo_product_info_count_sql = 'SELECT COUNT(*) FROM repositories_product_information'
cursor.execute(repo_product_info_count_sql)
count_result = cursor.fetchone()

# Number of rows in repositories_product_information from data warehouse.
num_rows_repo_products = count_result[0]

# This is a list of list of all data and wrap with length function to get row count.
num_rows_sheets = len(sheet.get_all_values())

# First row is the header to remove this from count.
num_rows_sheets = num_rows_sheets - 1

# Get results that can be iterated on.
iterable_results = iter(sheet.get_all_values())
# Skip header (first) row
next(iterable_results)

# islice is a library to allow us to slice or start iterating in loop
# from a certain number.  In this case, we start at the last row already
# inserted into the PostgreSQL table.  So if the PostgreSQL table has 5 entries (row count of 5)
# then we start looping through the Google Sheet at that number to prevent inserting duplicates.
# This is, of course, assuming the database only has rows getting inserted from the spreadsheet.
# @todo: may remove islice and update code with insert/update based on referer.
for i, value in islice(enumerate(iterable_results), num_rows_repo_products, None):
    # value[0], the referer url cannot be null or empty so skip this row if it is.
    if not value[0]:
        continue
    referer = value[0]
    hardware_platform = "" if not value[1] else value[1]
    os = "" if not value[2] else value[2]
    os_version = "" if not value[3] else value[3]
    product_name = "unknown" if not value[4] else value[4]
    product_version = "" if not value[5] else value[5]
    packaging = "" if not value[6] else value[6]
    campaign = "" if not value[7] else value[7]

    # Build insert query and insert records from spreadsheet into PostgreSQL table.
    query = (
        "INSERT INTO repositories_product_information (referer, hardware_platform, os, os_version, product, product_version, packaging, campaign_id)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.execute(query, (
        referer, hardware_platform, os, os_version, product_name, product_version, packaging, campaign))
    dwarehouse_conn.commit()

    print value