import io, sys
p = r"N:\HEALTHKATHON\analysis\reports\13-text-channel.md"
lines = io.open(p, encoding="utf-8").read().split("\n")
out = io.open(r"N:\HEALTHKATHON\analysis\reports\scripts\_scan3.out", "w", encoding="utf-8")
for n in [8, 31, 78, 95, 136, 138, 211, 221, 246, 258, 265, 268, 269, 303, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 323, 374, 375, 394, 429, 434, 440, 447, 448, 455, 462, 465, 466, 467, 468, 490, 497, 504, 511, 528, 538, 541, 543, 546, 549]:
    out.write(f"L{n}: {lines[n-1]}\n")
out.close()
