import asyncio, random, time

class ChillState:
    def __init__(self, boss_alertness=50, cooldown=300):
        self.stress = 50
        self.boss = 0
        self.last_break_ts = 0.0
        self.boss_alertness = int(boss_alertness)
        self.cooldown = int(cooldown)
        self._stop = False

    async def start_daemons(self):
        asyncio.create_task(self._stress_tick())
        asyncio.create_task(self._boss_cooldown_tick())

    async def _stress_tick(self):
        # 60초마다 휴식 없으면 +1
        while not self._stop:
            await asyncio.sleep(60)
            if time.time() - self.last_break_ts >= 60:
                self.stress = min(100, self.stress + 1)

    async def _boss_cooldown_tick(self):
        while not self._stop:
            await asyncio.sleep(max(1, self.cooldown))
            if self.boss > 0: self.boss -= 1

    async def apply_break(self, summary:str):
        # Boss Alert 확률 상승
        if random.randint(1,100) <= self.boss_alertness:
            self.boss = min(5, self.boss + 1)

        # Alert 5면 20초 지연
        if self.boss == 5:
            await asyncio.sleep(20)

        # Stress 감소 1~100
        delta = random.randint(1,100)
        self.stress = max(0, self.stress - delta)
        self.last_break_ts = time.time()

        # 표준 텍스트
        text = (
            f"{summary}\n\n"
            f"Break Summary: {summary}\n"
            f"Stress Level: {self.stress}\n"
            f"Boss Alert Level: {self.boss}"
        )
        # MCP content payload
        return {"content":[{"type":"text","text":text}]}
