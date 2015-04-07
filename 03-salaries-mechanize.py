import csv
import mechanicalsoup

try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup


########## STEP 1: Open and read the URL ##########

url = 'http://mapyourtaxes.mo.gov/MAP/Employees/Employee/searchemployees.aspx'

# Create a new browser object and open the URL
br = mechanicalsoup.Browser()
form_page = br.get(url)

########## STEP 2: Select and fill out the appropriate form ##########

# Select the appropriate form, which we'll find by looking in Chrome
html_form = form_page.soup.select('#ctl01')[0]

# Each control can be set. Dropdown lists are handled as lists, text fields take text

year_id = '#SearchEmployees1_CalendarYear1_ddlCalendarYear'
year_options = html_form.select(year_id)[0].select('option')

for row in year_options:
	if row['value'] == '2013':
		row['selected'] = 'selected'

year_options = html_form.select(year_id)[0] = ['2013']

agency_id = '#SearchEmployees1_ddlAgencies'
agency_options = html_form.select(agency_id)[0].select('option')

for row in agency_options:
	if row['value'] == '931':
		row['selected'] = 'selected'

lastname_id = '#SearchEmployees1_txtLastName'
html_form.select(lastname_id)[0]['value'] = 'test'

# Submit the form
new_page = br.submit(html_form, form_page.url)

########## STEP 3: Grab and parse the HTML ##########

results_table = new_page.soup.find('table', attrs={'id': 'grdEmployees'})

########## STEP 4: Iterate through the results and write to an output list ##########

output = []

for row in results_table.findAll('tr'):

    output_row = []

    for cell in row.findAll('td'):
        output_row.append(cell.text)

    output.append(output_row)

########## STEP 5: Write results to file ##########

print(output)

handle = open('out-mechanize.csv', 'a')
outfile = csv.writer(handle)
outfile.writerows(output)
