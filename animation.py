from manimlib import *
import numpy as np

# To watch one of these scenes, run the following:
# manimgl example_scenes.py OpeningManimExample
# Use -s to skip to the end and just save the final frame
# Use -w to write the animation to a file
# Use -o to write it to a file and open it once done
# Use -n <number> to skip ahead to the n'th animation of a scene.

class QFT_intro(Scene):
    def construct(self) -> None:
        intro_words = Text(
            """
            Quantum Fourier Transform
            """
        )

        self.play(Write(intro_words))
        
        self.play(
            intro_words.animate.scale(0.75).to_corner(UL),
            run_time=2,
        )

        self.wait()

class QFT(Scene):
    def construct(self) -> None:
        

        formula = TexText(
            r"$\psi$ = \[ \sum_{n=1}^{\infty} 2^{-n} = 1 \]"
        )

        self.play(Write(formula))

        self.wait()