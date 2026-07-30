from client import analisar_curriculo

curriculo_teste = "Rafael Ferreira, estudante de ADS, experiência com React, Java Spring Boot..."
vaga_teste = "Vaga de estágio dev backend, Python, FastAPI, PostgreSQL..."

resultado = analisar_curriculo(curriculo_teste, vaga_teste)
print(resultado)