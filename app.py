from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import random
import math
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'adventurous_traveler_secret_key_2024')
CORS(app, supports_credentials=True)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'suprim123',
    'database': 'adventurous_traveler_game',
    'autocommit': False
}

def get_db_connection():
    """Get database connection"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> int:

    R = 6371
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return int(R * c)

def get_cardinal_direction(lat1: float, lon1: float, lat2: float, lon2: float) -> str:
    
    lat_diff = lat2 - lat1
    lon_diff = lon2 - lon1
    
    if abs(lat_diff) > abs(lon_diff):
        return "north" if lat_diff > 0 else "south"
    else:
        return "east" if lon_diff > 0 else "west"

def get_distance_category(distance: int) -> str:
    
    if distance < 300:
        return "very close (under 300km)"
    elif distance < 600:
        return "close (300-600km)"
    elif distance < 1200:
        return "medium distance (600-1200km)"
    elif distance < 2000:
        return "far (1200-2000km)"
    else:
        return "very far (over 2000km)"

def generate_clue_text(current_airport: Dict, target_airport: Dict, clue_type: str, clue_quality: str) -> str:
    
    distance = calculate_distance(
        current_airport['latitude'], current_airport['longitude'],
        target_airport['latitude'], target_airport['longitude']
    )
    direction = get_cardinal_direction(
        current_airport['latitude'], current_airport['longitude'],
        target_airport['latitude'], target_airport['longitude']
    )
    
    
    if clue_quality == 'low':
        distance_range = f"approximately {distance + random.randint(-200, 200)}km"
    elif clue_quality == 'medium':
        distance_range = f"about {distance}km"
    else:
        distance_range = f"exactly {distance}km"
    
    if clue_type == 'DIRECTION':
        return f"The target is to the {direction} of your current location, {distance_range} away."
    
    elif clue_type == 'DISTANCE':
        cardinal = ['north', 'south', 'east', 'west'][random.randint(0, 3)]
        return f"The target is {distance_range} to the {cardinal}."
    
    elif clue_type == 'REGION':
        return f"The target is in the {target_airport['region']} region, {distance_range} away."
    
    elif clue_type == 'AIRPORT_TYPE':
        size_map = {'small': 'small regional', 'medium': 'medium-sized', 'large': 'major international'}
        return f"Look for a {size_map.get(target_airport['airport_size'], 'medium-sized')} airport, {distance_range} away."
    
    elif clue_type == 'COUNTRY':
        return f"The target is in {target_airport['country']}, {distance_range} away."
    
    elif clue_type == 'NAME_PATTERN':
        if random.random() > 0.5:
            return f"The airport name contains '{target_airport['city'][:3].lower()}', {distance_range} away."
        else:
            return f"The airport code starts with '{target_airport['code'][:2]}', {distance_range} away."
    
    elif clue_type == 'SPECIFIC':
        options = [
            f"Rumors say it's near {target_airport['city']}, {distance_range} away.",
            f"Search in {target_airport['region']} for clues, {distance_range} away.",
            f"Look for airport with runway length around {target_airport['runway_length_m']}m, {distance_range} away.",
            f"The destination is {get_distance_category(distance)}, to the {direction}."
        ]
        return random.choice(options)
    
    elif clue_type == 'EXACT_LOCATION':
        return f"Exact location: {target_airport['name']} ({target_airport['code']}) in {target_airport['city']}, {target_airport['country']}."
    
    return "No clue available."

def get_random_airport(exclude_ids: List[int] = None) -> Optional[Dict]:
    """Get random airport excluding specified IDs"""
    conn = get_db_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        if exclude_ids:
            exclude_str = ','.join(str(id) for id in exclude_ids)
            query = f"SELECT * FROM airports WHERE id NOT IN ({exclude_str}) ORDER BY RAND() LIMIT 1"
            cursor.execute(query)
        else:
            cursor.execute("SELECT * FROM airports ORDER BY RAND() LIMIT 1")
        
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def initialize_game_artifacts(game_id: int, cursor) -> bool:
    
    try:
        
        cursor.execute("SELECT id FROM airports ORDER BY RAND() LIMIT 1")
        hidden_airport = cursor.fetchone()
        
        if not hidden_airport:
            return False
        
        
        cursor.execute("SELECT id FROM artifacts ORDER BY artifact_order")
        artifacts = cursor.fetchall()
        
        
        for artifact in artifacts:
            
            exclude_ids = [hidden_airport['id']]
            
            # Get previously assigned delivery airports in this game
            cursor.execute("""
                SELECT DISTINCT delivery_airport_id 
                FROM player_artifacts 
                WHERE game_id = %s AND delivery_airport_id IS NOT NULL
            """, (game_id,))
            
            previous_deliveries = cursor.fetchall()
            exclude_ids.extend([d['delivery_airport_id'] for d in previous_deliveries])
            
            # Find unique delivery airport
            exclude_str = ','.join(str(id) for id in exclude_ids)
            cursor.execute(f"""
                SELECT id FROM airports 
                WHERE id NOT IN ({exclude_str}) 
                ORDER BY RAND() LIMIT 1
            """)
            
            delivery_airport = cursor.fetchone()
            
            if not delivery_airport:
                # If we run out of airports, use any except hidden
                cursor.execute(f"""
                    SELECT id FROM airports 
                    WHERE id != {hidden_airport['id']}
                    ORDER BY RAND() LIMIT 1
                """)
                delivery_airport = cursor.fetchone()
            
            # Create player artifact record
            cursor.execute("""
                INSERT INTO player_artifacts 
                (game_id, artifact_id, status, delivery_airport_id, is_dug)
                VALUES (%s, %s, %s, %s, %s)
            """, (game_id, artifact['id'], 'HIDDEN', delivery_airport['id'], 0))
        
        cursor.execute("""
            UPDATE games 
            SET artifact_airport_id = %s
            WHERE id = %s
        """, (hidden_airport['id'], game_id))
        
        return True
        
    except Error as e:
        print(f"Initialize artifacts error: {e}")
        return False

def generate_random_event(game_id: int, cursor):
    """Generate and apply random event"""
    try:
        # Get random event
        cursor.execute("SELECT * FROM random_events ORDER BY RAND() LIMIT 1")
        event = cursor.fetchone()
        
        if not event:
            return None
        
        # Apply event effects
        money_change = event['money_effect']
        fuel_change = 0
        
        if event['fuel_effect_fixed'] != 0:
            fuel_change = event['fuel_effect_fixed']
        elif event['fuel_effect_percent'] != 0:
            cursor.execute("SELECT fuel_km FROM games WHERE id = %s", (game_id,))
            current_fuel = cursor.fetchone()['fuel_km']
            fuel_change = int(current_fuel * event['fuel_effect_percent'] / 100)
        
        travels_change = event['travels_effect']
        
        # Update game
        cursor.execute("""
            UPDATE games 
            SET money = money + %s,
                fuel_km = GREATEST(0, fuel_km + %s),
                travels_remaining = GREATEST(0, travels_remaining + %s)
            WHERE id = %s
        """, (money_change, fuel_change, travels_change, game_id))
        
        # Log event
        cursor.execute("""
            INSERT INTO game_events 
            (game_id, event_id, description, money_change, fuel_change, travels_change)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (game_id, event['id'], event['description'], money_change, fuel_change, travels_change))
        
        # Log to game logs
        cursor.execute("""
            INSERT INTO game_logs 
            (game_id, log_type, description, money_change, fuel_change)
            VALUES (%s, 'EVENT_TRIGGERED', %s, %s, %s)
        """, (game_id, f"{event['name']}: {event['description']}", money_change, fuel_change))
        
        return {
            'name': event['name'],
            'description': event['description'],
            'money_change': money_change,
            'fuel_change': fuel_change,
            'travels_change': travels_change,
            'type': event['event_type']
        }
        
    except Error as e:
        print(f"Generate event error: {e}")
        return None

