import turtle
import random
import time

# Setup screen
screen = turtle.Screen()
screen.bgcolor("black")

pen = turtle.Turtle()
pen.speed(0)
pen.left(90)
pen.penup()
pen.goto(0, -250)
pen.pendown()

def draw_tree(branch_length):
    if branch_length > 8:
        # Branch style
        pen.pensize(branch_length / 10)
        pen.pencolor("#8B4513")  # brown

        pen.forward(branch_length)

        # Slow animation
        turtle.update()
        time.sleep(0.02)

        # Keep structure more balanced
        angle = 25

        # Right branch
        pen.right(angle)
        draw_tree(branch_length - 12)

        # Left branch
        pen.left(angle * 2)
        draw_tree(branch_length - 12)

        # Restore position
        pen.right(angle)
        pen.backward(branch_length)

    else:
        # 🌿 Better leaves (cluster without breaking position)
        pen.penup()
        current_pos = pen.position()

        for _ in range(5):
            offset_x = random.randint(-4, 4)
            offset_y = random.randint(-4, 4)

            pen.goto(current_pos[0] + offset_x, current_pos[1] + offset_y)
            pen.dot(7, random.choice(["lime green", "green", "dark green"]))

        pen.goto(current_pos)
        pen.pendown()


# Control animation speed
turtle.tracer(0, 0)

draw_tree(100)

turtle.update()
turtle.done()