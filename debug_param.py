#!/usr/bin/env python3
"""
파라미터 인식 디버깅
"""

import subprocess
import sys
import time

print("=" * 80)
print("🔍 파라미터 인식 디버깅")
print("=" * 80)

test_cases = [
    {"alertness": 50, "cooldown": 300, "name": "기본값"},
    {"alertness": 100, "cooldown": 10, "name": "최대 경계"},
]

for test in test_cases:
    print(f"\n\n📌 테스트: {test['name']}")
    print(f"   파라미터: --boss_alertness {test['alertness']} --boss_alertness_cooldown {test['cooldown']}")
    print("-" * 80)
    
    cmd = [
        sys.executable, "main.py",
        "--boss_alertness", str(test['alertness']),
        "--boss_alertness_cooldown", str(test['cooldown'])
    ]
    
    print(f"실행 명령: {' '.join(cmd)}\n")
    
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    time.sleep(2)
    
    try:
        process.terminate()
        stdout, stderr = process.communicate(timeout=5)
        
        print("📤 stdout:")
        print(stdout if stdout else "  (없음)")
        
        print("\n📥 stderr:")
        print(stderr if stderr else "  (없음)")
        
        print("\n🔎 분석:")
        if "Boss Alertness:" in stderr:
            print("   ✅ 'Boss Alertness:' 발견")
            if f"{test['alertness']}%" in stderr:
                print(f"   ✅ '{test['alertness']}%' 발견")
            else:
                print(f"   ❌ '{test['alertness']}%' 미발견")
                print(f"   실제 내용: {stderr}")
        else:
            print("   ❌ 'Boss Alertness:' 미발견")
            print(f"   stderr 내용: {repr(stderr)}")
            
    except Exception as e:
        print(f"❌ 오류: {e}")
        stdout, stderr = process.communicate()
        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")

print("\n" + "=" * 80)