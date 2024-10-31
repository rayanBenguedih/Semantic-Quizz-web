fake_artists: [str] = [
        "TheWeekend", "Arianna Grande", "50 cent", "KIK", "Queen",
        "Vianney", "One Direction", "The Rolling Stones", "The Beatles", "The Who",
        "The Clash", "The Cure", "The Police", "The Smiths", "The Strokes",
        "The Velvet Underground", "The White Stripes", "The XX", "The Zombies", "The 1975",
    ]

fake_questions = []

for i in range(1, 21):
    data = {
        "question": f"Question {i}: What is the capital of country X?",
        "validAnswer": f"Capital {i}",
        "wrongAnswers": [f"Wrong Answer {i}-1", f"Wrong Answer {i}-2", f"Wrong Answer {i}-3"]
    }
    fake_questions.append(data)
