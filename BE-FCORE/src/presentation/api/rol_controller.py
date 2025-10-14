from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from src.application.ports.input.i_admin_rol_use_case import IAdminRolUseCase
from src.presentation.dependencies.rol_dependencies import get_admin_rol_use_case
from src.presentation.dtos.rol_dto import CreateRolDto, UpdateRolDto, RolResponseDto
from src.core.errors.roles_exceptions import RolNotFoundError, RolAlreadyExistsError

rol_router = APIRouter(prefix="/roles", tags=["Roles"])

@rol_router.post("/", response_model=RolResponseDto, status_code=status.HTTP_201_CREATED)
def create_rol(
    request: CreateRolDto,
    use_case: IAdminRolUseCase = Depends(get_admin_rol_use_case)
):
    try:
        command = request.to_command()
        created_rol = use_case.create_rol(command)
        return RolResponseDto.from_entity(created_rol)
    except RolAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@rol_router.get("/", response_model=List[RolResponseDto])
def get_all_roles(use_case: IAdminRolUseCase = Depends(get_admin_rol_use_case)):
    roles = use_case.get_all_roles()
    return [RolResponseDto.from_entity(rol) for rol in roles]

@rol_router.get("/find_by_id/{id_rol}", status_code=status.HTTP_200_OK)
def find_rol_by_id(
    id_rol : int,
    admin_rol_use : IAdminRolUseCase = Depends(get_admin_rol_use_case) 
):
    try:
        result = admin_rol_use.get_rol_by_id(id_rol)
        return result
    except RolNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@rol_router.put("/{rol_id}", response_model=RolResponseDto)
def update_rol(
    rol_id: int,
    request: UpdateRolDto,
    use_case: IAdminRolUseCase = Depends(get_admin_rol_use_case)
):
    try:
        command = request.to_command(rol_id=rol_id)
        updated_rol = use_case.update_rol(command)
        return RolResponseDto.from_entity(updated_rol)
    except (RolNotFoundError, RolAlreadyExistsError) as e:
        status_code = status.HTTP_404_NOT_FOUND if isinstance(e, RolNotFoundError) else status.HTTP_409_CONFLICT
        raise HTTPException(status_code=status_code, detail=str(e))
    
@rol_router.get("/deactivate/{id}", status_code=status.HTTP_200_OK)
def deactivate_rol(
    id : int,
    admin_rol_use: IAdminRolUseCase = Depends(get_admin_rol_use_case)
):
    try:
        result = admin_rol_use.deactivate_rol(id)
        return result
    except RolNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )