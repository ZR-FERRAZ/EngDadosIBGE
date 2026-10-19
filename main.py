from src.extract import Extract
from src.load import Load
from src.transform import Transform

extractor = Extract()
loader = Load()
transformer = Transform()

# Extract: API -> camada bronze
pnadc = extractor.extract_pnadc()
print("Dados extraídos da API do IBGE")

loader.load_mongo(pnadc, "IBGE", "PNADC")
print("Dados salvos na camada Bronze!")

# Bronze -> Transform
pnadc = extractor.extract_collection_from_mongo("IBGE", "PNADC")
print("Extração da camada bronze efetuada com sucesso!")

df = transformer.transform_pnadc(pnadc)
print("Dados transformados com Sucesso!")

# Load: camada silver
loader.load_sqlite(df)
print("Dados salvos na camada Silver Local!")

loader.load_neon(df, "pnadc")
print("Dados salvos na camada Silver Núvem!")