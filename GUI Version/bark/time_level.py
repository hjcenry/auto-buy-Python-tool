from enum import Enum


class TimeLevel(Enum):
    # 默认值，系统立即亮屏显示通知
    ACTIVE = "active"
    # 时效性通知，可在专注状态下显示通知
    TIME_SENSITIVE = "timeSensitive"
    # 仅将通知添加到通知列表，不会亮屏体型
    PASSIVE = "passive"
