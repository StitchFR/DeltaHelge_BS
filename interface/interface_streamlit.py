import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import interface.interface_dicts as interface_dicts

def TextPolice(texte:str, size:int=12) -> str:
    return f"<span style='font-size:{size}px;'>{texte}</span>"


def main():
    st.set_page_config(page_title=interface_dicts.nomdelapage, page_icon=":robot_face:", layout="wide")
    st.markdown(TextPolice(interface_dicts.TITRES["T1"], 40), unsafe_allow_html=True)
    st.markdown(TextPolice(interface_dicts.ST1, 15), unsafe_allow_html=True)

    with st.form("parameters_form_top"):
        st.markdown(TextPolice(interface_dicts.titrerectangle, 20), unsafe_allow_html=True)
        col1_1, col1_2, col1_3 = st.columns(3, vertical_alignment="bottom")
        with col1_1:
            produits = list(interface_dicts.LSTPRODUCTS.values())
            S = st.selectbox(interface_dicts.nmselectbox1, produits)
        with col1_2:
            produits2 = list(interface_dicts.LSTPRODUCTS2.values())
            Q = st.selectbox(interface_dicts.nmselectbox2, produits2)
        with col1_3:
            NB_SJ = st.number_input(
                interface_dicts.nmimput1,
                min_value=interface_dicts.NB_INPUTS["nmimput1"]["min"],
                max_value=interface_dicts.NB_INPUTS["nmimput1"]["max"],
                value=10,
                step=interface_dicts.NB_INPUTS["nmimput1"]["step"]
            ) / 100

        st.markdown("---")  # Trait de séparation dans la bulle

        col2_1, col2_2 = st.columns(2, vertical_alignment="bottom")
        with col2_1:
            NB_Sim = st.number_input(
                interface_dicts.nmimput2,
                min_value=interface_dicts.NB_INPUTS["nmimput2"]["min"],
                max_value=interface_dicts.NB_INPUTS["nmimput2"]["max"],
                value=200_000,
                step=interface_dicts.NB_INPUTS["nmimput2"]["step"]
            )
        with col2_2:
            NB_Per = st.number_input(
                interface_dicts.nmimput3,
                min_value=interface_dicts.NB_INPUTS["nmimput3"]["min"],
                max_value=interface_dicts.NB_INPUTS["nmimput3"]["max"],
                value=360*12*24,
                step=interface_dicts.NB_INPUTS["nmimput3"]["step"]
            )

        col_btn1, col_btn2, col_btn3 = st.columns([6, 1, 1])
        with col_btn3:
            submit_button = st.form_submit_button(label="Start Computation")
    if submit_button:   
        with st.form("parameters_form_bottom"):
            st.markdown(TextPolice(f"{interface_dicts.titrerectangle2}: {S}", 20), unsafe_allow_html=True)
             
            PRODUIT_dict = interface_dicts.produits_dict[S]
            keys = list(PRODUIT_dict.keys())
            matrice: dict = {}

            for key in keys:
                if key != "name":
                    # Assuming PRODUIT_dict[key] = [desc, default, min, max, step]
                    matrice[key] = st.number_input(
                        label=key,
                        min_value=PRODUIT_dict[key][2],
                        max_value=PRODUIT_dict[key][3],
                        value=PRODUIT_dict[key][1],
                        step=PRODUIT_dict[key][4]
                    )

            col_btn1, col_btn2, col_btn3 = st.columns([6, 1, 1])
            with col_btn3:
                submit_button1 = st.form_submit_button(label="Start Computation")
   



main()