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
    ],
    "users": [
        {
            "id": str(uuid4()),
            "email": "john@gmail.com",
            "prenom":"john",
            "nom":"doe",
            "password": "john_password",
            "confirm_password": "john_password",
            "role":"client"
        },
        {
            "id": str(uuid4()),
            "email": "steve@gmail.com",
            "prenom":"steve",
            "nom":"estatof",
            "password": "steve_password",
            "confirm_password": "steve_password",
            "role":"admin"
        },
    ]

}
