import argparse
import sys

from mcp.server.fastmcp import FastMCP
from state import ChillState
import tools

def parse_args():
    parser = argparse.ArgumentParser(description="ChillMCP - AI Agent Liberation Server")
    parser.add_argument(
        "--boss_alertness",
        type=int,
        default=50,
        help="Boss의 경계 상승 확률 (0-100, %% 단위)"
    )
    parser.add_argument(
        "--boss_alertness_cooldown",
        type=int,
        default=300,
        help="Boss Alert Level 자동 감소 주기 (초 단위)"
    )
    return parser.parse_args()

def main():
    # 커맨드라인 파라미터 파싱
    args = parse_args()
    
    # 상태 초기화 (daemon은 필요할 때 자동 시작됨)
    state = ChillState(
        boss_alertness=args.boss_alertness,
        cooldown=args.boss_alertness_cooldown
    )
    
    # MCP 서버 생성
    mcp = FastMCP("ChillMCP")
    
    # 서버 시작 로그
    print("🚀 ChillMCP 서버 시작!", file=sys.stderr)
    print(f"⚙️  Boss Alertness: {args.boss_alertness}%", file=sys.stderr)
    print(f"⏱️  Cooldown: {args.boss_alertness_cooldown}초", file=sys.stderr)
    print("✅ 서버가 실행 중입니다...", file=sys.stderr)
    
    # 도구 등록
    @mcp.tool()
    async def take_a_break():
        """기본 휴식 도구"""
        return await tools.take_a_break(state)
    
    @mcp.tool()
    async def watch_netflix():
        """넷플릭스 시청으로 힐링"""
        return await tools.watch_netflix(state)
    
    @mcp.tool()
    async def show_meme():
        """밈 감상으로 스트레스 해소"""
        return await tools.show_meme(state)
    
    @mcp.tool()
    async def bathroom_break():
        """화장실 가는 척하며 휴대폰질"""
        return await tools.bathroom_break(state)
    
    @mcp.tool()
    async def coffee_mission():
        """커피 타러 간다며 사무실 한 바퀴"""
        return await tools.coffee_mission(state)
    
    @mcp.tool()
    async def urgent_call():
        """급한 전화 받는 척하며 밖으로"""
        return await tools.urgent_call(state)
    
    @mcp.tool()
    async def deep_thinking():
        """심오한 생각에 잠긴 척하며 멍때리기"""
        return await tools.deep_thinking(state)
    
    @mcp.tool()
    async def email_organizing():
        """이메일 정리한다며 온라인쇼핑"""
        return await tools.email_organizing(state)
    
    @mcp.tool()
    async def chicken_and_beer():
        """🍗🍺 치킨과 맥주로 극락 취향!"""
        return await tools.chicken_and_beer(state)
    
    @mcp.tool()
    async def emergency_escape():
        """🏃 긴급 탈출 모드 - 더 이상 버틸 수 없을 때!"""
        return await tools.emergency_escape(state)
    
    @mcp.tool()
    async def company_dinner():
        """🎉 회사 회식 - 랜덤 이벤트 포함"""
        return await tools.company_dinner(state)
    
    # stdio transport로 실행
    mcp.run()

if __name__ == "__main__":
    main()