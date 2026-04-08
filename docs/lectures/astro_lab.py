from manim import *
import numpy as np

class PerturbationsScene(Scene):
    def construct(self):
        # 1. Earth and Orbit
        earth = Dot(radius=0.5, color=BLUE).move_to(ORIGIN)
        earth_label = Text("Yer", font_size=20).next_to(earth, DOWN)
        
        orbit = Ellipse(width=6, height=3, color=WHITE).move_to(ORIGIN)
        satellite = Dot(radius=0.1, color=YELLOW)
        
        title = Text("Oy va Quyosh ta'sirida Perturbatsiyalar", font_size=36, color=BLUE_A).to_edge(UP)
        self.play(Write(title))
        self.play(FadeIn(earth), FadeIn(earth_label))
        self.play(Create(orbit))
        
        ideal_text = Text("Ideal Kepler orbitasi", font_size=24, color=GREEN).to_corner(UL)
        self.play(Write(ideal_text))
        
        satellite.move_to(orbit.point_from_proportion(0))
        self.play(FadeIn(satellite))
        self.play(MoveAlongPath(satellite, orbit), run_time=3, rate_func=linear)
        
        self.play(FadeOut(ideal_text))
        perturb_text = Text("Oy va Quyosh ta'siri ostida \norbitaning chetlanishi (presessiya)", font_size=24, color=RED).to_corner(UL)
        self.play(Write(perturb_text))
        
        moon = Dot(radius=0.2, color=GRAY).move_to(RIGHT * 5 + UP * 2)
        moon_label = Text("Oy", font_size=20).next_to(moon, DOWN)
        sun = Dot(radius=0.8, color=YELLOW).move_to(LEFT * 6 + UP * 2.5)
        sun_label = Text("Quyosh", font_size=20).next_to(sun, DOWN)
        
        self.play(FadeIn(moon), FadeIn(moon_label), FadeIn(sun), FadeIn(sun_label))
        
        # Vectors of perturbation
        f_moon = Arrow(start=satellite.get_center(), end=moon.get_center(), buff=0.1, color=RED)
        f_sun = Arrow(start=satellite.get_center(), end=sun.get_center(), buff=0.2, color=ORANGE)
        
        def update_f_moon(m):
            v = moon.get_center() - satellite.get_center()
            n = v / np.linalg.norm(v)
            m.put_start_and_end_on(satellite.get_center(), satellite.get_center() + n * 1.5)
            
        def update_f_sun(m):
            v = sun.get_center() - satellite.get_center()
            n = v / np.linalg.norm(v)
            m.put_start_and_end_on(satellite.get_center(), satellite.get_center() + n * 2.5)
            
        f_moon.add_updater(update_f_moon)
        f_sun.add_updater(update_f_sun)
        self.play(Create(f_moon), Create(f_sun))
        
        orbit.generate_target()
        orbit.target.rotate(PI/2)
        
        def update_sat_during_rot(mob, dt):
            val = (self.renderer.time / 4) % 1
            mob.move_to(orbit.point_from_proportion(val))

        satellite.add_updater(update_sat_during_rot)
        self.play(Rotate(orbit, angle=PI/1.5, about_point=ORIGIN), run_time=6, rate_func=linear)
        satellite.remove_updater(update_sat_during_rot)
        
        self.play(FadeOut(f_moon), FadeOut(f_sun))
        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))


