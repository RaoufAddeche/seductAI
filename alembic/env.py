# 📄 env.py — Configuration Alembic
# Permet d’inclure TOUS les modèles du projet (API + Graph)

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, MetaData
from alembic import context

# 🔧 Configuration de logging
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 📌 Importer les bases des modèles
from api.models.user import Base as UserBase
from model.db.models import Base as ModelBase  # contient Interaction

# 🔗 Fusionner toutes les metadata
combined_metadata = MetaData()
for base in [UserBase, ModelBase]:
    for table in base.metadata.tables.values():
        table.tometadata(combined_metadata)

# 🧠 C’est cette metadata qui sera utilisée par Alembic
target_metadata = combined_metadata

# 🔁 Mode offline
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

# 🔁 Mode online
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

# 🚀 Exécution selon le mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
