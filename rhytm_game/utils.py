def count_score(score, combo_multiplier):
    if combo_multiplier > 0:
        return score + int(100 * combo_multiplier)
    return score + 100

def display_score(screen, font, score):
    text = font.render(f"Score: {score}", False, "white")
    rect = text.get_rect(center=(800, 50))
    screen.blit(text, rect)

def accuracy_color(accuracy):

    if accuracy == 100:
        color = (255, 255, 255)
    elif accuracy > 90.0:
        color = (255, 245, 90)
    elif accuracy > 70.0:
        color = (90, 255, 94)
    elif accuracy > 50.0:
        color = (90, 156, 255)
    else:
        color = (255, 191, 90)

    return color


def display_accuracy(screen, font, accuracy):

    color = accuracy_color(accuracy)

    text = font.render(f"Accuracy: {accuracy:.1f}%", False, color)
    rect = text.get_rect(center=(800, 100))
    screen.blit(text, rect)

def get_hitobjects(osu_file_path):
    with open(osu_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    in_hitobjects = False
    hitobjects = []

    for line in lines:
        if line.strip() == '[HitObjects]':
            in_hitobjects = True
            continue
        if in_hitobjects:
            if line.strip() == '' or line.startswith('['):
                break
            parts = line.strip().split(',')
            x = int(parts[0])
            time = int(parts[2]) - 873
            column = x * 4 // 512

            hitobjects.append({'column': column, 'time': time})

    return hitobjects

#C:\Users\dangh\AppData\Local\osu!\Songs