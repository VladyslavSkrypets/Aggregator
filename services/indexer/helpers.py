from services.indexer.database import init_prod_db, ServicesInfo

db = init_prod_db()


def update_service_state(service_type: str, is_active: bool) -> None:
    (
        db.query(ServicesInfo)
        .filter(ServicesInfo.service_type.like(service_type))
        .update({'is_active': is_active}, synchronize_session=False)
    )
    db.commit()
