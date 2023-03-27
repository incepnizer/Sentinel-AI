import psycopg2
import pandas as pd

connection = psycopg2.connect(host='ec2-3-229-166-245.compute-1.amazonaws.com', database='d81l57ohoqttlu', user='owrzrgewethgnm', password='179c8ce1e814e2081f9f1cdf42240a30f465d6c1b61e442d7ff9d5a42f3e775f')
c = connection.cursor()
query = "SELECT * FROM amazon_reviews"
c.execute(query)
result = c.fetchall()

toCsv = []
 
for r in result:

    toCsv.append(list(r))

for i in toCsv:
    i[1] = i[1].replace("\n", "")

sql_df = pd.DataFrame(toCsv, columns=['id', 'review', 'sentiscore'])
sql_df.to_csv("test.csv", encoding='utf-8', index=False)


connection.commit()
c.close()
connection.close()