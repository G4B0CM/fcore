class RolesExepctions(Exception):
    """Lanzado cuando fallan las reglas de negocio de rol"""
    pass

class RolesValidationError(ValueError):
    """Lanzado cuando los campos del rol no son válidos"""
    pass

class RolNotFoundError(RolesExepctions):
    """Lanzado cuando no se encuentra un rol"""
    pass

class RolAlreadyExistsError(RolesExepctions):
    """Lanzado cuando no se encuentra un rol"""
    pass

class RolAlreadyDeactivatedError(RolesExepctions):
    """Lanzado cuando un rol ya esta desactivado"""
    pass
