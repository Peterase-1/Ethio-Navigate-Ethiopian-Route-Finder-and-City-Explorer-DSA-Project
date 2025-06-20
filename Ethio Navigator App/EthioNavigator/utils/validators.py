def validate_city_connection(from_city, to_city, distance):
    if not from_city or not to_city:
        raise ValueError("City names cannot be empty.")
    if from_city == to_city:
        raise ValueError("From city and to city cannot be the same.")
    if not isinstance(distance, int) or distance <= 0:
        raise ValueError("Distance must be a positive integer.")