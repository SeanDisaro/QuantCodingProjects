import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from PIL import Image, ImageDraw, ImageFont
import numpy as np


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

    fig, ax = plt.subplots(figsize=(4, 8))

    color = cmap((rating - 1) / 9)

    ax.bar(x=[0], height=[rating], color=color, width=0.5)

    ax.set_ylim(0, 10.5)
    ax.set_xlim(-0.5, 0.5)

    ax.set_title("1-10 Optimism Rating  -NVIDIA stock", fontsize=16)
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

    plt.tight_layout(rect=[0, 0, 0.85, 1])
    plt.savefig("./pictures/ratingPlot.png")

    # picture with text rating
    width, height = 600, 400
    background_color = mcolors.to_hex(color)  
    text_color = (0, 0, 0)  # White
    custom_text = textRating[rating]


    image = Image.new('RGB', (width, height), color= background_color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), custom_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) / 2
    y = (height - text_height) / 2


    draw.text((x, y), custom_text, fill=text_color,   font=font)

    image.save("./pictures/textRating.png")