from src.business_logic.common.protocols import IUoW
from src.business_logic.task.protocols.repository import ITaskRepository


class ITaskUoW(IUoW):
    task: ITaskRepository
