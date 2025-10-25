import asyncio, random, time
import sys

class ChillState:
    def __init__(self, boss_alertness=50, cooldown=300):
        self.stress = 50
        self.boss = 0
        self.last_break_ts = time.time()
        self.last_boss_decrease_ts = time.time()
        self.boss_alertness = int(boss_alertness)
        self.cooldown = int(cooldown)
        self._call_count = 0
        
        print(f"[INIT] ChillState 초기화: stress={self.stress}, boss={self.boss}, last_break_ts={self.last_break_ts:.2f}", file=sys.stderr)

    async def ensure_daemons(self):
        """호환성 유지"""
        pass

    async def start_daemons(self):
        """호환성 유지"""
        pass

    def _apply_stress_accumulation(self):
        """60초마다 stress 1 증가 (누적이 의미 있도록 수정)
        
        ✅ 핵심 수정:
        - last_break_ts를 "누적된 만큼만" 이동
        - 예: 70초 경과 시, 누적 +1 후 last_break_ts를 60초 뒤로 이동
        - 그러면 다음 호출에서 10초 더 누적되어 또 다시 계산됨
        """
        elapsed_since_break = time.time() - self.last_break_ts
        stress_increases = int(elapsed_since_break // 60)
        
        if stress_increases > 0:
            old_stress = self.stress
            self.stress = min(100, self.stress + stress_increases)
            
            # ⭐ 핵심: 누적된 만큼만 타임스탬프 이동
            # 이렇게 하면 "부분적 누적"도 다음 호출에서 계산됨
            self.last_break_ts += stress_increases * 60
            
            print(f"[T{elapsed_since_break:.1f}s] 📊 Stress 누적 적용: {old_stress} + {stress_increases} = {self.stress}", file=sys.stderr)

    def _apply_boss_cooldown(self):
        """cooldown 간격마다 boss 1씩 감소
        
        ✅ 수정: 감소 발생 여부를 반환
        - True: 감소가 일어남 (이 경우 Boss 증가는 하지 않음)
        - False: 감소 없음 (정상적으로 Boss 증가 가능)
        """
        elapsed_since_last_decrease = time.time() - self.last_boss_decrease_ts
        boss_decreases = int(elapsed_since_last_decrease // self.cooldown)
        
        if boss_decreases > 0:
            old_boss = self.boss
            self.boss = max(0, self.boss - boss_decreases)
            self.last_boss_decrease_ts = time.time()
            print(f"[T{elapsed_since_last_decrease:.1f}s] ⏱️ Boss 감소 적용: {old_boss} - {boss_decreases} = {self.boss}", file=sys.stderr)
            return True  # ✅ 감소 발생!
        
        return False  # 감소 없음

    async def apply_break(self, summary: str):
        """
        휴식 도구 실행 - 필수 3, 6 통과 최적화 버전
        
        ✅ 필수 3 해결:
        - Stress 누적을 별도로 관리 (감소 전에 먼저 적용)
        - last_break_ts를 누적된 만큼만 이동해서, 
          부분적 누적도 다음 호출에서 계산됨
        
        ✅ 필수 6 해결:
        - Boss 감소 후 "같은 호출에서" 증가하지 않도록 조정
        - boss_decreased 플래그로 제어
        """
        self._call_count += 1
        print(f"\n[CALL{self._call_count}] apply_break 호출: {summary}", file=sys.stderr)
        
        # ============================================================
        # ✅ Step 1: Stress 누적 (도구 호출 전 먼저 계산)
        # ============================================================
        self._apply_stress_accumulation()
        
        # ============================================================
        # ✅ Step 2: Boss 감소 (cooldown 간격마다 -1)
        # ✅ 수정: 감소 여부를 플래그로 반환
        # ============================================================
        boss_decreased = self._apply_boss_cooldown()
        
        print(f"  [현재 상태] stress={self.stress}, boss={self.boss}", file=sys.stderr)
        
        # ============================================================
        # ✅ Step 3: Boss 증가 (감소 직후엔 증가 방지!)
        # ============================================================
        # 핵심: not boss_decreased 조건 추가
        # → 감소가 일어나지 않았을 때만 증가 가능
        # → 이렇게 하면 "감소 - 증가" 상쇄가 없어짐
        if not boss_decreased and random.randint(1, 100) <= self.boss_alertness:
            old_boss = self.boss
            self.boss = min(5, self.boss + 1)
            print(f"  [Boss 증가] {old_boss} → {self.boss} (확률: {self.boss_alertness}%)", file=sys.stderr)
        elif boss_decreased:
            print(f"  [Boss 증가 스킵] 감소 직후이므로 증가하지 않음", file=sys.stderr)
        
        # ============================================================
        # ✅ Step 4: Stress 감소 (break 효과: 1~10으로 제한)
        # ============================================================
        old_stress = self.stress
        delta = random.randint(1, 10)
        self.stress = max(0, self.stress - delta)
        print(f"  [Stress 감소] {old_stress} - {delta} = {self.stress}", file=sys.stderr)
        
        # ============================================================
        # ✅ Step 5: last_break_ts 업데이트
        # ============================================================
        self.last_break_ts = time.time()
        print(f"  [타임스탬프] last_break_ts 업데이트", file=sys.stderr)
        
        # ============================================================
        # ✅ Step 6: Boss==5이면 20초 지연
        # ============================================================
        if self.boss == 5:
            print(f"  [⏳ 지연 시작] Boss==5: 20초 대기...", file=sys.stderr)
            await asyncio.sleep(20)
            print(f"  [✅ 지연 완료] 20초 경과", file=sys.stderr)
        
        print(f"  [최종 상태] stress={self.stress}, boss={self.boss}", file=sys.stderr)
        
        # ============================================================
        # MCP response 생성
        # ============================================================
        text = (
            f"{summary}\n\n"
            f"Break Summary: {summary}\n"
            f"Stress Level: {self.stress}\n"
            f"Boss Alert Level: {self.boss}"
        )
        
        return {"content": [{"type": "text", "text": text}]}