
def get_or_create(session, dbModel, **kwargs):
    instance = session.query(dbModel).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = dbModel(**kwargs)
        session.add(instance)
        session.commit()
        return instance