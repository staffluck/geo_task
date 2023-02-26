from src.business_logic.task.access_policy import TaskApplicationAccessPolicy
from src.business_logic.task.dto.task_application import (
    TaskApplicationCreate,
    TaskApplicationDetail,
    TaskApplicationDTO,
)
from src.business_logic.task.entities.task_application import TaskApplication
from src.business_logic.task.exceptions.task_application import (
    TaskApplicationAlreadyExistsError,
    TaskApplicationByOwnerError,
)
from src.business_logic.task.protocols.uow import ITaskApplicationUoW


class TaskApplicationService:
    def __init__(
        self,
        task_appl_uow: ITaskApplicationUoW,
        access_policy: TaskApplicationAccessPolicy,
    ) -> None:
        self.task_appl_uow = task_appl_uow
        self.access_policy = access_policy

    async def add_application(
        self, task_application_data: TaskApplicationCreate
    ) -> TaskApplicationDTO:
        if await self.task_appl_uow.task_appl.user_has_application(
            task_application_data.user.id, task_application_data.task_id
        ):
            raise TaskApplicationAlreadyExistsError(["user"])
        task = await self.task_appl_uow.task.get_task_by_id(
            task_application_data.task_id
        )
        if task.owner_id == task_application_data.user.id:
            raise TaskApplicationByOwnerError()
        task_appl = TaskApplication.create(
            task_id=task_application_data.task_id,
            user_id=task_application_data.user.id,
            text=task_application_data.text,
        )
        task_appl_in_db = await self.task_appl_uow.task_appl.create_application(
            task_appl
        )
        await self.task_appl_uow.commit()
        return TaskApplicationDTO.from_orm(task_appl_in_db)

    async def get_user_task_applications(
        self, user_id: int, limit: int = 100, offset: int = 0
    ) -> list[TaskApplicationDetail]:
        task_appls = (
            await self.task_appl_uow.task_appl_reader.get_user_task_applications(
                user_id, limit=limit, offset=offset
            )
        )
        return task_appls
