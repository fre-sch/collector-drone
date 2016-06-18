from errors import ServiceError
from sqlalchemy import or_, and_, not_


def model_filter(crit, model):
    try:
        if crit.op == "and":
            return and_(*[model_filter(it, model) for it in crit.value])
        elif crit.op == "or":
            return or_(*[model_filter(it, model) for it in crit.value])
        elif crit.op == "eq":
            return getattr(model, crit.field) == crit.value
        elif crit.op == "ilike":
            return getattr(model, crit.field).ilike(crit.value)
        elif crit.op == "neq":
            return getattr(model, crit.field) != crit.value
        elif crit.op == "gt":
            return getattr(model, crit.field) > crit.value
        elif crit.op == "lt":
            return getattr(model, crit.field) < crit.value
        elif crit.op == "gte":
            return getattr(model, crit.field) >= crit.value
        elif crit.op == "lte":
            return getattr(model, crit.field) <= crit.value
        elif crit.op == "null":
            return getattr(model, crit.field) == None
        elif crit.op == "notnull":
            return getattr(model, crit.field) != None
        elif crit.op == "not":
            return not_(model_filter(crit.value, model))
    except AttributeError:
        raise ServiceError("invalid query field %s" % crit.field)

