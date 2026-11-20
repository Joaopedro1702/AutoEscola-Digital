# Dashboard Autoescola

Dashboard Streamlit com layout baseado no PDF do Projeto Integrador.

## Instalação

```bash
pip install -r requirements.txt
streamlit run projeto_streamlit.py
```

O dashboard usa a aba `Aulas` de `dados/Autoescola.xlsx` como fonte principal (ou `dados/Autoescola_Aulas.csv` como alternativa). Não soma ambas as fontes, pois representam os mesmos registros. Os acessos da SENATRAN são exibidos em painel complementar.

O total de aulas é a **soma** da coluna `Quantidade_Aulas`, não a quantidade de linhas. A média de satisfação usa `Avaliacao`. A distribuição de satisfação usa `Perfil` quando presente.
