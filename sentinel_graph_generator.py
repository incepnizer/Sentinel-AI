import matplotlib.pyplot as plt
import numpy as np
import psycopg2

# Basic colors:
blue = '#008fd5'
red = '#fc4f30'
yellow = '#e5ae37'
green = '#6d904f'

def est_connection(db, user_id):
    connection = psycopg2.connect(host='ec2-3-229-166-245.compute-1.amazonaws.com', database='d81l57ohoqttlu', user='owrzrgewethgnm', password='179c8ce1e814e2081f9f1cdf42240a30f465d6c1b61e442d7ff9d5a42f3e775f')
    c = connection.cursor()
    query = f"SELECT * FROM {db} WHERE user_id = '{user_id}'"
    c.execute(query)
    result = c.fetchall()

    connection.commit()
    c.close()
    connection.close()

    return result


def get_sentiment_values(result):

    neg_counter = 0
    neu_counter = 0
    pos_counter = 0


    for r in result:
        if r[2] > 3:
            pos_counter = pos_counter + 1

        elif r[2] < 3:
            neg_counter = neg_counter + 1

        else:
            neu_counter = neu_counter + 1

    senti_values = [neg_counter, neu_counter, pos_counter]
    return senti_values


def get_sentiscore_distribution(result):
    num_1 = 0
    num_2 = 0
    num_3 = 0
    num_4 = 0
    num_5 = 0

    for r in result:

        if r[2] == 1:
            num_1 = num_1 + 1
        elif r[2] == 2:
            num_2 = num_2 + 1
        elif r[2] == 3:
            num_3 = num_3 + 1
        elif r[2] == 4:
            num_4 = num_4 + 1
        else:
            num_5 = num_5 + 1
    
    res = [num_1, num_2, num_3, num_4, num_5]
    return res


# Pie Chart
def create_pie_chart(senti_values, platform, user_id):


    slices = [senti_values[0], senti_values[1], senti_values[2]]
    labels = ["Negative", "Neutral", "Positive"]
    colors = [red, green, blue]
    plt.pie(slices, labels=labels, colors=colors, autopct='%1.1f%%')

    # wedgeprops={'edgecolor':'black'}

    plt.title(f"{platform} Review Sentiment Distribution" )
    #plt.show()
    plt.tight_layout()
    plt.savefig(f"{user_id}{platform}SentiPie.png")
    plt.clf()


# Bar Graph
def create_bar_graph(senti_values, platform, user_id):

    x_axis = ["Negative", "Neutral", "Positive"]
    y_axis = [senti_values[0], senti_values[1], senti_values[2]]
    colors = [red, green, blue]


    plt.bar(x_axis, y_axis, color=colors)
    plt.title(f"{platform} Review Sentiment Distribution")
    plt.xlabel("Review Sentiment")
    plt.ylabel("Number of Reviews")

    for i in range(0, 3):
        plt.text(x_axis[i], y_axis[i], y_axis[i])

    #plt.show()
    plt.tight_layout()
    plt.savefig(f"{user_id}{platform}SentiBar.png")
    plt.clf()


# Bar Graph
def create_sentiscore_distribution(y_ax, platform, user_id):

    x_axis = [1, 2, 3, 4, 5]
    y_axis = y_ax

    plt.bar(x_axis, y_axis)
    plt.title(f"{platform} SentiScore Distribution")
    plt.xlabel("SentiScore")
    plt.ylabel("Number of Reviews")

    for i in range(0, 5):
        plt.text(x_axis[i], y_axis[i], y_axis[i])

    #plt.show()
    plt.tight_layout()
    plt.savefig(f"{user_id}{platform}SentiScoreDist.png")
    plt.clf()




def main():

    db = 'amazon_reviews'
    user_id = 70
    platform = 'Amazon'
        
    create_sentiscore_distribution(get_sentiscore_distribution(est_connection(db, user_id)), platform, user_id)
    create_bar_graph(get_sentiment_values(est_connection(db, user_id)), platform, user_id)
    create_pie_chart(get_sentiment_values(est_connection(db, user_id)), platform, user_id)

main()



# Line Graph
# #print(plt.style.available)

# #plt.style.use("fivethirtyeight")

# dev_x = [25, 26, 27, 28, 29]
# dev_y = [38496, 42000, 46752, 49320, 53200]
# dev_y1 = [32000, 34321, 35674, 41122, 45231]

# plt.plot(dev_x, dev_y, color="#444444" , linewidth=3, label="Comapany 1")
# plt.plot(dev_x, dev_y1, color= "#5a7d9a", label="Company 2")
# plt.legend()

# plt.title("Review Sentiment Distribution")
# plt.xlabel("Review Sentiment")
# plt.ylabel("Number of reviews")

# plt.tight_layout()
# plt.grid(True)
# plt.show()

# plt.savefig("SentiGraph.png")