#fast-api
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter

#Aplicación
from src.application.ports.input.i_admin_oficial_use_case import IAdminOficialUseCase
from src.application.models.rol_commands import AssignRolCommand
#Presentación
from src.presentation.dtos.oficial_dto import CreateOficialDto, UpdateOficialDto, ResponseOficialDto
from src.presentation.dependencies.oficial_dependencies import get_admin_oficial_use_case
#Errores
from src.core.errors.oficial_exceptions import OficialAlreadyExistsError, OficialNotFoundError, OficialNotInAuthError ,OficialAlreadyDeactivatedError,OficialValidationError
from src.core.errors.roles_exceptions import RolNotFoundError

oficial_router = APIRouter(
    prefix="/oficial",
    tags=["oficial"],
    responses={404: {"description": "Not found"}, 409: {"description": "Oficial ya registrado"}}, # Respuestas personalizadas
)

@oficial_router.post("/create", status_code=status.HTTP_200_OK)
def create_oficial(
    request: CreateOficialDto,
    admin_oficial_use : IAdminOficialUseCase = Depends(get_admin_oficial_use_case),
):
    try:
        command = request.to_command()
        result = admin_oficial_use.create_oficial(command)
        return ResponseOficialDto.from_entity(oficial=result)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=str(e)
        )
    except OficialAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except OficialNotInAuthError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except OficialValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=str(e)
        )
    
@oficial_router.get("/list", status_code=status.HTTP_200_OK)
def get_oficiales(
    admin_oficial_use : IAdminOficialUseCase = Depends(get_admin_oficial_use_case)
):
    try:
        result = admin_oficial_use.get_all_oficiales()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
@oficial_router.get("/find_by_id/{id_oficial}", status_code=status.HTTP_200_OK)
def find_by_id_oficial(
    id_oficial : int,
    admin_oficial_use : IAdminOficialUseCase = Depends(get_admin_oficial_use_case) 
):
    try:
        result = admin_oficial_use.get_oficial_by_id(id_oficial)
        return result
    except OficialNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    
@oficial_router.get("/find_by_qcode/{qcode}", status_code=status.HTTP_200_OK)
def find_by_qcode_oficial(
    qcode : str,
    admin_oficial_use: IAdminOficialUseCase = Depends(get_admin_oficial_use_case)
):
    try:
        result = admin_oficial_use.get_oficial_by_qcode(qcode)
        return result
    except OficialNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
        
@oficial_router.post("/update", status_code=status.HTTP_200_OK)
def update_oficial(
    request: UpdateOficialDto,
    admin_oficial_use: IAdminOficialUseCase = Depends(get_admin_oficial_use_case)
):
    try:
        command = request.to_command()
        result = admin_oficial_use.update_oficial(command)
        return result
    except OficialNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@oficial_router.get("/deactivate/{qcode}", status_code=status.HTTP_200_OK)
def deactivate_oficial(
    qcode : str,
    admin_oficial_use: IAdminOficialUseCase = Depends(get_admin_oficial_use_case)
):
    try:
        result = admin_oficial_use.deactivate_oficial(qcode)
        return result
    except OficialAlreadyDeactivatedError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except OficialNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@oficial_router.post("/{oficial_id}/roles/{rol_id}", response_model=ResponseOficialDto, status_code=status.HTTP_200_OK)
def assign_rol_to_oficial(
    oficial_id: int,
    rol_id: int,
    use_case: IAdminOficialUseCase = Depends(get_admin_oficial_use_case)
):
    try:
        command = AssignRolCommand(oficial_id=oficial_id, rol_id=rol_id)
        updated_oficial = use_case.assign_rol_to_oficial(command)
        return ResponseOficialDto.from_entity(updated_oficial)
    except (OficialNotFoundError, RolNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@oficial_router.delete("/{oficial_id}/roles/{rol_id}", response_model=ResponseOficialDto, status_code=status.HTTP_200_OK)
def remove_rol_from_oficial(
    oficial_id: int,
    rol_id: int,
    use_case: IAdminOficialUseCase = Depends(get_admin_oficial_use_case)
):
    try:
        command = AssignRolCommand(oficial_id=oficial_id, rol_id=rol_id)
        updated_oficial = use_case.remove_rol_from_oficial(command)
        return ResponseOficialDto.from_entity(updated_oficial)
    except (OficialNotFoundError, RolNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@oficial_router.get("/{oficial_id}/roles", status_code=status.HTTP_200_OK)
def get_roles_for_oficial(
    oficial_id: int,
    admin_oficial_use: IAdminOficialUseCase = Depends(get_admin_oficial_use_case)
):
    """
    Obtiene todas las secciones de marca asignadas a un oficial específico.
    """
    try:
        roles = admin_oficial_use.get_roles_assigned(oficial_id)
        return roles
        
    except OficialNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )