from wordcloud import WordCloud, ImageColorGenerator
import streamlit as st
import numpy as np
from PIL import Image 
    

# --- display begin ---
st.title("Word Cloud Generator")

text = st.text_area("",value="please input text here")

# expander1

expander1 = st.expander("basic options")

text_color = expander1.selectbox("text color",[
    'viridis','inferno', 'magma', 'plasma',
    'Blues', 'BuGn', 'BuPu', 'GnBu',
    'Greens', 'Greys', 'OrRd', 'Oranges',
    'PuBu', 'PuBuGn', 'PuRd', 'Purples',
    'RdPu', 'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd',
    'binary', 'gist_yarg', 'gist_gray', 'gray',
    'bone', 'pink', 'spring', 'summer',
    'autumn', 'winter', 'cool', 'Wistia',
    'hot', 'afmhot', 'gist_heat', 'copper',
    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
    'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
    'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
    'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c',
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern', 'gnuplot',
    'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv', 'gist_rainbow', 'rainbow',
    'jet', 'nipy_spectral', 'gist_ncar'])

bg_color = expander1.radio("background color",["black","white","green"])

width = expander1.number_input("width",400,4000,800)
height = expander1.number_input("height",200,2000,400)

repeat = expander1.toggle("repeat words",value=True)

eliminated = expander1.toggle("eliminated basic words",value=False)


# expander2
expander2 = st.expander("mask options")
circlemask = expander2.toggle("apply circle mask")
expander2.write("if you use your own mask image, its background color must be white!")
ownmaskimg = expander2.file_uploader("Upload mask",accept_multiple_files=False)
useownmask = expander2.toggle("apply your mask")


edge_color = "white"
edge_size = 0
colorapply = False
if useownmask:
    edge = expander2.toggle("add edge")
    colorapply = expander2.toggle("apply image color")
    if edge:
        edge_size = expander2.number_input("edge size",1,100)
        edge_color = expander2.selectbox("edge color",["white","black"])

"---"

# --- display end ---



if text == "":
    st.error("input text please")
else:
    with st.spinner("Please wait..."):
        stopwords = [] if not eliminated else None
        
        mask = None

        if circlemask:
            height = width
            x, y = np.ogrid[:width, :height]
            mask = (x - width/2) ** 2 + (y - width/2) ** 2 > width/150*130 ** 2 # 円
            mask = 255 * mask.astype(int)

        if useownmask:
            if ownmaskimg is not None:
                mask = np.array(Image.open(ownmaskimg))
                circlemask = False
            else:
                expander2.error("upload your own image")


        wc = WordCloud(
            width=width,
            height=height,
            background_color=bg_color,
            repeat=repeat,
            mask=mask,
            stopwords=stopwords,
            colormap=text_color,
            contour_color=edge_color,
            contour_width=edge_size
            )
        wc.generate(text)
        wc = wc if not colorapply else wc.recolor(color_func=(ImageColorGenerator(np.array(Image.open(ownmaskimg)))))
        wc.to_file("img.png")
        st.image("img.png",use_column_width=True)

        st.button("regenerate")
        
    with open("img.png","rb") as f:    
        st.download_button("Save image",data=f,file_name="img.png")

"""
---
@c 2023 kubotadaichi
"""
