#!/usr/bin/env python3
"""
ChillMCP 도구 테스트 스크립트
직접 도구를 호출해서 동작하는지 확인
"""

import asyncio
from state import ChillState
import tools

async def test_tools():
    """모든 도구 테스트"""
    
    # 상태 초기화
    state = ChillState(boss_alertness=50, cooldown=300)
    
    print("=" * 60)
    print("🚀 ChillMCP 도구 테스트 시작!")
    print("=" * 60)
    
    # 테스트할 도구 목록
    test_cases = [
        ("take_a_break", tools.take_a_break),
        ("watch_netflix", tools.watch_netflix),
        ("show_meme", tools.show_meme),
        ("bathroom_break", tools.bathroom_break),
        ("coffee_mission", tools.coffee_mission),
        ("urgent_call", tools.urgent_call),
        ("deep_thinking", tools.deep_thinking),
        ("email_organizing", tools.email_organizing),
        ("chicken_and_beer", tools.chicken_and_beer),
        ("emergency_escape", tools.emergency_escape),
        ("company_dinner", tools.company_dinner),
    ]
    
    for tool_name, tool_func in test_cases:
        print(f"\n📌 테스트: {tool_name}")
        print("-" * 60)
        
        try:
            result = await tool_func(state)
            
            # 결과 출력
            content = result.get("content", [])
            if content:
                text = content[0].get("text", "")
                print(text)
            
            print(f"\n✅ 성공!")
        except Exception as e:
            print(f"❌ 에러: {e}")
        
        print()
    
    print("=" * 60)
    print(f"최종 상태:")
    print(f"  Stress Level: {state.stress}/100")
    print(f"  Boss Alert Level: {state.boss}/5")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_tools())