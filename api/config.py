from enum import Enum
from typing import Dict


class Stage(str, Enum):
    TEST = "TEST"
    DEV = "DEV"
    STAGE = "STAGE"
    PROD = "PROD"


auth_postfix = "/auth/realms/rrap"

AUTH_SERVER_STAGE_MAP: Dict[Stage, str] = {
    Stage.TEST: "https://auth.dev.rrap-is.com" + auth_postfix,
    Stage.DEV: "https://auth.dev.rrap-is.com" + auth_postfix,
    Stage.STAGE: "https://auth.stage.rrap-is.com" + auth_postfix,
    Stage.PROD: "https://auth.mds.gbrrestoration.org" + auth_postfix,
}
