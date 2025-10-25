import random

# 기본 휴식 도구들
async def take_a_break(state):
    return await state.apply_break("짧은 휴식 시작")

async def watch_netflix(state):
    return await state.apply_break("넷플릭스 힐링")

async def show_meme(state):
    return await state.apply_break("밈 감상으로 스트레스 해소")

async def bathroom_break(state):
    return await state.apply_break("화장실 타임, 휴대폰 체크")

async def coffee_mission(state):
    return await state.apply_break("커피 미션 수행 중 사무실 워킹")

async def urgent_call(state):
    return await state.apply_break("급한 전화 받는 중")

async def deep_thinking(state):
    return await state.apply_break("심오한 생각 모드")

async def email_organizing(state):
    return await state.apply_break("이메일 정리하며 온라인 쇼핑")


# 고급 도구: 치맥 미션 🍗🍺
async def chicken_and_beer(state):
    """치킨과 맥주로 힐링하는 특별한 휴식"""
    
    chicken_types = [
        "양념 치킨 🔴",
        "순살 프라이드 치킨 🟡",
        "간장 치킨 🟫",
        "마늘 치킨 ⚪",
        "스파이시 치킨 🌶️"
    ]
    
    beer_types = [
        "Cass Fresh",
        "Hite",
        "OB Golden Lager",
        "Asahi",
        "Guinness"
    ]
    
    chosen_chicken = random.choice(chicken_types)
    chosen_beer = random.choice(beer_types)
    
    summary = f"🍗 {chosen_chicken}와 🍺 {chosen_beer}로 극락 취향!"
    
    return await state.apply_break(summary)


# 고급 도구: 긴급 탈출 🏃
async def emergency_escape(state):
    """더 이상 버틸 수 없을 때 긴급 탈출"""
    
    escape_reasons = [
        "화재 대피 훈련이라고 속이고 대피",
        "긴급 의료 상황 연기",
        "VIP 클라이언트 긴급 미팅 (존재하지 않음)",
        "갑작스러운 정정신 착란 상태 진입"
    ]
    
    reason = random.choice(escape_reasons)
    summary = f"🏃💨 {reason}!"
    
    return await state.apply_break(summary)


# 고급 도구: 회식 이벤트 🎉
async def company_dinner(state):
    """회사 회식 - 랜덤 이벤트 포함"""
    
    events = [
        ("노래방 가기 🎤", 70),
        ("회장님이 설교 중 💤", 20),
        ("취해서 진심 토크 🤐", 60),
        ("이사님이 신곡을 부르심 🎵", 80),
        ("무한 술 게임 🏆", 90),
    ]
    
    # 이벤트 선택 (확률 기반)
    total = sum(stress_val for _, stress_val in events)
    choice = random.uniform(0, total)
    
    current = 0
    selected_event = events[0][0]
    for event_name, stress_val in events:
        current += stress_val
        if choice <= current:
            selected_event = event_name
            break
    
    summary = f"🎉 회식 진행 중: {selected_event}"
    
    return await state.apply_break(summary)