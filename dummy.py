if pokemon_data:
    print(f"ID: {pokemon_data['id']}")
    print(f"Name: {pokemon_data['name']}")
    types = pokemon_data['types']
    
    for index, entry in enumerate(types,start=1):
        type_name = entry['type']['name']
        print(f"Type {index} :  {type_name}")
    
    pokemon_data['level'] = 50
    print(f"Level {pokemon_data['level']}")
    # print(f"stats: {pokemon_data['stats']}")    
    
    pokemon_stats = pokemon_data['stats']
    for entry in pokemon_stats:
        stat = entry['stat']['url']
        base_stat = entry['base_stat']
        print(f"{stat} : {base_stat}")    
    
    pokemon_moves = pokemon_data['moves']
    # print(pokemon_moves)
    move_pool = []
    for entry in pokemon_moves:
        move_details = entry['version_group_details']
        move_name = entry['move']
        for details in move_details:
            if details['version_group']['name'] == "red-blue" and details['level_learned_at'] < 50:
                level_learned = details['level_learned_at']
                move_pool.append(move_name['name'])
    
    print(move_pool)  
else:
    print(f"Pokemon not found with identifier: {pokemon_identifier}")