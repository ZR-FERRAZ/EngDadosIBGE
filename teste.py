from src.extract import Extract
from src.transform import Transform

dados = Extract().extract_pnadc()

for res in dados[0]["resultados"]:
    sexo = list(res["classificacoes"][0]["categoria"].values())[0]
    serie = res["series"][0]["serie"]
    sem_valor = [p for p, v in serie.items() if v in ("-", "...", "..", "X", None, "")]
    print(
        sexo,
        "| períodos na API:", len(serie),
        "| primeiro:", min(serie),
        "| último:", max(serie),
        "| sem valor:", len(sem_valor),
    )

df = Transform().transform_pnadc(dados)
print(df.groupby("sexo")["periodo"].agg(["min", "max", "count"]))