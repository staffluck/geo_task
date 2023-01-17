from src.business_logic.common.protocols import IUoW
from src.business_logic.user.protocols.repository import IUserRepoistory


class IUserUoW(IUoW):
    user: IUserRepoistory
