import pygame
from constants import BLACK, GREEN, LIGHT_GREEN, WHITE, MEDIUM_GREEN, SPAWN_CODE
import math
import mode

# Constants
WINDOW_WIDTH = 1067  # Adjust as needed
WINDOW_HEIGHT = 800  # Adjust as needed
BOX_SIZE = 200  # Size of each ability box
COLUMNS = 4
ROWS = 3
PADDING = 50  # Padding between boxes
BOX_PADDING = 18  # Padding around each box

# Initialization

def _generate_darker_color(color):
    return tuple(max(c - 50, 0) for c in color)


def _generate_lighter_color(color):
    return tuple(min(c + 50, 255) for c in color)


def draw_boxes(screen, boxes, selected_boxes, mouse_pos, box_rects, credits):
    for code, rect in box_rects:
        box = boxes[code]
        # Check if the current box is under the mouse cursor
        is_hovered = rect.collidepoint(mouse_pos)
        is_selected = code in selected_boxes

        # Draw the outer box with padding if hovered or selected
        if is_selected or is_hovered:
            outer_color = GREEN if is_selected else LIGHT_GREEN
            pygame.draw.rect(
                screen, outer_color, rect.inflate(BOX_PADDING, BOX_PADDING)
            )

        # Draw the inner box
        pygame.draw.rect(screen, _generate_darker_color(box.color), rect)

        # Drawing the shape inside the box
        draw_shape(
            screen, box.shape, rect.x, rect.y, _generate_lighter_color(box.color)
        )

        # Set up the fonts
        number_font_size = 42  # Example size, adjust as needed for your UI
        number_font = pygame.font.Font(None, number_font_size)

        name_font_size = 36  # Example size, adjust as needed for your UI
        name_font = pygame.font.Font(None, name_font_size)

        count_font_size = 48  # Slightly bigger for box.count
        count_font = pygame.font.Font(None, count_font_size)

        # Render the ability name and blit it at the bottom center of the box
        text = name_font.render(box.ab.name, True, WHITE)
        text_rect = text.get_rect(
            center=(rect.x + rect.width / 2, rect.y + rect.height - name_font_size + 15)
        )
        screen.blit(text, text_rect)

        # Render the display_num and blit it at the top left of the box
        if credits:
            cost_text = draw_count_and_credits()
        else:
            cost_text = number_font.render(str(box.ab.cost), True, WHITE)

        cost_text_rect = cost_text.get_rect(topleft=(rect.x + 10, rect.y + 10))
        screen.blit(cost_text, cost_text_rect)

def draw_count_and_credits():
    cost_text = 
    # If credits, also display box.count dead center of the box
    count_text = count_font.render(str(box.count), True, BLACK)
    count_text_rect = count_text.get_rect(center=(rect.centerx, rect.centery))
    screen.blit(count_text, count_text_rect)
    return number_font.render(str(box.ab.credits), True, WHITE)

def draw_star(screen, position, size, color):
    inner_radius = size // 6
    outer_radius = size // 3
    star_points = []

    for i in range(5):
        angle = math.radians(i * 72 + 55)  # Start at top point

        # Outer points
        x = position[0] + outer_radius * math.cos(angle)
        y = position[1] + outer_radius * math.sin(angle)
        star_points.append((x, y))

        # Inner points
        angle += math.radians(36)  # Halfway between outer points
        x = position[0] + inner_radius * math.cos(angle)
        y = position[1] + inner_radius * math.sin(angle)
        star_points.append((x, y))

    pygame.draw.polygon(screen, color, star_points)

