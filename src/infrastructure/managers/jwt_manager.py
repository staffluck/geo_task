from datetime import datetime, timedelta
from enum import Enum

from jose import JWTError, jwt

from src.business_logic.common.exceptions import BadJWTTokenError
from src.business_logic.user.dto.auth import AccessTokenData, RefreshTokenData
from src.business_logic.user.protocols.security import IJWTManager
from src.config import SecuritySettings


class JWTType(Enum):
    REFRESH_TOKEN = "refresh"
    ACCESS_TOKEN = "access"


class JWTManager(IJWTManager):
    def __init__(self, security_settings: SecuritySettings) -> None:
        self.settings = security_settings

    def create_access_token(self, token_data: AccessTokenData) -> str:
        return self._create_jwt(
            {"sub": str(token_data.user_id), "type": JWTType.ACCESS_TOKEN.value},
            expires_delta=timedelta(minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    def create_refresh_token(self, token_data: RefreshTokenData) -> str:
        return self._create_jwt(
            {"sub": str(token_data.user_id), "type": JWTType.REFRESH_TOKEN.value},
            expires_delta=timedelta(minutes=self.settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        )

    def _create_jwt(self, data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode["exp"] = expire
        encoded_jwt = jwt.encode(
            to_encode, self.settings.SECRET_KEY, algorithm=self.settings.ALGORITHM
        )
        return encoded_jwt

    def decode_access_token(self, access_token: str) -> AccessTokenData:
        token_data = self._decode_jwt(access_token, JWTType.ACCESS_TOKEN)
        return AccessTokenData(user_id=token_data["sub"])

    def decode_refresh_token(self, refresh_token: str) -> RefreshTokenData:
        token_data = self._decode_jwt(refresh_token, JWTType.REFRESH_TOKEN)
        return RefreshTokenData(user_id=token_data["sub"])

    def _decode_jwt(self, jwt_token: str, token_type: JWTType) -> dict:
        jwt_exception = BadJWTTokenError()
        try:
            payload = jwt.decode(
                jwt_token,
                self.settings.SECRET_KEY,
                algorithms=[self.settings.ALGORITHM],
            )
        except JWTError as e:
            raise jwt_exception from e
        try:
            input_token_type = JWTType(payload["type"])
        except ValueError:
            raise jwt_exception
        if input_token_type != token_type:
            raise jwt_exception
        return payload
