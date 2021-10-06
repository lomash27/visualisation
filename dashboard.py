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
import SessionState

session_state = SessionState.get(authenticated = False,balloons = False)
#balloons = SessionState.get(authenticate = False)

def app():
    if session_state.balloons == False:
        st.balloons()
        session_state.balloons = True
    st.title("Dashboard for Project")
    st.sidebar.title("Menu")

    #functions###############################################################################################################
    with st.spinner("Loading...."):
        @st.cache(show_spinner = False)
        def load_data_1():
            data = pd.read_csv("Battery.csv")
            return data

    with st.spinner("Loading...."):
        @st.cache(show_spinner = False)
        def load_data_2():
            data = pd.read_csv("Table4.16.csv")
            return data

    with st.spinner("Loading...."):
        @st.cache(show_spinner = False)
        def load_data_3():
            data = pd.read_csv("Table4.4.csv")
            return data

    with st.spinner("Loading...."):
        @st.cache(show_spinner = False)
        def get_map_data():
            data = pd.read_csv('Table4.16.csv')
            return data

    with st.spinner("Loading...."):
        @st.cache(show_spinner = False)
        def get_policy_data():
            data = pd.read_csv('Policy.csv')
            return data


    def make_clickable(link):
        # target _blank to open new window
        # extract clickable text to display for your link
        text = 'Download'
        return f'<a target="_blank" href="{link}">{text}</a>'




    #first function
    def return_html(option):
        html_string = ''
        if option == 'Central Policy':
            html_string = '<html>\
    <head>\
    <style>\
    body {background-color: #E6E6FA;}\
    </style>\
    </head><ul>\
                  <li>Faster Adoption and Manufacturing of Hybrid and Electric Vehicles(FAME)-1\
                    <ul>\
                      <li>Initially launched for a two-year period, but extended till September 2018 at an aprroved outlay of INR 795 Cr in 2015</li>\
                      <li>Focussed on technology development, demand creation, pilot projects and charging infrastructure</li>\
                    </ul>\
                </li>\
                  <li>FAME-2\
                    <ul>\
                      <li>Under phase two extend financial support of INR 8,730 Cr for three years</li>\
                      <li>The fund support includes INR 2,500 Cr for buses, INR 1,000 Cr for four-wheelers,  \
                    INR 600 Cr for two-wheelers and INR 750 Cr for high speed three-wheelers</li>\
                    </ul>\
                </li>\
                </ul></body></html>'
        elif option == "Delhi":
            html_string = '<ul>\
            <li>It envisions the replacement of the existing auto rickshaws and State-run buses with E-Autos and E-Buses respectively\
                          It will also ensure that delivery based services operating in the city are powered by E-Mobility.</li>\
            <li>It talks about increasing road tax for fuel-based vehicles, at least in the luxury segment and imposing in certain parts of the city\
                          a congestion fee that EVs will be exempt from.</li>\
            </ul>'
        return html_string


    def chart_return(data,column):
        data = data.sort_values(column)
        x = list()
        y = list()
        for i in range(len(data)):
            x.append(data.iloc[i]['Manufacturer'] + " " + data.iloc[i]['Model'])
            y.append(data.iloc[i][column])
        plt.close()
        #plt.barh(data['Model'], data[column])
        plt.barh(x,y)
        plt.ylabel("Make & Model")
        plt.xlabel(column)
        # st.pyplot(plt)
        return plt



    def pie_chart1(data,column1,column2,string):
        pie_chart = px.pie(
            data_frame=data,
            values=column2,
            names=column1,
            color= column1,  # differentiate markers (discrete) by color
            color_discrete_sequence=px.colors.sequential.Rainbow,  # set marker colors
            #color_discrete_sequence=px.colors.qualitative.Plotly
            #hover_name=column1,  # values appear in bold in the hover tooltip
            #labels={"Resources(Tonnes)": "Resources (Tonnes)"},  # map the labels
            template='seaborn',#'presentation',  #'ggplot2', 'seaborn', 'simple_white', 'plotly',
            # 'plotly_white', 'plotly_dark', 'presentation',
            # 'xgridoff', 'ygridoff', 'gridon', 'none'
            width=500,  # figure width in pixels
            height=500,  # figure height in pixels
            hole=0,  # represents the hole in middle of pie
        )
        pie_chart.update(layout_showlegend=False)
        #pie_chart.update(layout_hovermode="x")
        string_hover = ' %{label} : %{percent} <br> ' + string + ' : %{value}'
        pie_chart.update_traces(textinfo = "none",hovertemplate = string_hover)
        return pie_chart





    #third function
    def car_list(data):
        cars = []
        for i in range(len(data)):
            string_company = data.iloc[i]['Manufacturer']
            string_model = data.iloc[i]['Model']
            string_car = string_company + " " + string_model
            cars.append(string_car)
        return tuple(cars)


    #fourth function
    def display_car_info(data,option):
        for i in range(len(data)):
            string_company = data.iloc[i]['Manufacturer']
            string_model = data.iloc[i]['Model']
            string_car = string_company + " " + string_model
            if string_car == option:
                #st.subheader(string_car)
                return data.iloc[i]


    #fifth function
    def fancy_html2(map_data,row):
        i = row
        string_1 = map_data.iloc[i]['Country']
        if pd.notna(map_data.iloc[i]['Reserve(Tonnes)']):
            string_3 = int(map_data.iloc[i]['Reserve(Tonnes)'])
        else:
            string_3 = "-"
        if pd.notna(map_data.iloc[i]['Resources(Tonnes)']):
            string_4 = int(map_data.iloc[i]['Resources(Tonnes)'])
        else:
            string_4 = "-"
        left_col_colour = "#CCFFCC"
        right_col_colour = "#CCFFCC"

        html = """<!DOCTYPE html>
    <html>
    
    <head>
    <style>
    table, th, td {
      border: 1px solid black;
    }
    </style>
    </head>
        <table style="width: 350px">
    <tbody>
    <tr>
    <td style="background-color: """ + left_col_colour + """;"><span style="color: #000000;">Country</span></td>
    <td style="width: 150px;background-color: """ + right_col_colour + """;">{}</td>""".format(string_1) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_colour + """;"><span style="color: #000000;">Reserve(Tonnes)</span></td>
    <td style="width: 150px;background-color: """ + right_col_colour + """;">{}</td>""".format(string_3) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_colour + """;"><span style="color: #000000;">Resources(Tonnes)</span></td>
    <td style="width: 150px;background-color: """ + right_col_colour + """;">{}</td>""".format(string_4) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
        return html

    def fancy_html1(map_data,row):
        i = row
        string_1 = map_data.iloc[i]['Country']
        string_2 = int(map_data.iloc[i]['Production(tonnes)(2018)'])
        string_5 = int(map_data.iloc[i]['Production(tonnes)(2019)'])
        left_col_colour = "#CCFFCC"
        right_col_colour = "#CCFFCC"

        html = """<!DOCTYPE html>
    <html>
    
    <head>
    <style>
    table, th, td {
      border: 1px solid black;
    }
    </style>
    </head>
        <table style="width: 350px">
    <tbody>
    <tr>
    <td style="background-color: """ + left_col_colour + """;"><span style="color: #000000;">Country</span></td>
    <td style="width: 150px;background-color: """ + right_col_colour + """;">{}</td>""".format(string_1) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_colour + """;"><span style="color: #000000;">Production(tonnes)(2018)</span></td>
    <td style="width: 150px;background-color: """ + right_col_colour + """;">{}</td>""".format(string_2) + """
    </tr>
    <tr>
    <td style="background-color: """ + left_col_colour + """;"><span style="color: #000000;">Production(tonnes)(2019)</span></td>
    <td style="width: 150px;background-color: """ + right_col_colour + """;">{}</td>""".format(string_5) + """
    </tr>
    </tbody>
    </table>
    </html>
    """
        return html

    def policy_button():
        data = get_policy_data()
        col3, col4 = st.beta_columns(2)
        for i in range(len(data)):
            col3.write(data.iloc[i]['Entity'])
            link = make_clickable(data.iloc[i]['Link'])
            col4.write(link,unsafe_allow_html=True)

    def policy_map_button():
        data = pd.read_csv('StatePolicies.csv')
        m = folium.Map(tiles="Stamen Watercolor", zoom_start=3, max_zoom=6, min_zoom=2, zoom_Animation=False)
        states = json.load(open('india_states.geojson', 'r'))
        style1 = {'fillOpacity': '0', 'color': 'black', 'weight': '0.8'}
        layer = folium.GeoJson(
            states,
            name='geojson',
            style_function=lambda x: style1
        ).add_to(m)
        m.fit_bounds([[26.051054453379013, 64.6016217019466], [27.51097571534207, 100.03322049016737]])
        for i in range(0, len(data)):
            htmlFile = data.iloc[i]['FileName']
            html = open(htmlFile, 'r')
            #st.write(html)
            html = html.read()
            #html = """"""
            iframe = branca.element.IFrame(html=html, width=400, height=300)
            popup = folium.Popup(iframe, parse_html=True)
            print(data.iloc[i]['Latitude'])
            marker = folium.Marker([data.iloc[i]['Latitude'], data.iloc[i]['Longitude']],
                                   popup=popup, icon=folium.Icon(color='green', icon='info-sign')).add_to(m)
        folium_static(m)


    #functions end ###############################################################################################################

    st.sidebar.subheader("Central and State EV Policies")
    if st.sidebar.button('Salient Features of Central Policy'):
        st.subheader('Salient Features of Central Policy')

        string_central = """
        <html>
        <table >
        <head>
        <style>
            table{
            background-image: url("https://raw.githubusercontent.com/vibzwengz/Project1WebApp/main/IndiaBackground.jpg");
            background-position: center;
            background-repeat:no-repeat;
            border: 1px solid black;
            background-size:stretch;
            }
    }
        </style>
        </head>
        <ol>
        <li>Faster Adoption and Manufacturing of Hybrid and Electric Vehicles (FAME)-1
         <ul>
         <li>Initially launched for a two-year period, but extended till September 2018.</li>
         <li>Approved outlay of INR 795 crores in 2015.
         <li>Focused on technology development, demand creation, pilot projects and charging infrastructure.</li>
         </ul>
         </li>
        <li>Fame-2
        <ul>
        <li>Under phase II extend financial support of INR 8,730 Cr for three years.</li>
        <li>The fund support includes INR 2,500 Cr for buses, INR 1,000 Cr for four-wheelers, INR 600 Cr for two-wheelers (with maximum speed greater than 25 km) and INR 750 crore for high speed three-wheelers.</li>
        <li>Main focus on the deployment of electric buses on the Indian roads. Because during FAME-1 Central government received around 47 proposals which demanded deployment of 3,144 buses across 44 cities.</li>
        <li>With this policy, the central government is planning to prioritise the development of public transportation, shared mobility, and smaller electric vehicles such as two-wheelers.</li>
        <li>5595 electric buses have been sanctioned to 64 cities and the related STUs. 5095 units out of it are for intra-city transport. Currently, there are approximately 1.95 lakh buses under several STUs in India.</li>
        <li>There is no fixed timeline mandated by any government (state or central) to complete the transition of state transport union (STU) buses to EVs</li>    
        </ul>
        </li>
        <li>The government, in a recent move, has approved green license plates for electric vehicles in order to encourage people to use them. The purpose behind is their easy identification for proposed benefits such as concessional toll, preferential treatment for parking and free entry in congested zones.</li>
        <li>The government-backed Energy Efficiency Services Ltd (EESL) has issued tenders for 20K EVs to be deployed across the country for government use. With this the government aims an EV sales penetration of 30% for private cars, 70% for commercial cars, 40% for buses, and 80% for two- and three-wheelers by 2030.</li>
        </ol>
        </table>
        </html>
        """
        st.markdown(string_central, unsafe_allow_html=True)
        st.write(" ")
        if st.button('Hide'):
            string_central = ""
    if st.sidebar.button('Salient Features of State Policies'):
        st.subheader('Salient Features of State Policies')
        policy_map_button()
    if st.sidebar.checkbox('EV Policy List'):
        st.subheader('EV Policy List')
        policy_button()
    #option = st.sidebar.selectbox('Select State Specific Policy', ('--','Central Policy', 'Delhi'))
    #if option is not "--":
        #st.subheader("Main features")


    #st.markdown(return_html(option), unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    st.sidebar.subheader('Comparision of Present Battery Electric Vehicles sold in the US')
    option2 = st.sidebar.selectbox("Select type of visualization",("--","Vehicle Range(km)",'Vehicle Range(mi)','Battery Size(kWh)'))
    if option2 is not '--':
        data = load_data_1()
        st.subheader("Present Battery Electric Vehicles sold in the US")
        st.pyplot(chart_return(data,option2))


    more_info = st.sidebar.checkbox('More Information')
    if more_info:
        data = load_data_1()
        cars = car_list(data)
        option3 = st.sidebar.radio("Select Car",cars)
        st.subheader(option3)
        st.write(display_car_info(data,option3))


    st.sidebar.subheader('Comparision of Present Hybrid Electric Vehicles sold in the US')
    option4 = st.sidebar.selectbox("Select type of visualization",("--","Electric Range(km)",'Electric Range(mi)','Battery Size(kWh)'),key = "option4")
    if option4 is not '--':
        data = load_data_3()
        st.subheader("Present Hybrid Vehicles sold in the US")
        st.pyplot(chart_return(data,option4))


    more_info_2 = st.sidebar.checkbox('More Information',key = "more_info_2")
    if more_info_2:
        data = load_data_3()
        cars = car_list(data)
        option5 = st.sidebar.radio("Select Car",cars)
        st.write(display_car_info(data,option5))


    st.sidebar.subheader("Lithium Reserves,Resources & Production Details")
    show_map = st.sidebar.checkbox("Show map of lithium reserves and resources")
    show_map_two = st.sidebar.checkbox("Show map of lithium production")
    show_pie_chart = st.sidebar.checkbox("Distribution of World Lithium Resources")
    show_pie_chart1 = st.sidebar.checkbox("Distribution of World Lithium Reserves")
    show_pie_chart2 = st.sidebar.checkbox("Distribution of World Lithium Production(2018)")
    show_pie_chart3 = st.sidebar.checkbox("Distribution of World Lithium Production(2019)")

    if show_map:
        st.subheader("Lithium Reserves & Resources")
        map_data = get_map_data()
        m = folium.Map(tiles="Stamen Watercolor", zoom_start=3, max_zoom=6, min_zoom=2, zoom_Animation=False)
        for i in range(0, len(map_data)):
            html = fancy_html2(map_data,i)
            iframe = branca.element.IFrame(html=html, width=350, height=150)
            popup = folium.Popup(iframe, parse_html=True)
            marker = folium.Marker([map_data.iloc[i]['latitude'], map_data.iloc[i]['longitude']],
                                    popup=popup, icon=folium.Icon(color='green', icon='info-sign')).add_to(m)

        folium_static(m)



    if show_map_two:
        st.subheader("Lithium Production")
        map_data = get_map_data()
        m = folium.Map(tiles="Stamen Watercolor", zoom_start=3, max_zoom=6, min_zoom=2, zoom_Animation=False)
        for i in range(0, len(map_data)):
            if pd.notna(map_data.iloc[i]['Production(tonnes)(2018)']):
                html = fancy_html1(map_data,i)
                iframe = branca.element.IFrame(html=html, width=350, height=150)
                popup = folium.Popup(iframe, parse_html=True)
                marker = folium.Marker([map_data.iloc[i]['latitude'], map_data.iloc[i]['longitude']],
                                       popup=popup, icon=folium.Icon(color='green', icon='info-sign')).add_to(m)

        folium_static(m)

    if show_pie_chart:
        data = get_map_data()
        st.subheader("Distribution of World Lithium Resources")
        st.plotly_chart(pie_chart1(data,'Country','Resources(Tonnes)','Resources (Tonnes)'))


    if show_pie_chart1:
        data = get_map_data()
        st.subheader("Distribution of World Lithium Reserves")
        st.plotly_chart(pie_chart1(data,'Country','Reserve(Tonnes)','Reserve (Tonnes)'))

    if show_pie_chart2:
        data = get_map_data()
        st.subheader("Distribution of World Lithium Production(2018)")
        st.plotly_chart(pie_chart1(data,'Country','Production(tonnes)(2018)', 'Production (Tonnes) (2018)'))

    if show_pie_chart3:
        data = get_map_data()
        st.subheader("Distribution of World Lithium Production(2019)")
        st.plotly_chart(pie_chart1(data,'Country','Production(tonnes)(2019)', 'Production (Tonnes) (2019)'))


    st.sidebar.subheader("Miscellaneous Information")
    if st.sidebar.checkbox("Electric Two-Wheelers Models Available in Market"):
        HtmlFile = open("bar_book3_1.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        print(source_code)
        components.html(source_code,height = 810)

    if st.sidebar.checkbox("Electric Four-Wheelers Models Available in Market"):
        HtmlFile = open("bar_graph_1.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        print(source_code)
        components.html(source_code,height = 810)

    if st.sidebar.checkbox("Statewise No. of EV Charging Stations"):
        HtmlFile = open("IndiaMapVisualization1.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        print(source_code)
        components.html(source_code,height = 800,width = 750)

    if st.sidebar.checkbox("Countrywise EV Charging Stations"):
        HtmlFile = open("worldmaptable.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        print(source_code)
        components.html(source_code,height = 750,width = 750)

    if st.sidebar.checkbox("Battery Comparision 1"):
        HtmlFile = open("bar_nested.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        print(source_code)
        components.html(source_code,height = 370)

    if st.sidebar.checkbox("Battery Comparision 2"):
        HtmlFile = open("bar_nested2_1.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        print(source_code)
        components.html(source_code,height = 370)

    if st.sidebar.checkbox("List of Commercial EV models Available in Market"):
        HtmlFile = open("bar_t1.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        print(source_code)
        components.html(source_code,height = 810)

    if st.sidebar.checkbox("Leading Countries in Vehicle Production"):
        HtmlFile = open("pie.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        print(source_code)
        components.html(source_code,height = 520)

    if st.sidebar.checkbox("Leading Countries in Battery Cell Production"):
        HtmlFile = open("pie2.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        print(source_code)
        components.html(source_code,height = 480)

    if st.sidebar.checkbox("Leading Countries in Major Sales Market"):
        HtmlFile = open("pie3.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read()
        print(source_code)
        components.html(source_code,height = 600)

    if st.sidebar.button("Logout"):
        session_state.authenticated = False
        session_state.balloons = False


file = open('Project.key','rb')
key = file.read()
file.close()

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


if session_state.authenticated == False:

    login_blocks = generate_login_block()
    register_blocks = generate_register_block()
    answer = login(login_blocks)
    answerRegister = register(register_blocks)
    username = answer[0]
    password = answer[1]

    if is_authenticated(username,password):
        clean_blocks(login_blocks)
        clean_blocks(register_blocks)
        session_state.authenticated = True
        app()

    elif password:
        st.info("Please enter a valid username and/or password")
        st.info("New User? Please Register")

else:
    app()















