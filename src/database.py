import psycopg2
import json

conn = None
cur = None
try:
    conn = psycopg2.connect("host=localhost dbname=uncountable user=vikas")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS inputs(
        Experiment text,
        Polymer_1 decimal,
        Polymer_2 decimal,
        Polymer_3 decimal,
        Polymer_4 decimal,
        Carbon_Black_High_Grade decimal,
        Carbon_Black_Low_Grade decimal,
        Silica_Filler_1 decimal,
        Silica_Filler_2 decimal,
        Plasticizer_1 decimal,
        Plasticizer_2 decimal,
        Plasticizer_3 decimal,
        Antioxidant decimal,
        Coloring_Pigment decimal,
        Co_Agent_1 decimal,
        Co_Agent_2 decimal,
        Co_Agent_3 decimal,
        Curing_Agent_1 decimal,
        Curing_Agent_2 decimal,
        Oven_Temperature decimal,
        PRIMARY KEY(Experiment)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS outputs(
        Experiment text,
        Viscosity decimal,
        Cure_Time decimal,
        Elongation decimal,
        Tensile_Strength decimal,
        Compression_Set decimal,
        PRIMARY KEY(Experiment)
    )
    """)

    json_file = "Uncountable Front End Dataset.json"
    with open(json_file) as f:
        data = json.load(f)

    for experiment in data:
        inputs = data[experiment]['inputs']
        outputs = data[experiment]['outputs']
        exec = """INSERT INTO inputs VALUES('{}', '{}', '{}', '{}', '{}', '{}',
                    '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}',
                    '{}', '{}', '{}', '{}');""".format(\
                    experiment, inputs["Polymer 1"], inputs["Polymer 2"], inputs["Polymer 3"], \
                    inputs["Polymer 4"], inputs["Carbon Black High Grade"], inputs["Carbon Black Low Grade"], \
                    inputs["Silica Filler 1"], inputs["Silica Filler 2"], inputs["Plasticizer 1"], \
                    inputs["Plasticizer 2"], inputs["Plasticizer 3"], inputs["Antioxidant"], \
                    inputs["Coloring Pigment"], inputs["Co-Agent 1"], inputs["Co-Agent 2"], inputs["Co-Agent 3"], \
                    inputs["Curing Agent 1"], inputs["Curing Agent 2"], inputs["Oven Temperature"])
        cur.execute(exec)
        exec = "INSERT INTO outputs VALUES('{}', '{}', '{}', '{}', '{}', '{}');".format(\
        experiment, outputs['Viscosity'], outputs['Cure Time'], outputs['Elongation'], \
        outputs['Tensile Strength'], outputs['Compression Set'])
        cur.execute(exec)

    conn.commit()

except Exception as e:
    print(e)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
