import streamlit as st
import Structure as Head

def main():
    st.set_page_config(page_title="Delta Hedging", page_icon=":robot_face:", layout="wide")
    st.markdown(Head.TextPolice("Delta Hedging based on Black-Scholes-Merton Model.",40), unsafe_allow_html=True)

    st.markdown(Head.TextPolice("Define parameters of the underlying asset and the option.",15), unsafe_allow_html=True)

    with st.form("parameters_form"):
        st.markdown(Head.TextPolice("Underlying Asset Parameters", 20), unsafe_allow_html=True)
        S = st.number_input("Current Price of Underlying Asset (S)", min_value=1.0, value=100.0, step=1.0)
        Q = st.number_input("Dividend Yield % (q)", min_value=0.0, value=5.0, step=0.1) / 100
        Vol = st.number_input("Volatility of Underlying Asset % (σ)", min_value=0.0, value=20.0, step=0.1) / 100

        st.markdown(Head.TextPolice("Option Parameters", 20), unsafe_allow_html=True)
        option_type:Head.Literal["Call","Put"] = st.selectbox("Select Option Type", ["Call", "Put"])
        K = st.number_input("Strike Price of Option (K)", min_value=1.0, value=100.0, step=1.0)
        T = st.number_input("Time to Maturity in Years (T)", min_value=1/1000, value=1.0, step=1/1000)
        R = st.number_input("Risk-Free Interest Rate % (r)", min_value=-10.0, value=5.0, step=0.1) / 100

        st.markdown(Head.TextPolice("Environment Parameters", 20), unsafe_allow_html=True)
        Step = st.number_input("Time Step in Years (Δt)", min_value=10.0, value=365.0, step=1.0)
        Hedge = st.number_input("Hedge Frequency based on the number of periods ", min_value=1.0, value=10.0, step=1.0) / Step
        Rounding = int(st.number_input("Rounding Precision", min_value=1, value=3, step=1))
        Seed = int(st.number_input("Random Seed", min_value=0, value=10000, step=1))
        submit_button = st.form_submit_button(label="Start Computation")

    if submit_button:
        oENV = Head.Environnement_Modelisation(T=T, Steps= int(Step), Cout_Hedge=0, Periodicite_Hedge=Hedge)
        oOPT = Head.BlackSchole_Modele(OptionType=option_type, S0=S, K=K, T=T, r=R, q=Q, sigma=Vol,round=Rounding)
        TRA = Head.Trajectoire(ENV=oENV, Option=oOPT, seed=Seed)

        
main()