
import requests
import json
import pyodbc

url = "https://www.orlandohealth.com/-/media/files/orlando-health/patients-and-visitors/patient-financial-resources/pricing-transparency-guide/591726273_orlandohealth_winniepalmer_standardcharges.json"

response = requests.get(url)
data = json.loads(response.text)

# print(json.dumps(data, indent=4))

flattened_data = []
for key in data:
    for item in data[key]:
        flattened_data.append(item)



# SQL Server connection string
server = 'RANDYS-XPS' 
database = 'HC_PRICES' 

cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';Trusted_Connection=yes;')
cursor = cnxn.cursor()

cursor.execute('''
    IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[charges]') AND type in (N'U'))
    BEGIN
        CREATE TABLE charges (
            id INT PRIMARY KEY IDENTITY(1,1),
            payer NVARCHAR(255),
            apc NVARCHAR(50),
            description NVARCHAR(255),
            payer_specific_negotiated_charge FLOAT
        )
    END
''')
cursor.commit()

# Define the SQL query
query = '''
    INSERT INTO charges (payer, apc, description, payer_specific_negotiated_charge) 
    VALUES (?, ?, ?)
'''

# Iterate over the flattened_data list
for item in flattened_data:
    # Extract the values
    key1_value = item['payer']
    key2_value = item['apc']
    key3_value = item['description']
    key4_value = item['payer_specific_negotiated_charge']

    # Execute the SQL query
    cursor.execute(query, key1_value, key2_value, key3_value)

# Commit the changes
cnxn.commit()

# Insert data
""" try:
    for item in flattened_data:
        cursor.execute('''
            INSERT INTO charges (payer, apc, description, payer_specific_negotiated_charge) VALUES (?, ?, ?, ?)
        ''', (item['Payer'], item['APC'], item['Description'], item['Payer Specific Negotiated Charge']))

    cnxn.commit()
except Exception as e:
    print("An error occurred:", e)
finally:
    cursor.close()
    cnxn.close() """