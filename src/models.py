from pydantic import BaseModel
from typing import Optional, Any, List, Literal

class User(BaseModel):
    username: str
    nameplate: str
    icon: str

class ConfigData(BaseModel):
    table_type: Literal["分数列表", "b50", "完成表", "定数表"] = None
    level: Optional[str] = None
    version: Optional[str] = None
    completion: Literal["rate", "fc", "fs", "ap"] = None
    difficulty: List[Literal["basic", "advanced", "expert", "master", "remaster"]] = ["expert", "master", "remaster"]
    isfloat: bool = True
    isb50: bool = False

class FullPayload(BaseModel):
    user_data: Optional[User] = None
    scores_b50_data: Optional[Any] = None
    scores_data: Optional[Any] = None
    config_data: Optional[ConfigData] = None
