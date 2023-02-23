from src.business_logic.common.protocols import IUoW
from src.business_logic.task.protocols.repository import (
    ITaskApplicationReader,
    ITaskApplicationRepository,
    ITaskReader,
    ITaskRepository,
)


class ITaskUoW(IUoW):
    task: ITaskRepository
    task_reader: ITaskReader
    task_appl: ITaskApplicationRepository
    task_appl_reader: ITaskApplicationReader
