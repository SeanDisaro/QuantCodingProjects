import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from openai import OpenAI
import requests
from bs4 import BeautifulSoup


def createSummaryAndRating(api_key):
    
    baseUrl = "https://markets.businessinsider.com/"
    url ="https://markets.businessinsider.com/news/nvda-stock"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        headlines = soup.find_all("h2")
        for headline in headlines:
            print(headline.text)
            break
    else:
        print("error")

    numArticles = 10
    news_items = soup.find_all('div', class_='latest-news__story', limit=numArticles)

    removeFromText = ["\n"]


    for i in range(numArticles):
        for a in news_items[i].find_all('a', href=True):
            responseArticle = requests.get(baseUrl + a["href"])
            soupArticle = BeautifulSoup(responseArticle.content, "html.parser")
            paragraphs = soupArticle.find_all("p")
            txt = [p.get_text() for p in paragraphs]
            totaltxt = "".join(txt)
            for removetxt in removeFromText:
                totaltxt = totaltxt.replace(removetxt, "")
            
            with open("./articles/article_" + str(i)+".txt","w") as f:
                f.write("".join(txt))

    


    client = OpenAI(api_key=api_key)

    instruction = "Extract 5 Bulletpoints from the following " +str(numArticles) +" articles about NVIDIA. At the very Bottom of your response, give a number from 1 to 10 as a rating on how optimistic the market is for the NVIDIA stock where 1 is very unoptimistic and 10 is very optimistic."
    prompt = instruction
    texts = []
    for i in range(numArticles):
        with open("./articles/article_" + str(i)+".txt","r") as f:
            text = f.read()
        texts.append(text)
        prompt = prompt + ";;; ARTICLE " +str(i+1) +":  " + text



    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": "You are finantial advisor."},
            {"role": "user", "content": f"{prompt}"}
        ]
    )


    responseTxt = response.choices[0].message.content
    i = 1
    while(responseTxt[-i].isnumeric()):
        i +=1

    rating = int( responseTxt[-i+1 :] )

    bulletPoints = responseTxt[ :-i+1]
    with open("./articles/bulletPointSummary.txt","w") as f:
                f.write(bulletPoints)
    
    
    plotRating(rating = rating)



def plotRating(rating = 5):

    textRating = {1: "It's Bad. REALLY BAD!",
                2: "Seems hopeless,\nbut could be worse.",
                3: "It is probably\njust a very low dip.",
                4: "Not optimal,\nbut no reason to panic",
                5: "Neutral. Could be\nbad or could be good.\nWho knows.",
                6: "It's going up, but\nnot the highlight\nof the day.",
                7: "Mr Market is having\na very good day!",
                8: "Now we are talking!\nBuy, Buy, Buy!!",
                9: "Not sure if it can\nget any better than this!\n BUUUYYYY!!",
                10:"This is beyond optimism.\n10 out of 10!"}
    
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "red_to_green", ["red", "lime"]
    )

    # thermometer rating

    fig, ax = plt.subplots(figsize=(6, 5))

    color = cmap((rating - 1) / 9)

    ax.bar(x=[0], height=[rating], color=color, width=0.5)

    ax.set_ylim(0, 10.5)
    ax.set_xlim(-0.5, 0.5)

    ax.set_title("Optimism Rating\n-NVIDIA stock", fontsize=15)
    ax.set_ylabel("Rating")

    ax.set_xticks([])
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)


    ax.text(0, rating, f"{rating}", va='bottom', ha='center', fontsize=12, weight='bold', color='black')


    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    norm = mcolors.Normalize(vmin=1, vmax=10)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cbar_ax, orientation='vertical')
    cbar.set_label('Rating Scale', rotation=270, labelpad=15)

    #plt.tight_layout()#rect=[0, 0, 0.85, 1])
    plt.savefig("./pictures/ratingPlot.png")


    width, height = 300, 200
    background_color = mcolors.to_hex(color)  
    text_color = (0, 0, 0)  
    custom_text = textRating[rating]


    image = Image.new('RGB', (width, height), color= background_color)
    draw = ImageDraw.Draw(image)
    font =  ImageFont.load_default(25)

    bbox = draw.textbbox((0, 0), custom_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) / 2
    y = (height - text_height) / 2


    draw.text((x, y), custom_text, fill=text_color,   font=font)

    image.save("./pictures/textRating.png")