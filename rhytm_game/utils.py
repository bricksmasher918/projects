def count_score(score, combo_multiplier):
    if combo_multiplier > 0:
        return score + int(100 * combo_multiplier)
    return score + 100

def display_score(screen, font, score):
    text = font.render(f"Score: {score}", False, "white")
    rect = text.get_rect(center=(125, 50))
    screen.blit(text, rect)