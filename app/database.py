from uuid import uuid4

database = {
    "books": [
        {
            "id": str(uuid4()),
            "name": "le guide du voyageur intergalactique",
            "auteur": "Douglas Adams",
            "editeur": "Galliot",
        },
        {
            "id":  str(uuid4()),
            "name": "le dernier restaurant avant la fin du monde",
            "auteur": "Douglas Adams",
            "editeur": "De poche",
        },
        {
            "id":  str(uuid4()),
            "name": "La vie, l'univers et le reste",
            "auteur": "Douglas Adams",
            "editeur": "Flammarion",
        },
    ]
}
