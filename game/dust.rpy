init python:
    dust = SnowBlossom(
        "images/ui/tochka.png",
        count=60,            # количество пыли
        border=80,
        xspeed=(-12, 12),    # лёгкое горизонтальное колыхание
        yspeed=(-25, -10),   # ВВЕРХ (отрицательные значения)
        start=0.0,
        fast=False
    )
