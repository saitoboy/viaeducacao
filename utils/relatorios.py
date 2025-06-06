import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go

def aba_relatorios():
    st.title("📊 Relatórios")
    st.markdown("Visualize os principais indicadores de alunos, distritos e transportadores.")

    distritos_data = []
    transportadores_data = []
    try:
        distritos_resp = requests.get("http://localhost:8000/relatorio/distritos/")
        if distritos_resp.status_code == 200:
            distritos_data = distritos_resp.json()
        transportadores_resp = requests.get("http://localhost:8000/relatorio/transportadores/")
        if transportadores_resp.status_code == 200:
            transportadores_data = transportadores_resp.json()
    except Exception as e:
        st.error(f"Erro ao buscar dados do relatório: {e}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏘️ Alunos por Distrito")
        if distritos_data:
            df_distritos = pd.DataFrame(distritos_data)
            st.dataframe(df_distritos, use_container_width=True, hide_index=True)
            # Gráfico de barras horizontal
            fig1 = px.bar(df_distritos, x="Alunos", y="Distrito", orientation="h", color="Distrito",
                          labels={"Alunos": "Nº de Alunos", "Distrito": "Distrito"},
                          title="Distribuição de Alunos por Distrito")
            fig1.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Sem dados de distritos.")
    with col2:
        st.markdown("### 🚌 Alunos por Transportador")
        if transportadores_data:
            df_transp = pd.DataFrame(transportadores_data)
            st.dataframe(df_transp, use_container_width=True, hide_index=True)
            fig2 = px.bar(df_transp, x="Alunos", y="Transportador", orientation="h", color="Transportador",
                          labels={"Alunos": "Nº de Alunos", "Transportador": "Transportador"},
                          title="Distribuição de Alunos por Transportador")
            fig2.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Sem dados de transportadores.")

    # Alunos por Dia de Utilização
    dias_data = []
    try:
        dias_resp = requests.get("http://localhost:8000/relatorio/dias/")
        if dias_resp.status_code == 200:
            dias_data = dias_resp.json()
    except Exception as e:
        st.error(f"Erro ao buscar dados de dias: {e}")

    st.markdown("---")
    st.markdown("### 📅 Alunos por Dia de Utilização")
    if dias_data:
        df_dias = pd.DataFrame(dias_data)
        st.dataframe(df_dias, use_container_width=True, hide_index=True)
        fig3 = px.bar(df_dias, x="Dia", y="Alunos", color="Dia", labels={"Alunos": "Nº de Alunos", "Dia": "Dia da Semana"},
                      title="Distribuição de Alunos por Dia de Utilização")
        fig3.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Sem dados de dias de utilização.")

    # Heatmap: Alunos por Dia e Distrito
    dias_distritos_data = []
    try:
        dias_distritos_resp = requests.get("http://localhost:8000/relatorio/dias_distritos/")
        if dias_distritos_resp.status_code == 200:
            dias_distritos_data = dias_distritos_resp.json()
    except Exception as e:
        st.error(f"Erro ao buscar dados de dias por distrito: {e}")

    st.markdown("---")
    st.markdown("### 🔥 Mapa de Calor: Alunos por Dia e Distrito")
    if dias_distritos_data:
        df_dias_distritos = pd.DataFrame(dias_distritos_data)
        # Detectar coluna de valores numéricos
        value_col = None
        for col in df_dias_distritos.columns:
            if col.lower() in ["alunos", "quantidade", "qtd", "count"]:
                value_col = col
                break
        if not value_col:
            # Pega a primeira coluna numérica diferente de 'Distrito' e 'Dia'
            for col in df_dias_distritos.columns:
                if col not in ["Distrito", "Dia"] and pd.api.types.is_numeric_dtype(df_dias_distritos[col]):
                    value_col = col
                    break
        if value_col:
            tabela_pivot = pd.pivot_table(
                df_dias_distritos,
                index="Distrito",
                columns="Dia",
                values=value_col,
                aggfunc="sum",
                fill_value=0
            )
            st.dataframe(tabela_pivot, use_container_width=True)
            fig4 = go.Figure(data=go.Heatmap(
                z=tabela_pivot.values,
                x=tabela_pivot.columns,
                y=tabela_pivot.index,
                colorscale='Blues',
                colorbar=dict(title=value_col)
            ))
            fig4.update_layout(title="Alunos por Dia e Distrito", xaxis_title="Dia", yaxis_title="Distrito", height=350)
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("Não foi possível identificar a coluna de valores numéricos para o heatmap.")
    else:
        st.info("Sem dados de alunos por dia e distrito.")
