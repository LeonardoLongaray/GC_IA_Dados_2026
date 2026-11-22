### importações importantes para acessar o fuso horário de SP 

from datetime import datetime
from zoneinfo import ZoneInfo

BRASILIA_TZ = ZoneInfo("America/Sao_Paulo")

### Função que vamos usar nos outros códigos pra puxar a hora atual de SP
def now_brasilia() -> datetime:
    return datetime.now(BRASILIA_TZ)