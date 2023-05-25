def get_prompt(key):
    dct = {"Birthdate": "¿Cuándo es tu cumpleaños? Por favor incluye el año.",
           "Weight":"Ahora, ¿cuál es tu peso, por favor?",
           "Height":"¿Cuál es tu altura?",
           "SmartWatch":"¿Tienes un smartwatch o banda para que podamos hacer seguimiento a tu progreso?",
           "Activity Level": "¿Consideraría que no es activo, algo activo, moderadamente activo o súper activo?",
           "Fitness Level":  "¿En qué etapa te encuentras en tu viaje de fitness? ¿Recién empezando, principiante, intermedio o avanzado?",
           "Training Environment": "¿Te gusta entrenar en casa o en un ambiente híbrido?",
           "Goal": "¿Cuál es tu objetivo de fitness (perder grasa, ganar músculo, etc.)?",
           "Gender":  "¿Naciste hombre o mujer?",
           "AI Scan Permission": "¿Quieres hacer un escaneo de cuerpo con IA?"}
    return dct[key]
    