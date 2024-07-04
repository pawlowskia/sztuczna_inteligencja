from experta import *

class BlenderComponent(Fact):
    pass

class Ingredients(Fact):
    pass

class Blender(Fact):
    pass

class Recipe(Fact):
    pass

class Problem(Fact):
    pass

class Cause(Fact):
    pass

class Solution(Fact):
    pass

class Diagnosis(Fact):
    pass

class BlenderExpert(KnowledgeEngine):
    @DefFacts()
    def components(self):
        yield BlenderComponent(name="Kabel zasilania")
        yield BlenderComponent(name="Pokrętło do regulacji prędkości")
        yield BlenderComponent(name="Silnik")
        yield BlenderComponent(name="Obudowa")
        yield BlenderComponent(name="Nóż")
        yield BlenderComponent(name="Pokrywa")
        yield BlenderComponent(name="Dzbanek")
        yield BlenderComponent(name="Przycisk zasilania")
        yield BlenderComponent(name="Mechanizm zabezpieczenia pokrywy")

    @Rule(AND(
        Blender(),
        OR(
            Ingredients(name="Owoce"),
            Ingredients(name="Białko w proszku"),
            Ingredients(name="Mleko"),
            Ingredients(name="Woda")
        ),
        Recipe(name="Koktajl owocowy")
    ))
    def fruit_smoothie_recipe(self):
        print("Przygotuj koktajl owocowy.")

    @Rule(AND(
        Blender(),
        Ingredients(name="Owoce"),
        Ingredients(name="Białko w proszku"),
        NOT(Ingredients(name="Mleko")),
        Recipe(name="Koktajl białkowy")
    ))
    def protein_smoothie_recipe(self):
        print("Przygotuj koktajl białkowy.")

    @Rule(AND(
        Blender(),
        Ingredients(name="Owoce"),
        NOT(Ingredients(name="Mleko")),
        Recipe(name="Koktajl owocowy bez laktozy")
    ))
    def lactose_free_fruit_smoothie_recipe(self):
        print("Przygotuj koktajl owocowy bez laktozy.")

    @Rule(AND(
        Blender(),
        Ingredients(name="Owoce"),
        Ingredients(name="Białko w proszku"),
        NOT(Ingredients(name="Mleko")),
        Recipe(name="Koktajl białkowy bez laktozy")
    ))
    def lactose_free_protein_smoothie_recipe(self):
        print("Przygotuj koktajl białkowy bez laktozy.")

    @Rule(BlenderComponent(name="Kabel zasilania"),
          BlenderComponent(name="Pokrętło do regulacji prędkości"),
          BlenderComponent(name="Silnik"),
          BlenderComponent(name="Obudowa"),
          BlenderComponent(name="Nóż"),
          BlenderComponent(name="Pokrywa"),
          BlenderComponent(name="Dzbanek"),
          BlenderComponent(name="Przycisk zasilania"),
          BlenderComponent(name="Mechanizm zabezpieczenia pokrywy"))
    def assemble_blender(self):
        print("Złoż blender.")
    
    @Rule(AND(
        Blender(),
        Problem(description="Blender nie chce się włączać")
    ))
    def problem_power_button(self):
        print("Problem: Blender nie chce się włączać.")

    @Rule(AND(
        Blender(),
        Problem(description="Blender nie miksuje składników")
    ))
    def problem_blending(self):
        print("Problem: Blender nie miksuje składników.")

    @Rule(AND(
        Blender(),
        Problem(description="Blender działa głośno i nieefektywnie")
    ))
    def problem_noise(self):
        print("Problem: Blender działa głośno i nieefektywnie.")

    @Rule(AND(
        Blender(),
        Cause(problem="Blender nie chce się włączać"),
        Solution(problem="Blender nie chce się włączać")
    ))
    def fix_power_button(self):
        print("Rozwiązanie: Wymień przycisk zasilania.")

    @Rule(AND(
        Blender(),
        Cause(problem="Blender nie miksuje składników"),
        Solution(problem="Blender nie miksuje składników")
    ))
    def fix_blending(self):
        print("Rozwiązanie: Napraw lub wymień silnik blendera.")

    @Rule(AND(
        Blender(),
        Cause(problem="Blender działa głośno i nieefektywnie"),
        Solution(problem="Blender działa głośno i nieefektywnie")
    ))
    def fix_noise(self):
        print("Rozwiązanie: Napraw lub wymień pokrętło do regulacji prędkości.")

    @Rule(AND(
        Blender(),
        Problem(description="Blender nie chce się włączać"),
        Diagnosis(problem="Blender nie chce się włączać")
    ))
    def diagnose_power_button(self):
        print("Diagnoza: Blender nie chce się włączyć -> przyczyna: przycisk zasilania się zepsuł.")

    @Rule(AND(
        Blender(),
        Problem(description="Blender nie miksuje składników"),
        Diagnosis(problem="Blender nie miksuje składników")
    ))
    def diagnose_blending(self):
        print("Diagnoza: Blender nie miksuje składników -> przyczyna: silnik blendera jest uszkodzony.")

    @Rule(AND(
        Blender(),
        Problem(description="Blender działa głośno i nieefektywnie"),
        Diagnosis(problem="Blender działa głośno i nieefektywnie")
    ))
    def diagnose_noise(self):
        print("Diagnoza: Blender działa głośno i nieefektywnie -> przyczyna: pokrętło do regulacji prędkości nie działa poprawnie.")


engine = BlenderExpert()
engine.reset()
# 1. Przygotowanie koktajlu owocowego:

engine.declare(Blender())
engine.declare(Ingredients(name="Owoce"))
engine.declare(Recipe(name="Koktajl owocowy"))
engine.run()

# 2. Przygotowanie koktajlu białkowego bez laktozy
engine.reset()
engine.declare(Blender())
engine.declare(Ingredients(name="Owoce"))
engine.declare(Ingredients(name="Białko w proszku"))
engine.declare(Recipe(name="Koktajl białkowy bez laktozy"))
engine.run()

# 3. Problem: Blender nie chce się włączać
engine.reset()
engine.declare(Blender())
engine.declare(Problem(description="Blender nie chce się włączać"))
engine.run()

# 4. Rozwiązanie: Wymień przycisk zasilania

engine.reset()
engine.declare(Blender())
engine.declare(Cause(problem="Blender nie chce się włączać"))
engine.declare(Solution(problem="Blender nie chce się włączać"))
engine.run()

# 5. Diagnoza: Blender nie chce się włączyć -> przyczyna: przycisk zasilania się zepsuł:
engine.reset()
engine.declare(Blender())
engine.declare(Problem(description="Blender nie chce się włączać"))
engine.declare(Diagnosis(problem="Blender nie chce się włączać"))
engine.run()
