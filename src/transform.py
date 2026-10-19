import pandas as pd


class Transform:
    def transform_pnadc(self, pnadc):
        linhas = []
        for variavel in pnadc:
            for resultado in variavel["resultados"]:
                # ex.: {"6794": "Total"} -> "Total"
                sexo = list(resultado["classificacoes"][0]["categoria"].values())[0]
                for serie in resultado["series"]:
                    for cod_periodo, valor in serie["serie"].items():
                        linhas.append(
                            {"sexo": sexo, "cod_periodo": cod_periodo, "valor": valor}
                        )

        df = pd.DataFrame(linhas)

        # "-" ou "..." (sem dado) viram NaN
        df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

        # 201203 -> ano "2012", trimestre 3
        df["ano"] = df["cod_periodo"].str[:4]
        df["tri"] = df["cod_periodo"].str[4:].astype("int64")

        # primeiro dia do trimestre: tri 1 -> jan, 2 -> abr, 3 -> jul, 4 -> out
        mes = ((df["tri"] - 1) * 3 + 1).astype(str).str.zfill(2)
        df["periodo"] = pd.to_datetime(df["ano"] + "-" + mes + "-01")

        df = df.dropna(subset=["valor"]).drop(columns="cod_periodo")
        return df[["periodo", "valor", "ano", "tri", "sexo"]]