from math import sqrt

# Matriz de calificaciones: usuario -> {pelicula: puntuacion}
ratings = {
    "Ana": {"Dune": 5, "Matrix": 4, "Inception": 5, "Spider-Man": 3},
    "Luis": {"Dune": 4, "Matrix": 5, "Inception": 4, "Toy Story": 2},
    "Marta": {"Dune": 3, "Matrix": 4, "Spider-Man": 5, "Toy Story": 4},
    "Pedro": {"Matrix": 2, "Inception": 5, "Spider-Man": 4, "Toy Story": 5},
    "Sofía": {"Dune": 5, "Inception": 4, "Spider-Man": 3, "Toy Story": 1},
}


def cosine_similarity(user_a, user_b, data):
    """Calcula similitud coseno entre dos usuarios."""
    items = set(data[user_a]) & set(data[user_b])
    if not items:
        return 0

    numerator = sum(data[user_a][item] * data[user_b][item] for item in items)
    a_norm = sqrt(sum(v ** 2 for v in data[user_a].values()))
    b_norm = sqrt(sum(v ** 2 for v in data[user_b].values()))

    if a_norm == 0 or b_norm == 0:
        return 0

    return numerator / (a_norm * b_norm)


def get_recommendations(target_user, data, top_n=3):
    """Recomienda películas para un usuario usando similaridad entre usuarios."""
    if target_user not in data:
        raise ValueError(f"El usuario '{target_user}' no existe.")

    all_items = set().union(*(user_ratings.keys() for user_ratings in data.values()))
    watched = set(data[target_user].keys())
    candidates = all_items - watched

    if not candidates:
        return []

    scores = {}
    for other_user in data:
        if other_user == target_user:
            continue

        similarity = cosine_similarity(target_user, other_user, data)
        if similarity <= 0:
            continue

        for item in candidates:
            if item in data[other_user]:
                score = similarity * data[other_user][item]
                scores[item] = scores.get(item, 0) + score

    if not scores:
        popularity = {}
        for user_ratings in data.values():
            for item, score in user_ratings.items():
                if item not in data[target_user]:
                    popularity[item] = popularity.get(item, 0) + score
        return sorted(popularity.items(), key=lambda x: x[1], reverse=True)[:top_n]

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return ranked[:top_n]


if __name__ == "__main__":
    user = "Ana"
    recommendations = get_recommendations(user, ratings)

    print(f"Recomendaciones para {user}:\n")
    for movie, score in recommendations:
        print(f"- {movie}: puntuación estimada = {score:.2f}")
