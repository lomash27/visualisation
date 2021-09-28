import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import folium
import streamlit.components.v1 as components
from streamlit_folium import folium_static
import branca
import matplotlib.pyplot as plt
import matplotlib as cm
import numpy as np
import plotly.express as px
import json
from csv import writer
from cryptography.fernet import Fernet


file = open('Project.key','rb')
key = file.read()
file.close()



def app():

    st.write("Sucess!!!")


def is_authenticated(username,password):
    data = pd.read_csv('Auth.csv')

    f = Fernet(key)

    for i in range(0, len(data)):
        if username == f.decrypt(data.iloc[i]['username'].encode()).decode():
            if password == f.decrypt(data.iloc[i]['password'].encode()).decode():
                return True

    return False


def generate_login_block():

    block1 = st.empty()
    block2 = st.empty()
    block3 = st.empty()


    return block1, block2, block3

def generate_register_block():
    block1 = st.sidebar.empty()
    block2 = st.sidebar.empty()
    block3 = st.sidebar.empty()
    block4 = st.sidebar.empty()
    block5 = st.sidebar.empty()
    return block1, block2, block3, block4, block5


def clean_blocks(blocks):
    for block in blocks:
        block.empty()


def register(blocks):
    blocks[0].title("New User Registration")
    username = blocks[1].text_input('Enter username',key = "usernameRegister")
    username = username.encode()

    password = blocks[2].text_input('Password', type="password", key = "passwordRegister")
    password = password.encode()

    f = Fernet(key)

    data = pd.read_csv('Auth.csv')

    flagRegister = True
    for i in range(0, len(data)):

        if username.decode() == f.decrypt(data.iloc[i]['username'].encode()).decode():
            blocks[4].warning("User exists!! Please log in")
            flagRegister = False

    if flagRegister:
        if blocks[3].button("Register"):
            username = f.encrypt(username)
            password = f.encrypt(password)

            List = [username.decode(),password.decode()]

            with open('Auth.csv', 'a') as f_object:

                writer_object = writer(f_object)

                writer_object.writerow(List)

                f_object.close()

            blocks[4].write("User succesfully registered. Continue to login")



def login(blocks):

    blocks[0].title("Login")
    username = blocks[1].text_input('Enter username')

    password = blocks[2].text_input('Password', type="password")


    return username, password

login_blocks = generate_login_block()
register_blocks = generate_register_block()
answer = login(login_blocks)
answerRegister = register(register_blocks)
username = answer[0]
password = answer[1]

if is_authenticated(username,password):
    clean_blocks(login_blocks)
    clean_blocks(register_blocks)
    app()

elif password:
    st.info("Please enter a valid username and/or password")
    st.info("New User? Please Register")