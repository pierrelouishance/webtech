from uuid import uuid4

database = {
    "books": [
        {
            "id": str(uuid4()),
            "name": "Le guide du voyageur intergalactique",
            "auteur": "Douglas Adams",
            "editeur": "Gallimard",
        },
        {
            "id": str(uuid4()),
            "name": "Le dernier restaurant avant la fin du monde",
            "auteur": "Douglas Adams",
            "editeur": "Le Livre de Poche",
        },
        {
            "id": str(uuid4()),
            "name": "La vie, l'univers et le reste",
            "auteur": "Douglas Adams",
            "editeur": "Flammarion",
        },
    ]
}
