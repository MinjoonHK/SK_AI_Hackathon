#기본휴식도구 모음

#짧은 휴식 취하기
async def take_a_break(state):
    return await state.apply_break("짧은 휴식 시작")

#넷플릭스 시청하기
async def watch_netflix(state):
    return await state.apply_break("넷플릭스 힐링")

#밈 감상하기
async def show_meme(state):
    return await state.apply_break("밈 감상으로 스트레스 해소")

#화장실 다녀오기
async def bathroom_break(state):
    return await state.apply_break("화장실 타임, 휴대폰 체크")

#커피미션(캐시워크) 진행하기
async def coffee_mission(state):
    return await state.apply_break("커피 미션 수행 중 사무실 워킹")

#급한 전화 받기
async def urgent_call(state):
    return await state.apply_break("급한 전화 받는 중")

#심오한 생각중
async def deep_thinking(state):
    return await state.apply_break("심오한 생각 모드")

#이메일 정리하기
async def email_organizing(state):
    return await state.apply_break("이메일 정리하며 온라인 쇼핑")