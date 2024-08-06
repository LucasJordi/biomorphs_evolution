import streamlit as st
import re
import generate_csv
import core
import matplotlib.pyplot as plt
import os
import numpy as np
import io
# Title of the app


# Using "with" notation
st.set_page_config(
    page_title="Evolução Biomorfos",  # Page title that appears in the browser tab
)
   
st.title("Evolução Biomorfos")

# Input field for the numeral string
input_text = st.sidebar.text_input("Digite o estado inicial (formato: '0001000')")

sementinha = None
input_valid = False
if input_text:
    if re.match(r'^\d+$', input_text):
        input_valid = True
        
        sementinha = [int(x) for x in input_text] 
    else:
        st.error("Por favor, insira apenas números.")



rule_number = st.sidebar.number_input("Digite o número da regra 1D (0 a 255):",min_value=0, max_value=255,step=1,value=0)

option = st.sidebar.selectbox(
    "Escolha a regra para evolução",
    core.get_rules_label(),
)
if "is_animal_state" not in st.session_state:
    st.session_state.is_animal_state = []
if "load_state" not in st.session_state:
    st.session_state.load_state = False
if 'biomorfo_inicial' not in st.session_state:
    st.session_state['biomorfo_inicial'] = False
    st.session_state['generations'] = False
    st.session_state['rule_number'] = False
    
if option:
    selected_rule = core.get_rules()[core.get_rules()['Nome']==option]["Regra"].tolist()[0]
    print(selected_rule)
if input_valid:
    gerar_biomorfo_btn = st.sidebar.button("Gerar evolução")
    if gerar_biomorfo_btn or st.session_state.load_state :
        st.session_state.load_state = True
        selected_rule = core.get_rules()[core.get_rules()['Nome']==option]["Regra"].tolist()[0]
        regra=gerar_biomorfo_btn
        st.sidebar.write(f"Estado inicial : {input_text}")
        st.sidebar.write(f"A regra de automato escolhida foi a {rule_number}")
        initial_state = core.acrescentar_zeros(sementinha, 3) 
        generations = 7
        # Gerar biomorfo 1D com a regra escolhida
        biomorph_1d = core.generate_biomorphs_1d(generations, np.array(initial_state), rule_number)
        biomorph7x7 = core.extrair_centro(biomorph_1d,generations)
        #matrix_size = int(input("Digite o tamanho da matriz para atuação da regra 2D (ex: 30): "))
        matrix_size = 30
        matrix_2d = core.centralize_seed_in_matrix(biomorph7x7, matrix_size)
        st.session_state['biomorfo_inicial'] = matrix_2d
        st.session_state['generations'] = generations
        st.session_state['rule_number'] = rule_number
        plt.figure(figsize=(6, 6))
        plt.imshow(matrix_2d, cmap='binary')
        
        plt.title(f'Semente {generations}x{generations} gerada com a Regra {rule_number}')
        # plt.show()
        st.sidebar.pyplot(plt)

        rule = core.parse_life_rule(selected_rule)
        
        # # Evolução dos biomorfos 2D
        final_biomorph, characteristics_df = core.generate_biomorphs_2d_until_convergence(matrix_2d, rule, selected_rule, "Semente1-Regra1")
        if os.path.exists("biomorphs"):
            # Create ZIP file
            zip_buffer = core.create_zip_from_folder("biomorphs")
            
            # Provide download button
            downbtn =st.sidebar.download_button(
                label="Baixar todas as sementes",
                data=zip_buffer,
                file_name="folder_contents.zip",
                mime="application/zip"
            )
            
            if downbtn:
                for obj in st.session_state.is_animal_state:
                    characteristics_df.at[obj["iteration"]-1, 'É Animal?'] = 'Sim'
                    characteristics_df.at[obj["iteration"]-1, 'Nome do Animal'] = obj['name']

                characteristics_df.to_excel("biomorph_characteristics.xlsx", index=False)
                with open("biomorph_characteristics.xlsx", "rb") as file:
                    file_data = file.read()
                # st.session_state.is_animal_state = []
                st.sidebar.download_button(
                    label="Baixar planilha",
                    data=file_data,
                    file_name="biomorph_characteristics.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                print(characteristics_df)
                
        
        print(regra)
    else:
        if not isinstance(st.session_state['biomorfo_inicial'],bool):
            plt.figure(figsize=(6, 6))
            plt.imshow(st.session_state['biomorfo_inicial'], cmap='binary')
            plt.title(f'Semente {st.session_state["generations"]}x{st.session_state["generations"]} gerada com a Regra {st.session_state["rule_number"]}')
            # plt.show()
            st.sidebar.pyplot(plt)



