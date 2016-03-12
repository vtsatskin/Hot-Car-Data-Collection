import sqlite3
conn = sqlite3.connect('example3.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE project
             (date_text, type, movement, temp, dangerous)''')

# Insert a row of data
c.execute("INSERT INTO project VALUES ('2016-03-12','human','no','25', 'No')")

# Save (commit) the changes
conn.commit()

date = ('2016-03-12',)
c.execute('SELECT * FROM project WHERE date_text=?', date)
print c.fetchone()

conn.close()