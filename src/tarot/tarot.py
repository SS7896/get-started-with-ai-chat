"""Simple tarot deck implementation for MVP.

Provides:
- build_deck(): returns the list of 78 card names
- draw(count): returns a list of selected cards with a Chinese meaning
- get_meaning(card): returns the Chinese meaning for a card

Meanings are basic and concise (MVP). They can be expanded later or replaced with a data file.
"""
from typing import List, Dict
import random


MAJOR_ARCANA = [
    "The Fool",
    "The Magician",
    "The High Priestess",
    "The Empress",
    "The Emperor",
    "The Hierophant",
    "The Lovers",
    "The Chariot",
    "Strength",
    "The Hermit",
    "Wheel of Fortune",
    "Justice",
    "The Hanged Man",
    "Death",
    "Temperance",
    "The Devil",
    "The Tower",
    "The Star",
    "The Moon",
    "The Sun",
    "Judgement",
    "The World",
]

RANKS = [
    "Ace",
    "Two",
    "Three",
    "Four",
    "Five",
    "Six",
    "Seven",
    "Eight",
    "Nine",
    "Ten",
    "Page",
    "Knight",
    "Queen",
    "King",
]

SUITS = ["Wands", "Cups", "Swords", "Pentacles"]


def build_deck() -> List[str]:
    """Build and return a standard 78-card tarot deck (names only)."""
    deck = []
    deck.extend(MAJOR_ARCANA)
    for suit in SUITS:
        for rank in RANKS:
            deck.append(f"{rank} of {suit}")
    return deck


_DECK = build_deck()


