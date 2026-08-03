#!/usr/bin/env python3
"""Generate the original procedural sound pack used by Purple Shift 1.4.

The script intentionally uses only the Python standard library and ffmpeg.
Every render is deterministic, so the committed OGG files can be reproduced.
"""

from __future__ import annotations

import math
import random
import shutil
import struct
import subprocess
import tempfile
import wave
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "game" / "audio" / "live"
RATE = 22_050
TAU = math.tau


def clamp(value: float) -> float:
    return max(-1.0, min(1.0, value))


def smooth_noise(seed: int, response: float = 0.035):
    rng = random.Random(seed)
    state = 0.0

    def sample() -> float:
        nonlocal state
        state += (rng.uniform(-1.0, 1.0) - state) * response
        return state

    return sample


def render(name: str, duration: float, sampler, quality: int = 4) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required to render the sound pack")

    frame_count = int(duration * RATE)
    with tempfile.NamedTemporaryFile(suffix=".wav") as temporary:
        with wave.open(temporary.name, "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(RATE)

            chunk = bytearray()
            for index in range(frame_count):
                value = clamp(sampler(index / RATE, index))
                chunk.extend(struct.pack("<h", int(value * 32_000)))

                if len(chunk) >= 131_072:
                    wav.writeframesraw(chunk)
                    chunk.clear()

            if chunk:
                wav.writeframesraw(chunk)

        subprocess.run(
            [
                ffmpeg,
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-i",
                temporary.name,
                "-map_metadata",
                "-1",
                "-fflags",
                "+bitexact",
                "-flags:a",
                "+bitexact",
                "-c:a",
                "libvorbis",
                "-q:a",
                str(quality),
                "-serial_offset",
                "0",
                str(OUTPUT / name),
            ],
            check=True,
        )


def ambience_fluorescent():
    noise = smooth_noise(1401, 0.06)

    def sample(t: float, _: int) -> float:
        hum = (
            math.sin(TAU * 50 * t) * 0.045
            + math.sin(TAU * 100 * t) * 0.018
            + math.sin(TAU * 150 * t) * 0.009
        )
        flicker = 0.65 + 0.35 * math.sin(TAU * 0.17 * t) ** 8
        return hum * flicker + noise() * 0.025

    return sample


def ambience_breakroom():
    noise = smooth_noise(1402, 0.012)

    def sample(t: float, _: int) -> float:
        ventilation = noise() * 0.15
        hum = math.sin(TAU * 60 * t) * 0.018
        fridge = math.sin(TAU * 42 * t) * (0.018 + 0.009 * math.sin(TAU * 0.08 * t))
        return ventilation + hum + fridge

    return sample


def ambience_forklift():
    noise = smooth_noise(1403, 0.025)

    def sample(t: float, _: int) -> float:
        distance = 0.55 + 0.45 * math.sin(TAU * 0.055 * t)
        engine = (
            math.sin(TAU * (39 + 2 * math.sin(TAU * 0.11 * t)) * t) * 0.07
            + math.sin(TAU * 78 * t) * 0.018
        ) * distance
        beep_phase = t % 5.4
        beep = 0.0
        if 3.7 < beep_phase < 3.92 or 4.18 < beep_phase < 4.40:
            edge = min((beep_phase % 0.48) / 0.05, (0.22 - beep_phase % 0.48) / 0.05, 1.0)
            beep = math.sin(TAU * 740 * t) * max(0.0, edge) * 0.035
        return engine + beep + noise() * 0.035

    return sample


def ambience_rain():
    rng = random.Random(1404)
    noise = smooth_noise(1405, 0.28)
    drops: list[tuple[float, float]] = []
    for _ in range(145):
        drops.append((rng.uniform(0.0, 16.0), rng.uniform(0.015, 0.08)))

    def sample(t: float, _: int) -> float:
        value = noise() * 0.22
        for start, strength in drops:
            delta = t - start
            if 0.0 <= delta <= 0.045:
                value += math.sin(TAU * (1250 + strength * 4000) * delta) * (
                    1.0 - delta / 0.045
                ) * strength
        return value

    return sample


def ambience_storm():
    noise = smooth_noise(1410, 0.018)

    def sample(t: float, _: int) -> float:
        drone = (
            math.sin(TAU * 31 * t) * 0.052
            + math.sin(TAU * 46.5 * t) * 0.038
            + math.sin(TAU * 93 * t) * 0.015
        )
        pulse = math.sin(TAU * 0.125 * t) ** 10
        signal = math.sin(TAU * (610 + 35 * math.sin(TAU * 0.2 * t)) * t) * pulse * 0.035
        return drone * (0.55 + 0.45 * math.sin(TAU * 0.07 * t)) + noise() * 0.19 + signal

    return sample


def footsteps():
    noise = smooth_noise(1420, 0.42)
    steps = (0.55, 1.35, 2.15, 3.05, 3.85, 4.75, 5.55)

    def sample(t: float, _: int) -> float:
        value = 0.0
        for start in steps:
            delta = t - start
            if 0.0 <= delta <= 0.22:
                envelope = math.exp(-delta * 20)
                value += (
                    math.sin(TAU * 72 * delta) * 0.36
                    + noise() * 0.22
                ) * envelope
        return value

    return sample


def chirp(notes, duration: float, seed: int, noise_gain: float = 0.0):
    noise = smooth_noise(seed, 0.35)

    def sample(t: float, _: int) -> float:
        value = 0.0
        for start, length, frequency, gain in notes:
            delta = t - start
            if 0.0 <= delta <= length:
                envelope = max(
                    0.0,
                    math.sin(math.pi * delta / length),
                ) ** 1.4
                value += math.sin(TAU * frequency * delta) * gain * envelope
        if noise_gain:
            value += noise() * noise_gain * math.exp(-t * 5)
        return value

    return sample


def paper_rustle():
    noise = smooth_noise(1430, 0.65)

    def sample(t: float, _: int) -> float:
        envelope = (
            math.sin(math.pi * min(1.0, t / 0.34)) ** 2
            if t < 0.34
            else math.exp(-(t - 0.34) * 3.8)
        )
        movement = 0.35 + 0.65 * abs(math.sin(TAU * 7.5 * t))
        return noise() * envelope * movement * 0.46

    return sample


def route_motif(root: float, intervals: tuple[float, ...], seed: int):
    noise = smooth_noise(seed, 0.01)

    def sample(t: float, _: int) -> float:
        fade = min(1.0, t / 1.4, (12.0 - t) / 1.4)
        shimmer = 0.75 + 0.25 * math.sin(TAU * 0.09 * t)
        value = 0.0
        for index, ratio in enumerate(intervals):
            frequency = root * ratio
            value += math.sin(TAU * frequency * t + index * 0.7) * (0.035 / (index + 1))
        return (value * shimmer + noise() * 0.055) * max(0.0, fade)

    return sample


def route_variant_motif(
    root: float,
    intervals: tuple[float, ...],
    seed: int,
    growth: bool,
):
    """Render an evolved route motif without replacing the original identity."""

    noise = smooth_noise(seed, 0.012)
    detune = 1.006 if growth else 0.982

    def sample(t: float, _: int) -> float:
        fade = min(1.0, t / 1.35, (12.0 - t) / 1.35)
        breath = 0.76 + 0.24 * math.sin(TAU * 0.085 * t)
        value = 0.0

        for index, ratio in enumerate(intervals):
            frequency = root * ratio
            gain = 0.037 / (index + 1)
            value += math.sin(TAU * frequency * t + index * 0.64) * gain

        if growth:
            # A soft upper answer resolves at the end of every two-bar phrase.
            answer = max(0.0, math.sin(TAU * 0.125 * t - math.pi / 2)) ** 5
            value += math.sin(TAU * root * 2.0 * t) * answer * 0.026
            value += math.sin(TAU * root * 1.5 * t) * 0.012
        else:
            # The shadow variant keeps the motif recognizable but never quite settled.
            pulse = max(0.0, math.sin(TAU * 0.25 * t)) ** 7
            value += math.sin(TAU * root * 0.5 * detune * t) * pulse * 0.038
            value += math.sin(TAU * root * detune * t) * 0.014

        return (value * breath + noise() * (0.045 if growth else 0.065)) * max(0.0, fade)

    return sample


def main() -> None:
    renders = [
        ("fluorescent_hum.ogg", 16.0, ambience_fluorescent()),
        ("breakroom_hum.ogg", 16.0, ambience_breakroom()),
        ("forklift_distant.ogg", 16.0, ambience_forklift()),
        ("dock_rain.ogg", 16.0, ambience_rain()),
        ("storm_whisper.ogg", 16.0, ambience_storm()),
        ("footsteps_concrete.ogg", 6.0, footsteps()),
        (
            "scanner_confirm.ogg",
            0.55,
            chirp(((0.02, 0.20, 680, 0.28), (0.22, 0.24, 910, 0.24)), 0.55, 1440),
        ),
        (
            "scanner_warning.ogg",
            0.85,
            chirp(((0.02, 0.31, 390, 0.28), (0.43, 0.31, 330, 0.27)), 0.85, 1441),
        ),
        (
            "phone_unlock.ogg",
            0.42,
            chirp(((0.01, 0.20, 540, 0.18), (0.13, 0.25, 810, 0.20)), 0.42, 1442),
        ),
        (
            "ui_tap.ogg",
            0.18,
            chirp(((0.0, 0.14, 720, 0.18),), 0.18, 1443, 0.06),
        ),
        ("paper_rustle.ogg", 1.2, paper_rustle()),
        (
            "emergency_press.ogg",
            0.95,
            chirp(
                (
                    (0.0, 0.10, 105, 0.34),
                    (0.08, 0.16, 68, 0.26),
                    (0.28, 0.55, 470, 0.11),
                ),
                0.95,
                1444,
                0.16,
            ),
        ),
        (
            "radio_burst.ogg",
            0.72,
            chirp(((0.12, 0.34, 920, 0.09),), 0.72, 1445, 0.28),
        ),
        ("route_newbie_motif.ogg", 12.0, route_motif(174.6, (1.0, 1.25, 1.5), 1450)),
        ("route_veteran_motif.ogg", 12.0, route_motif(130.8, (1.0, 1.2, 1.5), 1451)),
        ("route_joker_motif.ogg", 12.0, route_motif(196.0, (1.0, 1.333, 1.667), 1452)),
        ("route_supervisor_motif.ogg", 12.0, route_motif(146.8, (1.0, 1.26, 1.68), 1453)),
        ("route_newbie_growth.ogg", 12.0, route_variant_motif(174.6, (1.0, 1.25, 1.5), 1460, True)),
        ("route_newbie_shadow.ogg", 12.0, route_variant_motif(174.6, (1.0, 1.25, 1.5), 1461, False)),
        ("route_veteran_growth.ogg", 12.0, route_variant_motif(130.8, (1.0, 1.2, 1.5), 1462, True)),
        ("route_veteran_shadow.ogg", 12.0, route_variant_motif(130.8, (1.0, 1.2, 1.5), 1463, False)),
        ("route_joker_growth.ogg", 12.0, route_variant_motif(196.0, (1.0, 1.333, 1.667), 1464, True)),
        ("route_joker_shadow.ogg", 12.0, route_variant_motif(196.0, (1.0, 1.333, 1.667), 1465, False)),
        ("route_supervisor_growth.ogg", 12.0, route_variant_motif(146.8, (1.0, 1.26, 1.68), 1466, True)),
        ("route_supervisor_shadow.ogg", 12.0, route_variant_motif(146.8, (1.0, 1.26, 1.68), 1467, False)),
    ]

    for name, duration, sampler in renders:
        render(name, duration, sampler)
        print(name)


if __name__ == "__main__":
    main()
