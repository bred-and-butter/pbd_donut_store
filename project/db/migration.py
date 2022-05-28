import psycopg2
from peewee import (
    Model,
    PostgresqlDatabase,
    AutoField,
    TextField,
    IntegerField,
    FloatField,
    DateTimeField,
    ForeignKeyField,
)

from project.configs import DB

db = PostgresqlDatabase(
    database=DB["name"],
    user=DB["LOGIN"]["user"],
    password=DB["LOGIN"]["user"],
    host=DB["host"],
    port=DB["port"],
    autoconnect=False
)


class BaseModel(Model):
    codigo = AutoField()

    class Meta:
        database = db


class Cliente(BaseModel):
    cpf = TextField(unique=True)
    nome = TextField()
    telefone = TextField(null=True)
    endereco = TextField(null=True)
    num_compras = IntegerField(default=0)


class Compra(BaseModel):
    precototal = FloatField()
    datacompra = DateTimeField()
    codcliente = ForeignKeyField(Cliente, backref="purchases")


class Filial(BaseModel):
    nome = TextField()
    endereco = TextField()


class SaborDonut(BaseModel):
    nome = TextField()
    preco = FloatField()
    numvendas = IntegerField(default=0)
    ingrediente = TextField(null=False)
    tipo = IntegerField()


class Funcionario(BaseModel):
    nome = TextField()
    cpf = TextField(unique=True)
    cargo = TextField()
    salario = FloatField()
    dataemissao = DateTimeField()
    datasaida = DateTimeField()
    codfilial = ForeignKeyField(Filial, backref="funcionarios")


class Filial_SaborDonut(BaseModel):
    codfilial = ForeignKeyField(Filial, backref="filial_sabordonut")
    codsabor = ForeignKeyField(SaborDonut, backref="filial_sabordonut")


class Filial_Compra(BaseModel):
    codfilial = ForeignKeyField(Filial, backref="filial_compra")
    codcompra = ForeignKeyField(Compra, backref="filial_compra")


class SaborDonut_Compra(BaseModel):
    codsabor = ForeignKeyField(SaborDonut, backref="sabordonut_compra")
    codcompra = ForeignKeyField(Compra, backref="sabordonut_compra")
    quantidade = IntegerField(default=0)


def init_db():
    with db.connection_context():
        db.create_tables(
            [
                Cliente,
                Compra,
                Filial,
                SaborDonut,
                Funcionario,
                Filial_SaborDonut,
                Filial_Compra,
                SaborDonut_Compra
            ],
            safe=True
        )


if __name__ == '__main__':
    init_db()
