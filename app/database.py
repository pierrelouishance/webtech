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
            "email": "user@example.com",
            "password": "hashed_password",
            "first_name": "John",
            "last_name": "Doe",
            "role": "client"
        },
        {
            "id": str(uuid4()),
            "email": "admin@example.com",
            "password": "hashed_password",
            "first_name": "Admin",
            "last_name": "User",
            "role": "admin"
        }
    ]
}
