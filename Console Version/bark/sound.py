from enum import Enum


class SoundType(Enum):
    """
    通知音效枚举
    """
    # 2s
    ALARM = "alarm"
    # 4.5s
    ANTICIPATE = "anticipate"
    # 1.4s
    BELL = "bell"
    # 0.67s
    BIRD_SONG = "birdsong"
    # 1.6s
    BLOOM = "bloom"
    # 0.9s
    CALYPSO = "calypso"
    # 4.5s
    CHIME = "chime"
    # 2.2s
    CHOO = "choo"
    # 1.9s
    DESCENT = "descent"
    # 1.5s
    ELECTRONIC = "electronic"
    # 1.5s
    FANFARE = "fanfare"
    # 1.7s
    GLASS = "glass"
    # 3s
    GOTO_SLEEP = "gotosleep"
    # 1.8s
    HEALTH_NOTIFICATION = "healthnotification"
    # 1.5s
    HORN = "horn"
    # 1.3s
    LADDER = "ladder"
    # 1.5s
    MAIL_SENT = "mailsent"
    # 7s
    MINUET = "minuet"
    # 2.2s
    MULTI_WAY_INVITATION = "multiwayinvitation"
    # 1.5s
    NEW_MAIL = "newmail"
    # 2.9s
    NEWS_FLASH = "newsflash"
    # 1.9s
    noir = "noir"
    # 1.4s
    PAYMENT_SUCCESS = "paymentsuccess"
    # 0.6s
    SHAKE = "shake"
    # 4.7s
    SHERWOOD_FOREST = "sherwoodforest"
    # 0.5s
    SILENCE = "silence"
    # 2.9s
    SPELL = "spell"
    # 4.2s
    SUSPENSE = "suspense"
    # 1.2s
    TELEGRAPH = "telegraph"
    # 1.5s
    TIPTOES = "tiptoes"
    # 2.6s
    TYPE_WRITERS = "typewriters"
    # 4.5s
    UPDATE = "update"