_MEANINGS_CN = {
    # Major Arcana
    "The Fool": "愚者：新的开始、无畏、天真与潜力，鼓励冒险与信任旅程。",
    "The Magician": "魔术师：专注与意志，资源整合、创造力付诸行动。",
    "The High Priestess": "女祭司：直觉、潜意识与神秘，提醒聆听内在声音。",
    "The Empress": "女皇：滋养、丰饶与创造力，代表孕育与舒适。",
    "The Emperor": "皇帝：秩序、结构与权威，强调稳定与领导。",
    "The Hierophant": "教皇：传统、信仰与教育，代表制度与指导。",
    "The Lovers": "恋人：关系与选择，爱情、价值观与和谐。",
    "The Chariot": "战车：意志、决心与胜利，通过控制与专注前行。",
    "Strength": "力量：勇气、耐心与内在温柔，驯服本能而非强压。",
    "The Hermit": "隐士：内省、寻求真理与独处，强调自我探索。",
    "Wheel of Fortune": "命运之轮：周期与变化，机遇与不可控的命运。",
    "Justice": "正义：公平、因果与责任，强调平衡与后果。",
    "The Hanged Man": "倒吊人：暂停、视角转换与牺牲，悟出不同的理解。",
    "Death": "死亡：结束与转化，旧事物结束以迎接新生。",
    "Temperance": "节制：平衡、整合与适度，通过协调达成和谐。",
    "The Devil": "魔鬼：束缚、欲望与物质诱惑，提醒面对影子面。",
    "The Tower": "塔：突变、瓦解与觉醒，破坏旧有结构以重建。",
    "The Star": "星星：希望、疗愈与灵感，指向内心的安慰与复兴。",
    "The Moon": "月亮：不确定与潜意识，提示直觉与隐藏信息。",
    "The Sun": "太阳：成功、活力与清晰，带来喜悦与成长。",
    "Judgement": "审判：觉醒、评估与转变，对过去的回顾与重生。",
    "The World": "世界：完成、成就与圆满，整合并进入新阶段。",

    # Minor Arcana - Wands (权杖) — 行动、创造、激情
    "Ace of Wands": "权杖 A：灵感与新行动、创造力的起点。",
    "Two of Wands": "权杖 2：规划与展望，开始为未来做决定。",
    "Three of Wands": "权杖 3：事业拓展、等待成果与远见。",
    "Four of Wands": "权杖 4：庆祝、稳定的基础与社群支持。",
    "Five of Wands": "权杖 5：冲突与竞争，短期的摩擦或挑战。",
    "Six of Wands": "权杖 6：胜利、认可与公众的成功。",
    "Seven of Wands": "权杖 7：防守立场、坚持自己的位置。",
    "Eight of Wands": "权杖 8：快速进展、消息或行动迅速到来。",
    "Nine of Wands": "权杖 9：疲惫但坚持，接近目标需防护与韧性。",
    "Ten of Wands": "权杖 10：负担过重、责任沉重，需学会释放。",
    "Page of Wands": "权杖侍从：好奇与创意的讯息，尝试与探索新想法。",
    "Knight of Wands": "权杖骑士：冲动与热情，行动力强但须谨慎。",
    "Queen of Wands": "权杖皇后：充满魅力、热情与领导力的女性能量。",
    "King of Wands": "权杖国王：愿景与果敢的领导者，激励他人付诸行动。",

    # Cups (圣杯) — 情感、关系、内心
    "Ace of Cups": "圣杯 A：情感的开始、爱与直觉的涌现。",
    "Two of Cups": "圣杯 2：二人连接、伙伴关系与互相吸引。",
    "Three of Cups": "圣杯 3：友情、庆祝与支持网络。",
    "Four of Cups": "圣杯 4：情感上的冷漠或沉思，机会被忽略。",
    "Five of Cups": "圣杯 5：失落與悲傷，專注於損失而忽略剩餘。",
    "Six of Cups": "圣杯 6：回忆、怀旧与童年的善意。",
    "Seven of Cups": "圣杯 7：幻想与选择，需辨别幻象与现实。",
    "Eight of Cups": "圣杯 8：离开不再满足的情境，寻求更深的意义。",
    "Nine of Cups": "圣杯 9：愿望成真与满足的情感状态。",
    "Ten of Cups": "圣杯 10：家庭幸福、情感圆满与和谐。",
    "Page of Cups": "圣杯侍从：情感讯息、创意灵感与温柔的邀请。",
    "Knight of Cups": "圣杯骑士：浪漫与追求感情的旅人，理想主义。",
    "Queen of Cups": "圣杯皇后：富有同理心、直觉敏锐与情感成熟。",
    "King of Cups": "圣杯国王：情感成熟、平和且能给予支持的领导者。",

    # Swords (宝剑) — 思维、沟通、冲突
    "Ace of Swords": "宝剑 A：真理的闪现、清晰的想法与决定。",
    "Two of Swords": "宝剑 2：犹豫不决、需要平衡信息与情绪。",
    "Three of Swords": "宝剑 3：心痛、分离与情感上的伤害。",
    "Four of Swords": "宝剑 4：休息、恢复与暂时撤退以疗愈。",
    "Five of Swords": "宝剑 5：争执与争胜，可能带来道德代价。",
    "Six of Swords": "宝剑 6：离开困境、过渡与平静的旅程。",
    "Seven of Swords": "宝剑 7：机智、策略或不完全诚实的行为。",
    "Eight of Swords": "宝剑 8：受限于思维与恐惧，需要改变观念。",
    "Nine of Swords": "宝剑 9：焦虑、失眠与心中的担忧。",
    "Ten of Swords": "宝剑 10：痛苦的终结，虽剧烈但标志着结束。",
    "Page of Swords": "宝剑侍从：好奇心强的消息与求知欲。",
    "Knight of Swords": "宝剑骑士：迅速行动与直接，有时过于冲动。",
    "Queen of Swords": "宝剑皇后：理性、客观与清晰的沟通能力。",
    "King of Swords": "宝剑国王：权威与智慧，法则与策略的代表。",

    # Pentacles (钱币) — 物质、工作、财富
    "Ace of Pentacles": "钱币 A：物质与事业的新机遇、务实的开始。",
    "Two of Pentacles": "钱币 2：平衡资源与多任务处理的需要。",
    "Three of Pentacles": "钱币 3：合作、技能发展与工匠精神。",
    "Four of Pentacles": "钱币 4：守护资源、吝啬或稳固的财务态度。",
    "Five of Pentacles": "钱币 5：物质匮乏或被排斥的感觉，需要寻求帮助。",
    "Six of Pentacles": "钱币 6：给予与接受的平衡，慈善与回报。",
    "Seven of Pentacles": "钱币 7：耐心等待投资结果与评估进展。",
    "Eight of Pentacles": "钱币 8：勤奋与专注于技能的精进。",
    "Nine of Pentacles": "钱币 9：独立与物质享受，通过努力获得的稳定。",
    "Ten of Pentacles": "钱币 10：家族财富、长期稳定与世代传承。",
    "Page of Pentacles": "钱币侍从：学习与实际的机会，务实的种子。",
    "Knight of Pentacles": "钱币骑士：可靠、踏实与持续的努力。",
    "Queen of Pentacles": "钱币皇后：务实、照顾家庭与物质上的富足。",
    "King of Pentacles": "钱币国王：成功的企业家或稳健的财务管理者。",
}


