from pydantic import BaseModel
from typing import Optional, Any, List, Literal

class User(BaseModel):
    username: str
    nameplate: str
    icon: str
    rating: Any

class ConfigData(BaseModel):
    table_type: Literal["分数列表", "b50", "完成表", "定数表"] = None
    level: Optional[str] = None
    version: Optional[str] = None
    completion: Literal["rate", "fc", "fc+", "ap", "ap+", "sync", "fs", "fs+", "fdx", "fdx+", "一星", "二星", "三星", "四星", "五星", "2星", "3星", "4星", "5星", ""] = None

    completion_type: str = None
    difficulty: List[Literal["basic", "advanced", "expert", "master", "remaster"]] = ["master", "remaster"]
    isfloat: bool = True
    isb50: bool = False

class MinfoData(BaseModel):
    type: Literal["sd", "dx"]
    level_index: int = 3
    minfo: Any

class FullPayload(BaseModel):
    user_data: Optional[User] = None
    scores_b50_data: Optional[Any] = None
    scores_data: Optional[Any] = None
    config_data: Optional[ConfigData] = None
    minfo_data: Optional[MinfoData] = None
