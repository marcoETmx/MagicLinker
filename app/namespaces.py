from flask_restx import Namespace

shortener_ns = Namespace(
    "shortener", description="Operaciones relacionadas con el acortamiento de URLs"
)
root_ns = Namespace(
    "root", description="Operaciones relacionadas con la raíz de la API"
)
