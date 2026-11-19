import logging
import os

# Ruta fija: el log se guarda siempre junto a este archivo
RUTA_LOG = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "eventos.log"
)

logging.basicConfig(
    filename=RUTA_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    force=True,
)


def registrar_evento(mensaje):
    logging.info(mensaje)


def registrar_error(mensaje):
    logging.error(mensaje)
