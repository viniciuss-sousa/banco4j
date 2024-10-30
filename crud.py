from neo4j import GraphDatabase

class Neo4jCRUD:
    def __init__(self, uri, usuario, senha):
        self.driver = GraphDatabase.driver(uri, auth=(usuario, senha))

    def fechar(self):
        self.driver.close()

    def criar_no(self, etiqueta, propriedades):
        with self.driver.session() as sessao:
            consulta = f"CREATE (n:{etiqueta} {{ {', '.join([f'{k}: ${k}' for k in propriedades.keys()])} }}) RETURN n"
            resultado = sessao.run(consulta, propriedades)
            return resultado.single()

    def ler_no(self, etiqueta, chave_propriedade, valor_propriedade):
        with self.driver.session() as sessao:
            consulta = f"MATCH (n:{etiqueta} {{ {chave_propriedade}: ${chave_propriedade} }}) RETURN n"
            resultado = sessao.run(consulta, {chave_propriedade: valor_propriedade})
            return [registro["n"] for registro in resultado]

    def atualizar_no(self, etiqueta, chave_propriedade, valor_propriedade, atualizacoes):
        with self.driver.session() as sessao:
            set_clause = ', '.join([f'n.{k} = ${k}' for k in atualizacoes.keys()])
            consulta = f"MATCH (n:{etiqueta} {{ {chave_propriedade}: ${chave_propriedade} }}) SET {set_clause} RETURN n"
            parametros = {**{chave_propriedade: valor_propriedade}, **atualizacoes}
            resultado = sessao.run(consulta, parametros)
            return resultado.single()

    def deletar_no(self, etiqueta, chave_propriedade, valor_propriedade):
        with self.driver.session() as sessao:
            consulta = f"MATCH (n:{etiqueta} {{ {chave_propriedade}: ${chave_propriedade} }}) DELETE n"
            sessao.run(consulta, {chave_propriedade: valor_propriedade})

crud = Neo4jCRUD("bolt://localhost:7687", "neo4j", "12345678")
crud.criar_no("Pessoa", {"nome": "Vinicius", "idade": 25})
print(crud.ler_no("Pessoa", "nome", "Vinicius"))
crud.atualizar_no("Pessoa", "nome", "Vinicius", {"idade": 26})
crud.deletar_no("Pessoa", "nome", "Vinicius")
crud.fechar()