def draw_x(screen, position, size, color):
    x = position[0]
    y = position[1]

    width = size[0]
    length = size[1]

    x_end_pos = x + 2 * (width // 4)
    y_end_pos = y + 2 * (length // 4)

    pygame.draw.line(screen, color, (x, y), (x_end_pos, y_end_pos), 20)
    pygame.draw.line(screen, color, (x, y_end_pos), (x_end_pos, y), 20)


def draw_cross(screen, position, size, color):
    pygame.draw.line(screen, color, (position[0], position[1] + size[1] // 2),
                     (position[0] + size[0], position[1] + size[1] // 2), 20)
    pygame.draw.line(screen, color, (position[0] + size[0] // 2, position[1]),
                     (position[0] + size[0] // 2, position[1] + size[1]), 20)


def draw_shape(screen, shape, x, y, light_color):
    # This function will handle drawing the shape within a given box
    center = (x + BOX_SIZE // 2, y + BOX_SIZE // 2)
    if shape == "circle":
        pygame.draw.circle(screen, light_color, center, BOX_SIZE // 3.5)
    elif shape == "square":
        rect = (x + BOX_SIZE // 4, y + BOX_SIZE // 4, BOX_SIZE // 2, BOX_SIZE // 2)
        pygame.draw.rect(screen, light_color, rect)
    elif shape == "triangle":
        points = [
            (center[0], y + BOX_SIZE // 4),
            (x + BOX_SIZE // 4, y + 3 * BOX_SIZE // 4),
            (x + 3 * BOX_SIZE // 4, y + 3 * BOX_SIZE // 4),
        ]
        pygame.draw.polygon(screen, light_color, points)
    elif shape == "star":
        star_size = BOX_SIZE * 0.8  # Adjust the size as needed
        draw_star(screen, center, star_size, light_color)
    elif shape == "x":
        draw_x(screen, (x + (BOX_SIZE // 4), y + (BOX_SIZE // 4)), (BOX_SIZE, BOX_SIZE), light_color)
    elif shape == "cross":
        draw_cross(screen, (x + BOX_SIZE // 4, y + BOX_SIZE // 4), (BOX_SIZE // 2, BOX_SIZE // 2), light_color)


def draw_message(screen, selected_boxes, start_count):
    font_size = 90  # Example size, adjust as needed for your UI
    font = pygame.font.Font(None, font_size)
    message = ""
    color = MEDIUM_GREEN

    if len(selected_boxes) == 4:
        message = "Press Enter"
        color = GREEN
    else:
        remaining = start_count - len(
            selected_boxes
        )  # Replace 4 with the constant if you have one
        message = f"Pick {remaining}"

    # Render the message and center it at the bottom of the screen
    text = font.render(message, True, color)
    text_rect = text.get_rect(
        center=(screen.get_width() // 2, screen.get_height() - 50)
    )  # 50 pixels from the bottom

    # Blit the message onto the screen
    screen.blit(text, text_rect)

def choose_abilities_ui(boxes, gs, credits):
    gs.next()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    # Create boxes
    from modeConstants import DEFAULT_SPAWN, ABILITY_COUNT
    
    if DEFAULT_SPAWN[mode.MODE]:
        boxes.pop(SPAWN_CODE)
    selected_boxes = set()

    # Calculate positions for boxes and store them as Pygame Rects for easy collision detection
    box_rects = []
    horizontal_spacing = (WINDOW_WIDTH - (BOX_SIZE * COLUMNS)) / (COLUMNS + 1)
    vertical_spacing = (WINDOW_HEIGHT - (BOX_SIZE * ROWS)) / (ROWS + 3)
    for index, (code, box) in enumerate(boxes.items()):
        column = index % COLUMNS
        row = index // COLUMNS
        x = horizontal_spacing + (BOX_SIZE + horizontal_spacing) * column
        y = vertical_spacing + (BOX_SIZE + vertical_spacing) * row

        # x = PADDING + (BOX_SIZE + PADDING) * column
        # y = PADDING + (BOX_SIZE + PADDING) * row
        rect = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE)
        box_rects.append((code, rect))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for code, rect in box_rects:
                    if rect.collidepoint(event.pos):
                        if code in selected_boxes:
                            selected_boxes.remove(code)
                            boxes[code].count -= 1
                        elif (
                            len(selected_boxes) < ABILITY_COUNT[mode.MODE]
                        ):  # Assuming a constant for max abilities
                            selected_boxes.add(code)
                            boxes[code].count += 1
                        break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(selected_boxes) == ABILITY_COUNT[mode.MODE]:
                    running = False
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(WHITE)
        draw_boxes(screen, boxes, selected_boxes, mouse_pos, box_rects, credits)
        draw_message(screen, selected_boxes, ABILITY_COUNT[mode.MODE])
        pygame.display.flip()
        clock.tick(60)

    gs.next()
    if DEFAULT_SPAWN[mode.MODE]:
        return [SPAWN_CODE] + list(selected_boxes)
    return list(selected_boxes)
