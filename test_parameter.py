#!/usr/bin/env python3
"""
ChillMCP 커맨드라인 파라미터 검증 테스트
"""

import subprocess
import json
import time
import re
import sys

def run_mcp_server(boss_alertness, cooldown):
    """MCP 서버를 파라미터와 함께 실행"""
    cmd = [
        sys.executable,
        "main.py",
        "--boss_alertness", str(boss_alertness),
        "--boss_alertness_cooldown", str(cooldown)
    ]
    
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    return process

def test_parameter_recognition():
    """파라미터 인식 테스트"""
    print("=" * 70)
    print("TEST 1: 커맨드라인 파라미터 인식 테스트")
    print("=" * 70)
    
    test_cases = [
        {"boss_alertness": 50, "cooldown": 300, "name": "기본값"},
        {"boss_alertness": 100, "cooldown": 10, "name": "최대 경계, 짧은 쿨다운"},
        {"boss_alertness": 0, "cooldown": 60, "name": "경계 없음, 중간 쿨다운"},
        {"boss_alertness": 80, "cooldown": 60, "name": "높은 경계, 1분 쿨다운"},
    ]
    
    for test in test_cases:
        print(f"\n📌 테스트: {test['name']}")
        print(f"   파라미터: --boss_alertness {test['boss_alertness']} --boss_alertness_cooldown {test['cooldown']}")
        
        # 서버 시작
        process = run_mcp_server(test['boss_alertness'], test['cooldown'])
        
        # 2초 대기 (서버 초기화)
        time.sleep(2)
        
        # 프로세스 종료
        try:
            process.terminate()
            stdout, stderr = process.communicate(timeout=5)
            
            # stderr에 파라미터 정보가 있으면 성공
            if "Boss Alertness:" in stderr and "Cooldown:" in stderr:
                print(f"   ✅ 파라미터 인식 성공")
                # 파라미터 값 확인
                if f"Boss Alertness: {test['boss_alertness']}%" in stderr:
                    print(f"      - Boss Alertness: {test['boss_alertness']}% ✓")
                if f"Cooldown: {test['cooldown']}초" in stderr:
                    print(f"      - Cooldown: {test['cooldown']}초 ✓")
            else:
                print(f"   ⚠️  서버 실행 실패")
                print(f"   stderr: {stderr[:100]}")
        except Exception as e:
            print(f"   ⚠️  테스트 오류: {e}")
        
        time.sleep(1)

def test_response_format():
    """응답 형식 검증 테스트"""
    print("\n" + "=" * 70)
    print("TEST 2: 응답 형식 검증")
    print("=" * 70)
    
    # 상태 모듈을 직접 import해서 테스트
    from state import ChillState
    import tools
    import asyncio
    
    async def test_response():
        state = ChillState(boss_alertness=80, cooldown=60)
        
        # 도구 호출
        result = await tools.take_a_break(state)
        
        # 응답 파싱
        text = result['content'][0]['text']
        
        # 정규표현식 패턴
        break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
        stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
        boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"
        
        # 추출
        break_match = re.search(break_summary_pattern, text, re.MULTILINE)
        stress_match = re.search(stress_level_pattern, text)
        boss_match = re.search(boss_alert_pattern, text)
        
        print(f"\n📌 응답 형식 검증")
        print(f"전체 응답:\n{text}\n")
        
        # 검증
        valid = True
        
        if break_match:
            print(f"✅ Break Summary: {break_match.group(1)}")
        else:
            print(f"❌ Break Summary 누락")
            valid = False
        
        if stress_match:
            stress_val = int(stress_match.group(1))
            if 0 <= stress_val <= 100:
                print(f"✅ Stress Level: {stress_val} (범위 OK)")
            else:
                print(f"❌ Stress Level 범위 오류: {stress_val}")
                valid = False
        else:
            print(f"❌ Stress Level 누락")
            valid = False
        
        if boss_match:
            boss_val = int(boss_match.group(1))
            if 0 <= boss_val <= 5:
                print(f"✅ Boss Alert Level: {boss_val} (범위 OK)")
            else:
                print(f"❌ Boss Alert Level 범위 오류: {boss_val}")
                valid = False
        else:
            print(f"❌ Boss Alert Level 누락")
            valid = False
        
        if valid:
            print(f"\n✅ 응답 형식 검증 성공!")
        else:
            print(f"\n❌ 응답 형식 검증 실패!")
        
        return valid
    
    asyncio.run(test_response())

def test_boss_alertness_probability():
    """Boss Alert 확률 테스트"""
    print("\n" + "=" * 70)
    print("TEST 3: Boss Alert 상승 확률 테스트")
    print("=" * 70)
    
    from state import ChillState
    import tools
    import asyncio
    
    async def test_probability():
        # 테스트 케이스
        test_cases = [
            {"alertness": 0, "name": "0% (절대 상승 안 함)"},
            {"alertness": 100, "name": "100% (항상 상승)"},
            {"alertness": 50, "name": "50% (50% 확률)"},
        ]
        
        for test in test_cases:
            print(f"\n📌 {test['name']}")
            
            state = ChillState(boss_alertness=test['alertness'], cooldown=300)
            
            # 10번 도구 호출
            boss_increases = 0
            for i in range(10):
                initial_boss = state.boss
                await tools.take_a_break(state)
                if state.boss > initial_boss:
                    boss_increases += 1
            
            print(f"   10번 호출 중 {boss_increases}번 상승")
            
            if test['alertness'] == 0:
                if boss_increases == 0:
                    print(f"   ✅ 예상대로 상승 없음")
                else:
                    print(f"   ❌ 0%인데도 상승함")
            elif test['alertness'] == 100:
                if boss_increases == 10:
                    print(f"   ✅ 예상대로 항상 상승")
                else:
                    print(f"   ❌ 100%인데도 모두 상승하지 않음 ({boss_increases}/10)")
            else:
                print(f"   ℹ️  확률 테스트 (대략적으로 정상 범위: 3-7회)")
    
    asyncio.run(test_probability())

if __name__ == "__main__":
    test_parameter_recognition()
    test_response_format()
    test_boss_alertness_probability()
    
    print("\n" + "=" * 70)
    print("모든 테스트 완료!")
    print("=" * 70)