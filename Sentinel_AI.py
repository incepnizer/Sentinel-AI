from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import psycopg2


connection = psycopg2.connect(host='ec2-3-229-166-245.compute-1.amazonaws.com', database='d81l57ohoqttlu', user='owrzrgewethgnm', password='179c8ce1e814e2081f9f1cdf42240a30f465d6c1b61e442d7ff9d5a42f3e775f')
c = connection.cursor()
query = "SELECT * FROM amazon_reviews"
c.execute(query)
result = c.fetchall()

tokenizer = AutoTokenizer.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

model = AutoModelForSequenceClassification.from_pretrained('nlptown/bert-base-multilingual-uncased-sentiment')

tweet = "This Veterans Day, I want to share Tom Voutsos's story. He served in the U.S Marine Corps, and has continued to live a life dedicated to public service. Through @LadderUpHousing, he's helping hardowrking folks but their own hom. https://t.co/wgWG9CBMf7"
tokens = tokenizer.encode(tweet, return_tensors='pt')
#print(tokens)

result = model(tokens)
#result.logits
#print(f'{tweet}:  {int(torch.argmax(result.logits))+1}')

print(int(torch.argmax(result.logits))+1)