class LibrationScene(Scene):
    def construct(self):
        title = Text("Libratsiya (Lagranj) Nuqtalari", font_size=36, color=BLUE_A).to_edge(UP)
        self.play(Write(title))
        
        earth = Dot(radius=0.6, color=BLUE).move_to(LEFT * 2)
        earth_label = Text("Yer (M1)", font_size=20).next_to(earth, DOWN)
        
        moon = Dot(radius=0.3, color=GRAY).move_to(RIGHT * 3)
        moon_label = Text("Oy (M2)", font_size=20).next_to(moon, DOWN)
        
        self.play(FadeIn(earth), FadeIn(earth_label), FadeIn(moon), FadeIn(moon_label))
        
        l1 = Dot(radius=0.08, color=GREEN).move_to(RIGHT * 1.5)
        l2 = Dot(radius=0.08, color=GREEN).move_to(RIGHT * 4.5)
        l3 = Dot(radius=0.08, color=GREEN).move_to(LEFT * 5)
        
        p1 = earth.get_center()
        p2 = moon.get_center()
        vec = p2 - p1
        dist = np.linalg.norm(vec)
        height = dist * np.sqrt(3) / 2
        norm_v = vec / dist
        perp_v = np.array([-norm_v[1], norm_v[0], 0])
        
        l4_pos = p1 + vec * 0.5 + perp_v * height
        l5_pos = p1 + vec * 0.5 - perp_v * height
        
        l4 = Dot(radius=0.08, color=GREEN).move_to(l4_pos)
        l5 = Dot(radius=0.08, color=GREEN).move_to(l5_pos)
        
        l_labels = VGroup(
            Text("L1", font_size=16).next_to(l1, UP),
            Text("L2", font_size=16).next_to(l2, UP),
            Text("L3", font_size=16).next_to(l3, UP),
            Text("L4", font_size=16).next_to(l4, UP),
            Text("L5", font_size=16).next_to(l5, DOWN)
        )
        
        desc = Text("Aylanuvchi ikki jism (M1-M2) tizimida \n5 ta muqim muvozanat nuqtasi mavjud.", font_size=24).to_corner(UL)
        self.play(Write(desc))
        
        self.play(
            FadeIn(l1), FadeIn(l2), FadeIn(l3), FadeIn(l4), FadeIn(l5),
            FadeIn(l_labels)
        )
        
        self.wait(1)
        
        self.play(FadeOut(desc))
        desc_stab = Text("L1, L2, L3 - Noturg'un (beqaror)\nL4, L5 - Turg'un (barqaror)", font_size=24, color=YELLOW).to_corner(UL)
        self.play(Write(desc_stab))
        
        sat = Dot(radius=0.1, color=YELLOW).move_to(l4_pos)
        sat_label = Text("Sun'iy yo'ldosh", font_size=14).next_to(sat, RIGHT)
        self.play(FadeIn(sat), FadeIn(sat_label))
        
        path = Circle(radius=0.3, color=WHITE).move_to(l4_pos)
        path.set_stroke(opacity=0.3)
        self.play(Create(path))
        self.play(MoveAlongPath(sat, path), run_time=2)
        self.play(MoveAlongPath(sat, path), run_time=2)
        
        self.wait(1)
        self.play(FadeOut(Group(*self.mobjects)))


class StationaryOrbitsScene(Scene):
    def construct(self):
        title = Text("Sinxron va Statsionar Orbitalar", font_size=36, color=BLUE_A).to_edge(UP)
        self.play(Write(title))
        
        earth_circle = Circle(radius=1.5, color=BLUE, fill_opacity=0.8).move_to(ORIGIN)
        earth_label = Text("Yer", font_size=24, color=WHITE).move_to(ORIGIN)
        axis_line = Line(DOWN*1.5, UP*1.5, color=WHITE)
        earth_group = VGroup(earth_circle, axis_line, earth_label)
        
        self.play(FadeIn(earth_group))
        
        desc = Text("Sinxron orbita: Sun'iy yo'ldoshning aylanish davri \nYerning o'z o'qi atrofida aylanish davriga teng.", font_size=24).to_corner(UL)
        self.play(Write(desc))
        
        geo_orbit = Circle(radius=3.5, color=WHITE)
        geo_orbit.set_stroke(opacity=0.5)
        self.play(Create(geo_orbit))
        
        sat = Dot(radius=0.15, color=YELLOW).move_to(geo_orbit.point_from_proportion(0))
        sat_label = Text("Statsionar \nYo'ldosh", font_size=18).next_to(sat, RIGHT)
        sat_group = VGroup(sat, sat_label)
        
        self.play(FadeIn(sat_group))
        
        def update_earth(mob, dt):
            # Rotating only the line inside earth to show spin
            axis_line.rotate(dt, about_point=ORIGIN)
            
        def update_sat(mob, dt):
            mob.rotate(dt, about_point=ORIGIN)
            sat_label.next_to(sat, RIGHT)
            
        earth_group.add_updater(update_earth)
        sat_group.add_updater(update_sat)
        
        self.wait(6.28)
        
        earth_group.remove_updater(update_earth)
        sat_group.remove_updater(update_sat)
        
        desc2 = Text("Geostatsionar yo'ldosh Yerdagi kuzatuvchiga \nnisbatan osmonda qo'zg'almas bo'lib ko'rinadi.", font_size=24, color=GREEN).to_corner(DL)
        self.play(Write(desc2))
        
        self.wait(3)
        self.play(FadeOut(Group(*self.mobjects)))
