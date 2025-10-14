class OficialExepctions(Exception):
    """Lanzado cuando fallan las reglas de negocio de oficial"""
    pass

class OficialValidationError(OficialExepctions):
    """Lanzado cuando los campos del oficial no son válidos"""
    pass

class OficialNotFoundError(OficialExepctions):
    """Lanzado cuando no se encontro un oficial"""
    pass

class OficialAlreadyExistsError(OficialExepctions):
    """Lanzado cuando se intenta registrar un oficial que ya existe"""
    pass

class OficialNotInAuthError(OficialExepctions):
    """Lanzado cuando no se envía un mensaje correctamente"""
    pass

class NotMatchingTurnEnumError(OficialExepctions):
    """Lanzado cuando no hace match el valor de un enum 'Turn' en la base de datos, no corresponde a uno del sistema."""
    pass

class NotMatchingFreeDaysEnumError(OficialExepctions):
    """Lanzado cuando no hace match el valor de un enum 'FreeDays' en la base de datos, no corresponde a uno del sistema."""
    pass

class NotMatchingTurnValueError(OficialExepctions):
    """Lanzado cuando no hace match el enum 'Turn'con un valor del sistema."""
    pass

class NotMatchingFreeDaysValueError(OficialExepctions):
    """Lanzado cuando no hace match el enum 'FreeDays'con un valor del sistema."""
    pass

class OficialAlreadyDeactivatedError(OficialExepctions):
    """Lanzado cuando no hace match el enum 'FreeDays'con un valor del sistema."""
    pass