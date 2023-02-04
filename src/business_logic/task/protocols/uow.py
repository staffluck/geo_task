from src.business_logic.common.protocols import IUoW
from src.business_logic.task.protocols.repository import ITaskReader, ITaskRepository


class ITaskUoW(IUoW):
    task: ITaskRepository
    task_reader: ITaskReader
