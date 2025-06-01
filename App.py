import streamlit as st
import Structure as Head
import plotly.express as px

def main():
    st.set_page_config(page_title="Delta Hedging", page_icon=":robot_face:", layout="wide")
    st.markdown(Head.TextPolice("Delta Hedging based on Black-Scholes-Merton Model.",40), unsafe_allow_html=True)

    st.markdown(Head.TextPolice("Define parameters of the underlying asset and the option.",15), unsafe_allow_html=True)

    with st.form("parameters_form"):
        st.markdown(Head.TextPolice("Underlying Asset Parameters", 20), unsafe_allow_html=True)
        col1_1, col1_2, col1_3 = st.columns(3, vertical_alignment="bottom")
        with col1_1:
            S = st.number_input("Current Price of Underlying Asset (S)", min_value=1.0, value=100.0, step=1.0)
        with col1_2:
            Q = st.number_input("Dividend Yield % (q)", min_value=0.0, value=5.0, step=0.1) / 100
        with col1_3:
            Vol = st.number_input("Volatility of Underlying Asset % (σ)", min_value=0.0, value=20.0, step=0.1) / 100

        st.markdown(Head.TextPolice("Option Parameters", 20), unsafe_allow_html=True)
        col2_1, col2_2, col2_3, col2_4 = st.columns(4, vertical_alignment="bottom")
        with col2_1:
            option_type:Head.Literal["Call","Put"] = st.selectbox("Select Option Type", ["Call", "Put"])
        with col2_2:
            K = st.number_input("Strike Price of Option (K)", min_value=1.0, value=100.0, step=1.0)
        with col2_3:
            T = st.number_input("Time to Maturity in Years (T)", min_value=1/1000, value=1.0, step=1/1000)
        with col2_4:
            R = st.number_input("Risk-Free Interest Rate % (r)", min_value=-10.0, value=5.0, step=0.1) / 100

        st.markdown(Head.TextPolice("Environment Parameters", 20), unsafe_allow_html=True)
        col3_1, col3_2, col3_3, col3_4 = st.columns(4, vertical_alignment="bottom")
        with col3_1:
            Step = st.number_input("Time Step overall (Δt)", min_value=10.0, value=365.0, step=1.0)
        with col3_2:
            Hedge = st.number_input("Hedge Frequency (number of periods) ", min_value=1.0, value=10.0, step=1.0) / Step
        with col3_3:
            Rounding = int(st.number_input("Rounding Precision", min_value=1, value=3, step=1))
        with col3_4:
            Seed = int(st.number_input("Random Seed", min_value=0, value=10000, step=1))
        submit_button = st.form_submit_button(label="Start Computation")

    if submit_button:
        oENV = Head.Environnement_Modelisation(T=T, Steps= int(Step), Cout_Hedge=0, Periodicite_Hedge=Hedge)
        oOPT = Head.BlackSchole_Modele(OptionType=option_type, S0=S, K=K, T=T, r=R, q=Q, sigma=Vol,round=Rounding)
        TRA = Head.Trajectoire(ENV=oENV, Option=oOPT, seed=Seed)

         #Réalise un graphique qui montre la trajectoire du sous-jacent qui est stockée dans TRA.Trajectoire avec l'axe X qui est un en % d'année
        Y1 = TRA.Trajectoire
        X1 = [T * i / TRA.ENV.Steps for i in range(len(Y1))] 
        fig = px.line(x=X1, y=Y1, labels={'x': 'Time (Years)', 'y': 'Underlying Asset Price'}, title='Underlying Asset Price Trajectory')
        fig.update_layout(title_x=0, title_font_size=20, xaxis_title_font_size=15, yaxis_title_font_size=15)
        st.plotly_chart(fig, use_container_width=True)

        X2,Y2 = TRA.Prime_Trajectoire[:,0], TRA.Prime_Trajectoire[:,1]
        fig2 = px.line(x=X2, y=Y2, labels={'x': 'Time (Years)', 'y': 'Option Premium'}, title='Option Premium Trajectory')
        fig2.update_layout(title_x=0, title_font_size=20, xaxis_title_font_size=15, yaxis_title_font_size=15)
        st.plotly_chart(fig2, use_container_width=True)

        X3,Y3 = TRA.Delta_Trajectoire[:,0], TRA.Delta_Trajectoire[:,1]
        fig3 = px.line(x=X3, y=Y3, labels={'x': 'Time (Years)', 'y': 'Delta'}, title='Delta Trajectory')
        fig3.update_layout(title_x=0, title_font_size=20, xaxis_title_font_size=15, yaxis_title_font_size=15)
        st.plotly_chart(fig3, use_container_width=True)

        X4,Y4 = TRA.DetlaHedging_Matrice[:,0], TRA.DetlaHedging_Matrice[:,4]
        fig4 = px.line(x=X4, y=Y4, labels={'x': 'Time (Years)', 'y': 'Value of delta hedged position'}, title='Portfolio value with Delta Hedging')
        fig4.update_layout(title_x=0, title_font_size=20, xaxis_title_font_size=15, yaxis_title_font_size=15)
        st.plotly_chart(fig4, use_container_width=True)

main()