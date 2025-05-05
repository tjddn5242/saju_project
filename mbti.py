from openai import OpenAI
import json

def get_personality_analysis(ilju, mbti):
    client = OpenAI()

    system_prompt = "당신은 사주와 MBTI를 통해 사람의 성격을 분석하는 전문가입니다."
    user_prompt = f"사주는 {ilju}일주이고, MBTI는 {mbti}입니다. 이 사람의 성격을 분석하여 형태에 맞게 출력하세요."

    tools = [{
        "type": "function",
        "name": "get_analysis",
        "description": "사주와 MBTI를 통해 사람의 성격을 분석합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "외향성": {
                    "type": "number",
                    "description": "외향성 점수를 1~5 사이의 정수로 평가합니다."
                },
                "안정성": {
                    "type": "number", 
                    "description": "안정성 점수를 1~5 사이의 정수로 평가합니다."
                },
                "개방성": {
                    "type": "number",
                    "description": "개방성 점수를 1~5 사이의 정수로 평가합니다."
                },
                "책임감": {
                    "type": "number",
                    "description": "책임감 점수를 1~5 사이의 정수로 평가합니다."
                },
                "친화성": {
                    "type": "number",
                    "description": "친화성 점수를 1~5 사이의 정수로 평가합니다."
                },
                "자기주도성": {
                    "type": "number",
                    "description": "자기주도성 점수를 1~5 사이의 정수로 평가합니다."
                },
                "이성적": {
                    "type": "number",
                    "description": "이성적 점수를 1~5 사이의 정수로 평가합니다."
                },
                "도전성": {
                    "type": "number",
                    "description": "도전성 점수를 1~5 사이의 정수로 평가합니다."
                },
                "MBIT기반 직업": {
                    "type": "string",
                    "description": "MBIT기반 직업을 세 가지 추천합니다. 예시: 브랜드 마케터, 조직문화 코치, 교육 기획자"
                },
                "사주기반 직업": {
                    "type": "string",
                    "description": "사주기반 직업을 세 가지 추천합니다. 예시: 스토리 기반 콘텐츠 기획자, 식물·자연·감성 기반 디자인 전문가, 문화·예술 분야의 중재자"
                },
                "최종 직업": {
                    "type": "string",
                    "description": "MBIT기반 직업과 사주기반 직업을 참고하여 최종 직업을 한 문장으로 나타냅니다. 예시: 사람의 감정을 기획으로 연결하는 공감형 BX 디자이너"
                },
                "성격 키워드": {
                    "type": "string",
                    "description": "MBIT와 사주를 기반으로 성격 키워드를 세 가지 태그로 나타냅니다. 예시: #섬세한 #사람을이끄는 #공감형"
                }
            },
            "required": [
                "외향성", "안정성", "개방성", "책임감", "친화성", "자기주도성", "이성적", "도전성",
                "MBIT기반 직업", "사주기반 직업", "최종 직업", "성격 키워드"
            ],
            "additionalProperties": False
        }
    }]

    response = client.responses.create(
        model="gpt-4.1",
        input=[{"role": "system", "content": system_prompt},
               {"role": "user", "content": user_prompt}],
        tools=tools
    )

    return json.loads(response.output[0].arguments)