def get_meaning(card_name: str) -> str:
    """Return a concise Chinese meaning for a card.

    We first lookup the explicit mapping for all 78 cards. If missing, fall back to a
    simple generated message.
    """
    if card_name in _MEANINGS_CN:
        return _MEANINGS_CN[card_name]

    # Fallback: keep a short generated description (should not occur once mapping filled)
    parts = card_name.split(" of ")
    if len(parts) == 2:
        rank, suit = parts
        suit_cn = {
            "Wands": "权杖",
            "Cups": "圣杯",
            "Swords": "宝剑",
            "Pentacles": "钱币",
        }.get(suit, suit)
        return f"{suit_cn} {rank}：此牌的简短释义（待完善）。"

    return "这张牌的释义暂不可用。"


def draw(count: int = 1) -> List[Dict[str, str]]:
    """Shuffle and draw `count` unique cards from the deck.

    Returns a list of dicts: {"card": str, "meaning": str}
    """
    if count < 1:
        raise ValueError("count must be >= 1")
    if count > len(_DECK):
        raise ValueError(f"count must be <= {len(_DECK)}")

    deck_copy = _DECK.copy()
    random.shuffle(deck_copy)
    picked = deck_copy[:count]
    result = []
    for card in picked:
        result.append({"card": card, "meaning": get_meaning(card)})
    return result


def draw_spread(spread: str = "single", count: int = 1) -> List[Dict[str, str]]:
    """Draw cards according to a spread type.

    Supported spreads:
    - single: returns list of cards (same as draw(count))
    - three: returns Past/Present/Future (3 cards)
    - cross: Celtic Cross (10 cards)

    Returns list of dicts: {"position": str, "card": str, "meaning": str}
    """
    spread = (spread or "").lower()
    if spread == "single":
        return [{"position": "", **c} for c in draw(count)]

    if spread == "three":
        positions = ["Past", "Present", "Future"]
        cards = draw(3)
        return [
            {"position": positions[i], "card": cards[i]["card"], "meaning": cards[i]["meaning"]}
            for i in range(3)
        ]

    if spread == "cross":
        # Celtic Cross - 10 cards with common positional names
        positions = [
            "Significator (1)",
            "Crossing / Challenge (2)",
            "Above / Conscious (3)",
            "Below / Subconscious (4)",
            "Past (5)",
            "Future (6)",
            "Self / Attitude (7)",
            "Environment (8)",
            "Hopes & Fears (9)",
            "Outcome (10)",
        ]
        cards = draw(10)
        return [
            {"position": positions[i], "card": cards[i]["card"], "meaning": cards[i]["meaning"]}
            for i in range(10)
        ]

    raise ValueError("Unsupported spread. Use 'single', 'three' or 'cross'.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Draw tarot cards (MVP CLI)")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of cards to draw")
    args = parser.parse_args()
    for c in draw(args.count):
        print(f"{c['card']}\n  {c['meaning']}\n")