def generate_quest(game_id: int, cursor) -> Optional[Dict]:
    """Generate a new quest for the player"""
    try:
        # Get game phase
        cursor.execute("SELECT current_phase FROM games WHERE id = %s", (game_id,))
        phase = cursor.fetchone()['current_phase']
        
        # Get current artifact
        cursor.execute("""
            SELECT pa.artifact_id, a.name as artifact_name
            FROM player_artifacts pa
            JOIN artifacts a ON pa.artifact_id = a.id
            WHERE pa.game_id = %s AND pa.status IN ('HIDDEN', 'FOUND')
            ORDER BY a.artifact_order
            LIMIT 1
        """, (game_id,))
        
        current_artifact = cursor.fetchone()
        
        if not current_artifact:
            return None
        
        quest_types = ['EXPLORATION', 'TRANSPORT', 'SCANNING']
        quest_type = random.choice(quest_types)
        
        titles = {
            'EXPLORATION': 'Explore New Regions',
            'TRANSPORT': 'Cargo Transport',
            'SCANNING': 'Radar Scanning'
        }
        
        descriptions = {
            'EXPLORATION': 'Visit 3 different regions to gather information about artifact locations.',
            'TRANSPORT': 'Deliver a package to earn money and fuel.',
            'SCANNING': 'Use scanning equipment to reveal hidden clues.'
        }
        
        requirements = {}
        
        if quest_type == 'EXPLORATION':
            requirements = {'regions_to_visit': 3, 'current_count': 0}
        elif quest_type == 'TRANSPORT':
            requirements = {'distance_km': random.randint(800, 1500), 'current_km': 0}
        
        reward_money = random.randint(500, 1500)
        reward_fuel = random.randint(200, 600)
        
        # Insert quest
        cursor.execute("""
            INSERT INTO quests 
            (game_id, quest_type, title, description, requirements, target_artifact_id,
            reward_money, reward_fuel, progress_required, expires_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            game_id, quest_type, titles[quest_type], descriptions[quest_type],
            json.dumps(requirements), current_artifact['artifact_id'],
            reward_money, reward_fuel, 1,
            datetime.now() + timedelta(minutes=30) if quest_type == 'TIMED' else None
        ))
        
        quest_id = cursor.lastrowid
        
        return {
            'id': quest_id,
            'type': quest_type,
            'title': titles[quest_type],
            'description': descriptions[quest_type],
            'requirements': requirements,
            'rewards': {'money': reward_money, 'fuel': reward_fuel},
            'progress': 0,
            'progress_required': 1
        }
        
    except Error as e:
        print(f"Generate quest error: {e}")
        return None

def generate_clue(game_id: int, cursor, clue_quality: str = 'medium', shop_bonus: float = 0.0) -> Optional[Dict]:

    try:
        # Get game state
        cursor.execute("""
            SELECT g.current_phase, g.current_airport_id, a.latitude, a.longitude,
                    g.clue_accuracy_bonus
            FROM games g
            JOIN airports a ON g.current_airport_id = a.id
            WHERE g.id = %s
        """, (game_id,))
        
        game_state = cursor.fetchone()
        
        if not game_state:
            return None
        
        # Get current target (either hidden artifact or delivery location)
        cursor.execute("""
            SELECT pa.*, a.name as artifact_name, 
                    ha.id as hidden_airport_id, ha.latitude as hidden_lat, ha.longitude as hidden_lng,
                    ha.region as hidden_region, ha.city as hidden_city, ha.country as hidden_country,
                    ha.code as hidden_code, ha.airport_size as hidden_size,
                    da.id as delivery_airport_id, da.latitude as delivery_lat, da.longitude as delivery_lng,
                    da.region as delivery_region, da.city as delivery_city, da.country as delivery_country,
                    da.code as delivery_code, da.airport_size as delivery_size
            FROM player_artifacts pa
            JOIN artifacts a ON pa.artifact_id = a.id
            JOIN games g ON pa.game_id = g.id
            LEFT JOIN airports ha ON g.artifact_airport_id = ha.id
            LEFT JOIN airports da ON pa.delivery_airport_id = da.id
            WHERE pa.game_id = %s AND pa.status IN ('HIDDEN', 'FOUND')
            ORDER BY a.artifact_order
            LIMIT 1
        """, (game_id,))
        
        target = cursor.fetchone()
        
        if not target:
            return None
        
        # Determine clue type based on phase
        phase = game_state['current_phase']
        
        if phase == 'FINDING_ARTIFACTS':
            # Clue about hidden location
            if not target['hidden_airport_id']:
                return None
            target_airport = {
                'id': target['hidden_airport_id'],
                'latitude': target['hidden_lat'],
                'longitude': target['hidden_lng'],
                'region': target['hidden_region'],
                'city': target['hidden_city'],
                'country': target['hidden_country'],
                'code': target['hidden_code'],
                'airport_size': target['hidden_size'],
                'runway_length_m': 3000  # Default
            }
            clue_phase = 'FINDING'
        else:
            # Clue about delivery location
            if not target['delivery_airport_id']:
                return None
            target_airport = {
                'id': target['delivery_airport_id'],
                'latitude': target['delivery_lat'],
                'longitude': target['delivery_lng'],
                'region': target['delivery_region'],
                'city': target['delivery_city'],
                'country': target['delivery_country'],
                'code': target['delivery_code'],
                'airport_size': target['delivery_size'],
                'runway_length_m': 3000  # Default
            }
            clue_phase = 'DELIVERING'
        
        # Get current airport info
        cursor.execute("SELECT * FROM airports WHERE id = %s", (game_state['current_airport_id'],))
        current_airport_db = cursor.fetchone()
        
        if not current_airport_db:
            return None
        
        current_airport = {
            'latitude': current_airport_db['latitude'],
            'longitude': current_airport_db['longitude']
        }
        
        # Determine clue type based on quality and shop bonuses
        clue_types = ['DIRECTION', 'DISTANCE', 'REGION', 'AIRPORT_TYPE', 'COUNTRY', 'NAME_PATTERN', 'SPECIFIC']
        
        # Apply shop bonuses to clue quality
        effective_quality = clue_quality
        if shop_bonus > 0:
            if random.random() < shop_bonus:
                if clue_quality == 'low':
                    effective_quality = 'medium'
                elif clue_quality == 'medium':
                    effective_quality = 'high'
                elif clue_quality == 'high':
                    effective_quality = 'exact'
        
        if effective_quality == 'low':
            clue_type = random.choice(clue_types[:3])
        elif effective_quality == 'medium':
            clue_type = random.choice(clue_types[2:5])
        elif effective_quality == 'high':
            clue_type = random.choice(clue_types[4:6])
        elif effective_quality == 'exact':
            clue_type = 'EXACT_LOCATION'
        else:
            clue_type = random.choice(clue_types)
        
        
        clue_text = generate_clue_text(current_airport, target_airport, clue_type, effective_quality)
        
        cursor.execute("""
            INSERT INTO game_clues 
            (game_id, artifact_id, target_airport_id, clue_type, clue_text, phase, quality, is_revealed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
        """, (
            game_id, target['artifact_id'], 
            target_airport['id'],
            clue_type, clue_text, clue_phase, effective_quality
        ))
        
        clue_id = cursor.lastrowid
        
        
        cursor.execute("""
            INSERT INTO game_logs 
            (game_id, log_type, description)
            VALUES (%s, 'CLUE_FOUND', %s)
        """, (game_id, f"Discovered clue: {clue_text}"))
        
        return {
            'id': clue_id,
            'type': clue_type,
            'text': clue_text,
            'phase': clue_phase,
            'quality': effective_quality,
            'artifact_name': target['artifact_name'],
            'target_airport_id': target_airport['id'],
            'target_airport_code': target_airport['code']
        }
        
    except Error as e:
        print(f"Generate clue error: {e}")
        return None

def check_quest_completion(game_id: int, quest_id: int, cursor) -> bool:
    
    try:
        
        cursor.execute("""
            SELECT * FROM quests 
            WHERE id = %s AND game_id = %s AND is_completed = 0 AND is_failed = 0
        """, (quest_id, game_id))
        
        quest = cursor.fetchone()
        
        if not quest:
            return False
        
        
        requirements = json.loads(quest['requirements']) if quest['requirements'] else {}
        
        if quest['quest_type'] == 'EXPLORATION':
            # Check if player visited required regions
            cursor.execute("""
                SELECT COUNT(DISTINCT a.region) as regions_visited
                FROM game_logs gl
                JOIN airports a ON gl.airport_id = a.id
                WHERE gl.game_id = %s AND gl.log_type = 'FLIGHT'
            """, (game_id,))
            
            result = cursor.fetchone()
            regions_visited = result['regions_visited'] if result else 0
            
            return regions_visited >= requirements.get('regions_to_visit', 3)
        
        elif quest['quest_type'] == 'TRANSPORT':
            # Check if player traveled required distance
            cursor.execute("""
                SELECT SUM(distance_km) as total_distance
                FROM game_logs 
                WHERE game_id = %s AND log_type = 'FLIGHT'
            """, (game_id,))
            
            result = cursor.fetchone()
            total_distance = result['total_distance'] if result else 0
            
            return total_distance >= requirements.get('distance_km', 1000)
        
        elif quest['quest_type'] == 'SCANNING':
            # Check if player found clues
            cursor.execute("""
                SELECT COUNT(*) as clues_found
                FROM game_clues 
                WHERE game_id = %s
            """, (game_id,))
            
            result = cursor.fetchone()
            clues_found = result['clues_found'] if result else 0
            
            return clues_found >= 1
        
        return False
        
    except Exception as e:
        print(f"Check quest completion error: {e}")
        return False

def check_game_status(game_id: int, cursor) -> str:
    """Check and update game status"""
    try:
        # Get current game state
        cursor.execute("""
            SELECT g.artifacts_delivered, g.travels_remaining, g.fuel_km, g.money, 
                   g.game_status, g.current_airport_id, g.current_phase
            FROM games g
            WHERE g.id = %s
        """, (game_id,))
        
        game = cursor.fetchone()
        
        if game['game_status'] != 'ACTIVE':
            return game['game_status']
        
        # Check win condition FIRST (highest priority)
        if game['artifacts_delivered'] >= 10:
            cursor.execute("UPDATE games SET game_status = 'WON' WHERE id = %s", (game_id,))
            return 'WON'
        
        # Check if player can still deliver at current location
        # This prevents losing when at a delivery location with 0 travels left
        if game['current_phase'] == 'DELIVERING_ARTIFACTS':
            cursor.execute("""
                SELECT COUNT(*) as deliverable_count
                FROM player_artifacts
                WHERE game_id = %s 
                  AND delivery_airport_id = %s 
                  AND status = 'FOUND'
            """, (game_id, game['current_airport_id']))
            
            result = cursor.fetchone()
            can_deliver_here = result['deliverable_count'] > 0 if result else False
            
            # If player is at a delivery location with artifacts to deliver,
            # don't end the game yet even if travels = 0
            if can_deliver_here and game['travels_remaining'] == 0:
                return 'ACTIVE'  # Let them deliver before game ends
        
        # Check lose conditions
        lose_reason = None
        
        
        if game['travels_remaining'] <= 0:
            # Final check: Can they still win from current position?
            if game['current_phase'] == 'FINDING_ARTIFACTS':
                # Check if already at artifact airport
                cursor.execute("""
                    SELECT artifact_airport_id 
                    FROM games 
                    WHERE id = %s
                """, (game_id,))
                artifact_location = cursor.fetchone()
                
                if artifact_location and artifact_location['artifact_airport_id'] == game['current_airport_id']:
                    return 'ACTIVE'  # Let them dig
                else:
                    lose_reason = "No more travels left"
            else:
                
                lose_reason = "No more travels left"
        
        elif game['fuel_km'] <= 0:
            lose_reason = "Out of fuel"
        elif game['money'] < 0:
            lose_reason = "Out of money"
        
        if lose_reason:
            cursor.execute("""
                UPDATE games 
                SET game_status = 'LOST', lose_reason = %s
                WHERE id = %s
            """, (lose_reason, game_id))
            return 'LOST'
        
        return 'ACTIVE'
        
    except Error as e:
        print(f"Check game status error: {e}")
        return 'ACTIVE'

#Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/game')
def game_page():
    game_id = request.args.get('game_id') or session.get('game_id')
    if not game_id:
        return redirect(url_for('welcome'))
    return render_template('game.html')

@app.route('/api/game/create', methods=['POST'])
def create_game():
    """Create a new game"""
    try:
        data = request.json
        player_name = data.get('player_name', 'Adventurer').strip()
        
        if not player_name or len(player_name) < 3:
            return jsonify({'success': False, 'error': 'Name must be at least 3 characters'})
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'})
        
        cursor = conn.cursor(dictionary=True)
        
        # Select random starting airport (prefer large airports)
        cursor.execute("SELECT id FROM airports WHERE airport_size = 'large' ORDER BY RAND() LIMIT 1")
        start_airport = cursor.fetchone()
        
        if not start_airport:
            cursor.execute("SELECT id FROM airports ORDER BY RAND() LIMIT 1")
            start_airport = cursor.fetchone()
        
        # Create game record
        cursor.execute("""
            INSERT INTO games 
            (player_name, current_airport_id, money, fuel_km, max_fuel_capacity, 
                travels_remaining, artifacts_found, artifacts_delivered, game_status,
                clue_accuracy_bonus, clue_reveal_chance, marker_reveal_chance)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            player_name, start_airport['id'], 10000, 2000, 5000, 
            20, 0, 0, 'ACTIVE', 0, 0.1, 0.0
        ))
        
        game_id = cursor.lastrowid
        
        # Initialize all artifacts (all in one airport, deliver to different airports)
        if not initialize_game_artifacts(game_id, cursor):
            conn.rollback()
            return jsonify({'success': False, 'error': 'Failed to initialize artifacts'})
        
        # Log game creation
        cursor.execute("""
            INSERT INTO game_logs (game_id, log_type, description)
            VALUES (%s, 'GAME_STATUS', 'Game started! Find all artifacts in one airport, then deliver them.')
        """, (game_id,))
        
        conn.commit()
        
        session['game_id'] = game_id
        session['player_name'] = player_name
        
        return jsonify({
            'success': True, 
            'game_id': game_id,
            'player_name': player_name
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Create game error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/game/state')
def get_game_state():
    """Get complete game state"""
    game_id = request.args.get('game_id') or session.get('game_id')
    
    if not game_id:
        return jsonify({'success': False, 'error': 'No game ID'})
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'success': False, 'error': 'Database connection failed'})
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get game state with current airport info
        cursor.execute("""
            SELECT g.*, 
                    a.code as current_airport_code, a.name as current_airport_name,
                    a.city as current_city, a.country as current_country,
                    a.latitude as current_latitude, a.longitude as current_longitude,
                    a.region as current_region,
                    art_a.code as artifact_airport_code, art_a.name as artifact_airport_name
            FROM games g
            LEFT JOIN airports a ON g.current_airport_id = a.id
            LEFT JOIN airports art_a ON g.artifact_airport_id = art_a.id
            WHERE g.id = %s
        """, (game_id,))
        
        game = cursor.fetchone()
        
        if not game:
            return jsonify({'success': False, 'error': 'Game not found'})
        
        # Get player artifacts with status
        cursor.execute("""
            SELECT pa.*, a.name as artifact_name, a.description, a.artifact_order,
                    a.delivery_reward_money, a.delivery_reward_fuel, a.difficulty_level,
                    da.code as delivery_airport_code, da.name as delivery_airport_name,
                    da.city as delivery_city, da.country as delivery_country
            FROM player_artifacts pa
            JOIN artifacts a ON pa.artifact_id = a.id
            LEFT JOIN airports da ON pa.delivery_airport_id = da.id
            WHERE pa.game_id = %s
            ORDER BY a.artifact_order
        """, (game_id,))
        
        player_artifacts = cursor.fetchall()
        
        # Get revealed clues
        cursor.execute("""
            SELECT gc.*, a.name as artifact_name
            FROM game_clues gc
            JOIN artifacts a ON gc.artifact_id = a.id
            WHERE gc.game_id = %s AND gc.is_revealed = 1
            ORDER BY gc.discovered_at DESC
        """, (game_id,))
        
        clues = cursor.fetchall()
        
        # Get active quests
        cursor.execute("""
            SELECT * FROM quests 
            WHERE game_id = %s AND is_completed = 0 AND is_failed = 0
            ORDER BY created_at DESC
        """, (game_id,))
        
        quests = cursor.fetchall()
        
        # Get recent logs
        cursor.execute("""
            SELECT * FROM game_logs 
            WHERE game_id = %s 
            ORDER BY created_at DESC 
            LIMIT 50
        """, (game_id,))
        
        logs = cursor.fetchall()
        
        # Get player inventory
        cursor.execute("""
            SELECT * FROM player_inventory 
            WHERE game_id = %s AND quantity > 0
            ORDER BY purchased_at DESC
        """, (game_id,))
        
        inventory = cursor.fetchall()
        
        # Get all airports for map
        cursor.execute("""
            SELECT id, code, name, city, country, latitude, longitude, 
                   airport_size, region, is_tourist_destination, runway_length_m
            FROM airports 
            ORDER BY name
        """)
        
        airports = cursor.fetchall()
        
        # Check game status
        status = check_game_status(game_id, cursor)
        
        return jsonify({
            'success': True,
            'game': game,
            'player_artifacts': player_artifacts,
            'clues': clues,
            'quests': quests,
            'logs': logs,
            'inventory': inventory,
            'airports': airports,
            'game_status': status
        })
        
    except Exception as e:
        print(f"Get game state error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/api/game/travel', methods=['POST'])
def travel():
    """Travel to another airport"""
    try:
        data = request.json
        game_id = data.get('game_id') or session.get('game_id')
        destination_id = data.get('destination_airport_id')
        
        if not game_id or not destination_id:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get current game state
        cursor.execute("""
            SELECT g.*, a.latitude as current_lat, a.longitude as current_lng
            FROM games g
            JOIN airports a ON g.current_airport_id = a.id
            WHERE g.id = %s AND g.game_status = 'ACTIVE'
        """, (game_id,))
        
        game = cursor.fetchone()
        
        if not game:
            return jsonify({'success': False, 'error': 'Game not active'})
        
        if game['travels_remaining'] <= 0:
            return jsonify({'success': False, 'error': 'No travels remaining'})
        
        if game['current_airport_id'] == destination_id:
            return jsonify({'success': False, 'error': 'Already at this airport'})
        
        # Get destination airport
        cursor.execute("SELECT * FROM airports WHERE id = %s", (destination_id,))
        destination = cursor.fetchone()
        
        if not destination:
            return jsonify({'success': False, 'error': 'Destination not found'})
        
        # Calculate distance and fuel cost
        distance = calculate_distance(
            game['current_lat'], game['current_lng'],
            destination['latitude'], destination['longitude']
        )
        
        # Apply fuel efficiency bonus
        fuel_cost = int(distance * (1 - game.get('fuel_efficiency_bonus', 0) / 100.0))
        
        # FIXED: Check fuel pass FIRST before checking fuel availability
        will_use_fuel_pass = game.get('fuel_pass_remaining', 0) > 0
        
        if will_use_fuel_pass:
            # Using fuel pass - no fuel cost
            actual_fuel_cost = 0
        else:
            # Not using fuel pass - check if enough fuel
            actual_fuel_cost = fuel_cost
            if game['fuel_km'] < fuel_cost:
                return jsonify({'success': False, 'error': f'Need {fuel_cost}km fuel, have {game["fuel_km"]}km. Consider buying a Fuel Pass!'})
        
        # Update game state
        if will_use_fuel_pass:
            # Deduct fuel pass
            cursor.execute("""
                UPDATE games 
                SET fuel_km = fuel_km - %s,
                    current_airport_id = %s,
                    travels_used = travels_used + 1,
                    travels_remaining = travels_remaining - 1,
                    flights_taken = flights_taken + 1,
                    fuel_pass_remaining = fuel_pass_remaining - 1,
                    updated_at = NOW()
                WHERE id = %s
            """, (actual_fuel_cost, destination_id, game_id))
        else:
            # Normal travel
            cursor.execute("""
                UPDATE games 
                SET fuel_km = fuel_km - %s,
                    current_airport_id = %s,
                    travels_used = travels_used + 1,
                    travels_remaining = travels_remaining - 1,
                    flights_taken = flights_taken + 1,
                    updated_at = NOW()
                WHERE id = %s
            """, (actual_fuel_cost, destination_id, game_id))
        
        # Log flight
        log_desc = f"Traveled to {destination['code']} ({distance}km)"
        if will_use_fuel_pass:
            log_desc += " [FUEL PASS USED]"
        
        cursor.execute("""
            INSERT INTO game_logs 
            (game_id, log_type, description, money_change, fuel_change, airport_id, distance_km)
            VALUES (%s, 'FLIGHT', %s, %s, %s, %s, %s)
        """, (
            game_id, 
            log_desc,
            0, -actual_fuel_cost, destination_id, distance
        ))
        
        result = {
            'distance': distance,
            'fuel_cost': actual_fuel_cost,
            'used_fuel_pass': will_use_fuel_pass,
            'destination': {
                'code': destination['code'],
                'name': destination['name'],
                'city': destination['city'],
                'country': destination['country']
            }
        }
        
        # Check if at artifact airport (finding phase)
        if game['current_phase'] == 'FINDING_ARTIFACTS' and destination_id == game['artifact_airport_id']:
            result['at_artifact_airport'] = True
            result['can_dig'] = True
        
        # Check for artifact delivery (if in DELIVERING phase)
        elif game['current_phase'] == 'DELIVERING_ARTIFACTS':
            cursor.execute("""
                SELECT pa.*, a.name as artifact_name, a.delivery_reward_money, a.delivery_reward_fuel
                FROM player_artifacts pa
                JOIN artifacts a ON pa.artifact_id = a.id
                WHERE pa.game_id = %s AND pa.delivery_airport_id = %s AND pa.status = 'FOUND'
            """, (game_id, destination_id))
            
            artifacts_to_deliver = cursor.fetchall()
            
            if artifacts_to_deliver:
                result['can_deliver'] = True
                result['artifacts_count'] = len(artifacts_to_deliver)
        
        # Random events
        event_result = None
        if random.random() < 0.70:
            event_result = generate_random_event(game_id, cursor)
            if event_result:
                result['event'] = event_result
                conn.commit()
                cursor = conn.cursor(dictionary=True)
        
        # Clues
        base_clue_chance = 0.40
        shop_bonus = game.get('clue_reveal_chance', 0)
        total_clue_chance = min(0.95, base_clue_chance + shop_bonus)
        
        if random.random() < total_clue_chance:
            clue_quality = 'medium'
            
            if game.get('clue_accuracy_bonus', 0) > 0:
                if random.random() < (game['clue_accuracy_bonus'] / 100.0):
                    clue_quality = 'high'
            
            clue_result = generate_clue(game_id, cursor, clue_quality, shop_bonus)
            if clue_result:
                result['clue'] = clue_result
        
        # Quests
        if random.random() < 0.20:
            quest_result = generate_quest(game_id, cursor)
            if quest_result:
                result['quest'] = quest_result
        
        conn.commit()
        
        # Get updated game state
        cursor.execute("SELECT * FROM games WHERE id = %s", (game_id,))
        updated_game = cursor.fetchone()
        
        result['game'] = updated_game
        
        return jsonify({'success': True, **result})
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Travel error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


@app.route('/api/game/dig', methods=['POST'])
def dig_for_artifacts():
    
    try:
        data = request.json
        game_id = data.get('game_id') or session.get('game_id')
        
        if not game_id:
            return jsonify({'success': False, 'error': 'No game ID'})
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        
        cursor.execute("""
            SELECT g.*, a.latitude, a.longitude
            FROM games g
            JOIN airports a ON g.current_airport_id = a.id
            WHERE g.id = %s
        """, (game_id,))
        
        game = cursor.fetchone()
        
        if not game:
            return jsonify({'success': False, 'error': 'Game not found'})
        
        
        if game['current_airport_id'] != game['artifact_airport_id']:
            return jsonify({'success': False, 'error': 'No artifacts to dig here'})
        
        
        if game['artifacts_found'] >= 10:
            return jsonify({'success': False, 'error': 'All artifacts already found'})
        
        
        cursor.execute("""
            INSERT INTO game_logs 
            (game_id, log_type, description, airport_id)
            VALUES (%s, 'DIG_ATTEMPT', 'Attempted to dig for artifacts', %s)
        """, (game_id, game['current_airport_id']))
        
        
        if random.random() < 0.6:
            
            cursor.execute("""
                UPDATE player_artifacts 
                SET status = 'FOUND', found_at = NOW(), is_dug = 1
                WHERE game_id = %s AND status = 'HIDDEN'
            """, (game_id,))
            
            
            cursor.execute("""
                UPDATE games 
                SET current_phase = 'DELIVERING_ARTIFACTS',
                    artifacts_found = 10,
                    updated_at = NOW()
                WHERE id = %s
            """, (game_id,))
            
            
            cursor.execute("""
                INSERT INTO game_logs 
                (game_id, log_type, description)
                VALUES (%s, 'ARTIFACT_FOUND', 'Found all 10 artifacts! Now deliver them to their destinations.')
            """, (game_id,))
            
            conn.commit()
            
            return jsonify({
                'success': True,
                'found': True,
                'message': 'You found all 10 artifacts! Now deliver them to their destinations.',
                'phase_changed': True
            })
        else:
            # Dig failed
            conn.commit()
            return jsonify({
                'success': True,
                'found': False,
                'message': 'You dug but found nothing. Try again!'
            })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Dig error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/game/deliver', methods=['POST'])
def deliver_artifacts():
    
    try:
        data = request.json
        game_id = data.get('game_id') or session.get('game_id')
        
        if not game_id:
            return jsonify({'success': False, 'error': 'No game ID'})
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        
        cursor.execute("SELECT * FROM games WHERE id = %s", (game_id,))
        game = cursor.fetchone()
        
        if not game:
            return jsonify({'success': False, 'error': 'Game not found'})
        
        
        cursor.execute("""
            SELECT pa.*, a.name as artifact_name, a.delivery_reward_money, a.delivery_reward_fuel
            FROM player_artifacts pa
            JOIN artifacts a ON pa.artifact_id = a.id
            WHERE pa.game_id = %s AND pa.delivery_airport_id = %s AND pa.status = 'FOUND'
        """, (game_id, game['current_airport_id']))
        
        artifacts_to_deliver = cursor.fetchall()
        
        if not artifacts_to_deliver:
            return jsonify({'success': False, 'error': 'No artifacts to deliver here'})
        
        total_money = 0
        total_fuel = 0
        delivered_names = []
        
        for artifact in artifacts_to_deliver:
            
            cursor.execute("""
                UPDATE player_artifacts 
                SET status = 'DELIVERED', delivered_at = NOW()
                WHERE id = %s
            """, (artifact['id'],))
            
            
            total_money += artifact['delivery_reward_money']
            total_fuel += artifact['delivery_reward_fuel']
            delivered_names.append(artifact['artifact_name'])
            
            
            cursor.execute("""
                INSERT INTO game_logs 
                (game_id, log_type, description, artifact_id, money_change, fuel_change)
                VALUES (%s, 'ARTIFACT_DELIVERED', %s, %s, %s, %s)
            """, (
                game_id,
                f"Delivered {artifact['artifact_name']}",
                artifact['artifact_id'],
                artifact['delivery_reward_money'],
                artifact['delivery_reward_fuel']
            ))
        
        
        cursor.execute("""
            UPDATE games 
            SET money = money + %s,
                fuel_km = LEAST(max_fuel_capacity, fuel_km + %s),
                artifacts_delivered = artifacts_delivered + %s
            WHERE id = %s
        """, (total_money, total_fuel, len(artifacts_to_deliver), game_id))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'delivered': len(artifacts_to_deliver),
            'money': total_money,
            'fuel': total_fuel,
            'artifacts': delivered_names
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Deliver error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/game/complete-quest', methods=['POST'])
def complete_quest():
    """Complete a quest"""
    try:
        data = request.json
        game_id = data.get('game_id') or session.get('game_id')
        quest_id = data.get('quest_id')
        
        if not game_id or not quest_id:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if quest conditions are met
        if not check_quest_completion(game_id, quest_id, cursor):
            return jsonify({'success': False, 'error': 'Quest conditions not met'})
        
        # Get quest
        cursor.execute("""
            SELECT * FROM quests 
            WHERE id = %s AND game_id = %s AND is_completed = 0 AND is_failed = 0
        """, (quest_id, game_id))
        
        quest = cursor.fetchone()
        
        if not quest:
            return jsonify({'success': False, 'error': 'Quest not found or already completed'})
        
        # Check if timed quest expired
        if quest['time_limit_minutes'] and quest['expires_at']:
            if datetime.now() > quest['expires_at']:
                cursor.execute("UPDATE quests SET is_failed = 1 WHERE id = %s", (quest_id,))
                conn.commit()
                return jsonify({'success': False, 'error': 'Quest expired'})
        
        # Apply rewards
        cursor.execute("""
            UPDATE games 
            SET money = money + %s,
                fuel_km = LEAST(max_fuel_capacity, fuel_km + %s),
                travels_remaining = travels_remaining + %s
            WHERE id = %s
        """, (quest['reward_money'], quest['reward_fuel'], quest.get('reward_travels', 0), game_id))
        
        # Mark quest as completed
        cursor.execute("UPDATE quests SET is_completed = 1 WHERE id = %s", (quest_id,))
        
        # Give clue reward if specified
        clue_result = None
        if quest['reward_clue_quality']:
            clue_result = generate_clue(game_id, cursor, quest['reward_clue_quality'])
        
        # Log completion
        cursor.execute("""
            INSERT INTO game_logs 
            (game_id, log_type, description, money_change, fuel_change, quest_id)
            VALUES (%s, 'QUEST_COMPLETED', %s, %s, %s, %s)
        """, (
            game_id,
            f"Completed quest: {quest['title']}",
            quest['reward_money'],
            quest['reward_fuel'],
            quest_id
        ))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'quest': {
                'id': quest['id'],
                'title': quest['title'],
                'rewards': {
                    'money': quest['reward_money'],
                    'fuel': quest['reward_fuel'],
                    'travels': quest.get('reward_travels', 0)
                }
            },
            'clue': clue_result
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Complete quest error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/shop/items')
def get_shop_items():
    """Get available shop items"""
    try:
        game_id = request.args.get('game_id') or session.get('game_id')
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM shop_items WHERE is_active = 1 ORDER BY price")
        items = cursor.fetchall()
        
        # Get player's purchase counts for each item
        purchase_counts = {}
        if game_id:
            cursor.execute("""
                SELECT shop_item_id, COUNT(*) as count
                FROM player_purchases
                WHERE game_id = %s
                GROUP BY shop_item_id
            """, (game_id,))
            
            for row in cursor.fetchall():
                purchase_counts[row['shop_item_id']] = row['count']
        
        # Add purchase count to each item
        for item in items:
            item['purchased_count'] = purchase_counts.get(item['id'], 0)
            item['can_purchase'] = item['purchased_count'] < item.get('max_purchases_per_game', 3)
        
        return jsonify({'success': True, 'items': items})
        
    except Exception as e:
        print(f"Get shop items error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/shop/buy', methods=['POST'])
def buy_shop_item():
    
    try:
        data = request.json
        game_id = data.get('game_id') or session.get('game_id')
        item_id = data.get('item_id')
        
        if not game_id or not item_id:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get item
        cursor.execute("SELECT * FROM shop_items WHERE id = %s AND is_active = 1", (item_id,))
        item = cursor.fetchone()
        
        if not item:
            return jsonify({'success': False, 'error': 'Item not available'})
        
        # Check purchase limit
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM player_purchases 
            WHERE game_id = %s AND shop_item_id = %s
        """, (game_id, item_id))
        
        purchase_count = cursor.fetchone()['count']
        
        if purchase_count >= item.get('max_purchases_per_game', 3):
            return jsonify({'success': False, 'error': 'Purchase limit reached for this item'})
        
        # Get player money
        cursor.execute("SELECT money FROM games WHERE id = %s", (game_id,))
        game = cursor.fetchone()
        
        if not game:
            return jsonify({'success': False, 'error': 'Game not found'})
        
        if game['money'] < item['price']:
            return jsonify({'success': False, 'error': 'Not enough money'})
        
        
        result = {'item': item}
        
        if item['category'] == 'TRAVEL':
            if item['effect_type'] == 'add_travels':
                cursor.execute("""
                    UPDATE games 
                    SET travels_remaining = travels_remaining + %s,
                        money = money - %s
                    WHERE id = %s
                """, (item['effect_value'], item['price'], game_id))
                
        elif item['category'] == 'FUEL':
            if item['effect_type'] == 'add_fuel':
                cursor.execute("""
                    UPDATE games 
                    SET fuel_km = LEAST(max_fuel_capacity, fuel_km + %s),
                        money = money - %s
                    WHERE id = %s
                """, (item['effect_value'], item['price'], game_id))
                
        elif item['category'] == 'UPGRADE':
            if item['effect_type'] == 'fuel_pass':
                cursor.execute("""
                    UPDATE games 
                    SET fuel_pass_remaining = fuel_pass_remaining + %s,
                        money = money - %s
                    WHERE id = %s
                """, (item['effect_value'], item['price'], game_id))
                
        elif item['category'] == 'POWERUP':
            if item['effect_type'] == 'clue_accuracy':
                cursor.execute("""
                    UPDATE games 
                    SET clue_accuracy_bonus = clue_accuracy_bonus + %s,
                        money = money - %s
                    WHERE id = %s
                """, (item['effect_value'], item['price'], game_id))
            elif item['effect_type'] == 'clue_reveal_chance':
                cursor.execute("""
                    UPDATE games 
                    SET clue_reveal_chance = clue_reveal_chance + %s,
                        money = money - %s
                    WHERE id = %s
                """, (item['effect_value'] / 100, item['price'], game_id))
            elif item['effect_type'] == 'marker_reveal_chance':
                cursor.execute("""
                    UPDATE games 
                    SET marker_reveal_chance = marker_reveal_chance + %s,
                        money = money - %s
                    WHERE id = %s
                """, (item['effect_value'] / 100, item['price'], game_id))
                
        elif item['category'] == 'SERVICE':
            if item['effect_type'] == 'reveal_clue':
                
                clue_result = generate_clue(game_id, cursor, 'high')
                cursor.execute("""
                    UPDATE games 
                    SET money = money - %s
                    WHERE id = %s
                """, (item['price'], game_id))
                result['clue'] = clue_result
                
            elif item['effect_type'] == 'reveal_delivery':
                
                cursor.execute("SELECT current_phase FROM games WHERE id = %s", (game_id,))
                phase = cursor.fetchone()['current_phase']
                
                if phase != 'DELIVERING_ARTIFACTS':
                    return jsonify({'success': False, 'error': 'Can only use in delivery phase'})
                
                
                cursor.execute("""
                    SELECT pa.delivery_airport_id, a.name as artifact_name
                    FROM player_artifacts pa
                    JOIN artifacts a ON pa.artifact_id = a.id
                    WHERE pa.game_id = %s AND pa.status = 'FOUND'
                    ORDER BY RAND()
                    LIMIT 1
                """, (game_id,))
                
                delivery_info = cursor.fetchone()
                
                if delivery_info:
                    cursor.execute("SELECT * FROM airports WHERE id = %s", (delivery_info['delivery_airport_id'],))
                    airport = cursor.fetchone()
                    
                    if airport:
                        
                        cursor.execute("""
                            INSERT INTO game_clues 
                            (game_id, artifact_id, target_airport_id, clue_type, clue_text, phase, quality, is_revealed)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, 1)
                        """, (
                            game_id,
                            delivery_info.get('artifact_id', 1),
                            airport['id'],
                            'EXACT_LOCATION',
                            f"Deliver {delivery_info['artifact_name']} to {airport['name']} ({airport['code']}) in {airport['city']}, {airport['country']}",
                            'DELIVERING',
                            'exact'
                        ))
                        
                        
                        cursor.execute("""
                            INSERT INTO game_logs 
                            (game_id, log_type, description)
                            VALUES (%s, 'ARTIFACT_REVEALED', %s)
                        """, (game_id, f"Revealed delivery location for {delivery_info['artifact_name']}: {airport['name']}"))
                        
                        result['marker_revealed'] = True
                        result['scan_result'] = airport
                
                cursor.execute("""
                    UPDATE games 
                    SET money = money - %s
                    WHERE id = %s
                """, (item['price'], game_id))
                
        elif item['category'] == 'LOOTBOX':
            # Random reward
            reward_type = random.choice(['money', 'fuel', 'clue', 'travel'])
            
            if reward_type == 'money':
                reward_value = random.randint(500, 2000)
                cursor.execute("""
                    UPDATE games 
                    SET money = money + %s - %s
                    WHERE id = %s
                """, (reward_value, item['price'], game_id))
                result['reward'] = {'type': 'money', 'value': reward_value}
                
            elif reward_type == 'fuel':
                reward_value = random.randint(300, 1000)
                cursor.execute("""
                    UPDATE games 
                    SET fuel_km = LEAST(max_fuel_capacity, fuel_km + %s),
                        money = money - %s
                    WHERE id = %s
                """, (reward_value, item['price'], game_id))
                result['reward'] = {'type': 'fuel', 'value': reward_value}
                
            elif reward_type == 'travel':
                reward_value = random.randint(1, 3)
                cursor.execute("""
                    UPDATE games 
                    SET travels_remaining = travels_remaining + %s,
                        money = money - %s
                    WHERE id = %s
                """, (reward_value, item['price'], game_id))
                result['reward'] = {'type': 'travel', 'value': reward_value}
                
            elif reward_type == 'clue':
                clue_result = generate_clue(game_id, cursor, random.choice(['medium', 'high']))
                cursor.execute("""
                    UPDATE games 
                    SET money = money - %s
                    WHERE id = %s
                """, (item['price'], game_id))
                result['reward'] = {'type': 'clue', 'value': clue_result}
        
        # Record purchase
        cursor.execute("""
            INSERT INTO player_purchases 
            (game_id, shop_item_id, quantity, total_price)
            VALUES (%s, %s, 1, %s)
        """, (game_id, item_id, item['price']))
        
        # Add to inventory
        cursor.execute("""
            INSERT INTO player_inventory 
            (game_id, item_type, item_name, quantity, is_active)
            VALUES (%s, %s, %s, 1, 0)
        """, (game_id, item['category'], item['name']))
        
        # Log purchase
        cursor.execute("""
            INSERT INTO game_logs 
            (game_id, log_type, description, money_change)
            VALUES (%s, 'PURCHASE', %s, %s)
        """, (game_id, f"Purchased {item['name']}", -item['price']))
        
        conn.commit()
        
        return jsonify({'success': True, **result})
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Buy item error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/inventory/use', methods=['POST'])
def use_inventory_item():
    """Use inventory item"""
    try:
        data = request.json
        game_id = data.get('game_id') or session.get('game_id')
        inventory_id = data.get('inventory_id')
        
        if not game_id or not inventory_id:
            return jsonify({'success': False, 'error': 'Missing parameters'})
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get inventory item
        cursor.execute("""
            SELECT * FROM player_inventory 
            WHERE id = %s AND game_id = %s AND quantity > 0
        """, (inventory_id, game_id))
        
        item = cursor.fetchone()
        
        if not item:
            return jsonify({'success': False, 'error': 'Item not found'})
        
        # Activate item
        cursor.execute("""
            UPDATE player_inventory 
            SET is_active = 1, remaining_uses = remaining_uses - 1
            WHERE id = %s
        """, (inventory_id,))
        
        # If no more uses, remove item
        cursor.execute("""
            UPDATE player_inventory 
            SET quantity = quantity - 1
            WHERE id = %s AND remaining_uses <= 0
        """, (inventory_id,))
        
        cursor.execute("""
            DELETE FROM player_inventory 
            WHERE id = %s AND quantity <= 0
        """, (inventory_id,))
        
        # Log usage
        cursor.execute("""
            INSERT INTO game_logs 
            (game_id, log_type, description)
            VALUES (%s, 'INVENTORY_USE', %s)
        """, (game_id, f"Used {item['item_name']} from inventory"))
        
        conn.commit()
        
        return jsonify({'success': True, 'item': item})
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Use inventory error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

@app.route('/api/game/quit', methods=['POST'])
def quit_game():
    """Quit the current game"""
    try:
        game_id = request.json.get('game_id') or session.get('game_id')
        
        if not game_id:
            return jsonify({'success': False, 'error': 'No game ID'})
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Update game status to quit
        cursor.execute("""
            UPDATE games 
            SET game_status = 'QUIT', quit_at = NOW()
            WHERE id = %s AND game_status = 'ACTIVE'
        """, (game_id,))
        
        # Log quit action
        cursor.execute("""
            INSERT INTO game_logs 
            (game_id, log_type, description)
            VALUES (%s, 'GAME_QUIT', 'Player quit the game')
        """, (game_id,))
        
        conn.commit()
        
        # Clear session
        session.pop('game_id', None)
        session.pop('player_name', None)
        
        return jsonify({'success': True, 'message': 'Game quit successfully'})
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Quit game error: {e}")
        return jsonify({'success': False, 'error': str(e)})
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)