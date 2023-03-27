from bs4 import BeautifulSoup
import requests
import psycopg2

def get_num_reviews(URL):
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    webpage = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(webpage.content, "lxml")
    rating = soup.find_all(class_ = 'a-row a-spacing-base a-size-base')
    str_reviews = ""
    num_reviews = 0
    for rate in rating:
        str_reviews = rate.get_text().replace("\n", " ")
        str_reviews = str_reviews.replace(" ", "")
    
    print(str_reviews)
    if str_reviews.find("|") != -1:

        sep_ind = str_reviews.find("|")
        end_ind = str_reviews.find("g", sep_ind)
        num_reviews = int(str_reviews[sep_ind + 1:end_ind].replace(',',''))
        print(num_reviews)
    else:
        sep_ind = str_reviews.find("s") + 1
        end_ind = str_reviews.find("w")
        num_reviews = int(str_reviews[sep_ind + 1:end_ind].replace(',',''))
        print(num_reviews)
    
    return num_reviews


def main(URL, num_reviews):
    #print(URL)
    #HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})
    ratings = []
    # Making the HTTP Request
    if num_reviews != 0:
        #print(int(num_reviews / 10) + 1)

        URL = URL[0:len(URL) - 1]
        
        for i in range(1, int(num_reviews / 10) + 2):
            print(URL + str(i))
            webpage = requests.get(URL + str(i), headers=HEADERS)
        
            # Creating the Soup Object containing all data
            soup = BeautifulSoup(webpage.content, "lxml")
            #print(soup.text)

            # retrieving review
            rating = soup.find_all(class_ = 'a-size-base review-text review-text-content')
            print(len(rating))
            for rate in rating:
                ratings.append(rate.get_text())
        
        print(len(ratings))
        print(len(set(ratings)))

        return set(ratings)

    else:
        return 0



def get_user_ID(email):

    query = f"SELECT * FROM users WHERE email = '{email}'"
    connection = psycopg2.connect(host='ec2-3-229-166-245.compute-1.amazonaws.com', database='d81l57ohoqttlu', user='owrzrgewethgnm', password='179c8ce1e814e2081f9f1cdf42240a30f465d6c1b61e442d7ff9d5a42f3e775f')
    c = connection.cursor()

    c.execute(query)
    result = c.fetchall()
    user_id = result[0][4]

    connection.commit()
    c.close()
    connection.close()

    return user_id

# opening our url file to access URLs
file = open(r"/Users/akshtyagi/Documents/Python/url.txt", "r")


def get_url(user_id):

    query = f"SELECT * FROM users WHERE user_id = {user_id}"
    connection = psycopg2.connect(host='ec2-3-229-166-245.compute-1.amazonaws.com', database='d81l57ohoqttlu', user='owrzrgewethgnm', password='179c8ce1e814e2081f9f1cdf42240a30f465d6c1b61e442d7ff9d5a42f3e775f')
    c = connection.cursor()
    c.execute(query)

    result = c.fetchall()
    amazon_url = result[0][6]

    connection.commit()
    c.close()
    connection.close()

    return amazon_url


user_id = 70
links = get_url(user_id)
ratings = main(links, get_num_reviews(links))
connection = psycopg2.connect(host='ec2-3-229-166-245.compute-1.amazonaws.com', database='d81l57ohoqttlu', user='owrzrgewethgnm', password='179c8ce1e814e2081f9f1cdf42240a30f465d6c1b61e442d7ff9d5a42f3e775f')
c = connection.cursor()

default_senti_score = -1

for rate in ratings:

    query = "INSERT INTO amazon_reviews (user_id, review, sentiscore) VALUES (%s, %s, %s);"
    review = (user_id, rate, default_senti_score, )
    c.execute(query, review)

connection.commit()
c.close()
connection.close()


