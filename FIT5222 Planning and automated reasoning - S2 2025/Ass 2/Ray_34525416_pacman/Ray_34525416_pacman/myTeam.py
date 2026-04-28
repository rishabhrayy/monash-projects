# myTeam.py
# ---------
# FIT5222 Assignment - Pacman Capture the Flag
# 
# This module implements a multi-agent Pacman team using:
# - PDDL-based high-level strategic planning
# - A* search for optimal pathfinding
# - Particle filters for probabilistic opponent tracking
# - Dynamic risk assessment and adaptive behavior
#
# Team Strategy:
# - Offensive Agent: Aggressive food collection with capsule exploitation
# - Defensive Agent: Intelligent patrol based on food density clusters
#
# Author: [Your Name]
# Student ID: [Your ID]
# Date: 2025

import random
import time
import os
import util
from captureAgents import CaptureAgent
from game import Directions, Actions
from util import nearestPoint

#################
# Team Creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='OffensiveAgent', second='DefensiveAgent'):
    """
    Creates a team of two agents for Pacman Capture the Flag.
    
    Args:
        firstIndex (int): Index of the first agent
        secondIndex (int): Index of the second agent
        isRed (bool): True if agents are on the red team
        first (str): Class name for the first agent (offensive)
        second (str): Class name for the second agent (defensive)
    
    Returns:
        list: Two initialized agent objects
    """
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

# --------------------------------------------------------------------------------------
# PDDL PLANNER INTEGRATION
# --------------------------------------------------------------------------------------

class PDDLPlanner:
    """
    PDDL-style strategic planner that converts game state into predicates
    and evaluates which high-level actions are applicable.
    
    This provides declarative, rule-based decision making at the strategic level,
    while A* handles tactical path planning at the operational level.
    """
    
    @staticmethod
    def get_world_state(gameState, agent):
        """
        Converts the current game state into PDDL-style predicates.
        
        Args:
            gameState: Current Pacman game state
            agent: The agent performing the reasoning
        
        Returns:
            set: Set of predicate strings representing the world state
        """
        predicates = set()
        
        my_state = gameState.getAgentState(agent.index)
        my_pos = my_state.getPosition()
        
        # World state predicates
        food_list = agent.getFood(gameState).asList()
        if len(food_list) > 0:
            predicates.add('food_available')
            
        capsules = agent.getCapsules(gameState)
        if len(capsules) > 0:
            predicates.add('power_capsule_available')
        
        # Check if territory is secure (no enemy Pacmen in our territory)
        opponents = agent.getOpponents(gameState)
        enemy_pacmen = [gameState.getAgentState(i) for i in opponents if gameState.getAgentState(i).isPacman]
        if len(enemy_pacmen) == 0:
            predicates.add('territory_secure')
        
        # Agent state predicates
        if my_state.isPacman:
            predicates.add('is_pacman')
        
        if not agent.is_on_home_side(my_pos, gameState):
            predicates.add('in_enemy_territory')
        else:
            predicates.add('at_home')
            
        if my_state.numCarrying > 0:
            predicates.add('food_in_backpack')
            
        if my_state.numCarrying >= 5:  # Threshold for "significant food"
            predicates.add('carrying_significant_food')
        
        # Check if agent has active power-up (enemies are scared)
        enemies_scared = False
        for opp_idx in opponents:
            opp_state = gameState.getAgentState(opp_idx)
            if opp_state.scaredTimer > 0:
                enemies_scared = True
                predicates.add(f'enemy_scared_{opp_idx}')
        
        if enemies_scared:
            predicates.add('power_mode_active')
        
        # Enemy predicates
        for opp_idx in opponents:
            opp_state = gameState.getAgentState(opp_idx)
            opp_pos = opp_state.getPosition()
            
            if opp_state.isPacman:
                predicates.add(f'enemy_is_pacman_{opp_idx}')
                
            if opp_pos and agent.getMazeDistance(my_pos, opp_pos) <= 5:
                predicates.add(f'enemy_near_{opp_idx}')
        
        # Check if being chased (only matters if enemies aren't scared)
        if not enemies_scared:
            danger_level = agent.assess_danger(gameState)
            if danger_level > 50:
                predicates.add('being_chased')
            
        return predicates
    
    @staticmethod
    def evaluate_actions(predicates, agent_role):
        """
        Evaluates which PDDL actions are applicable given current predicates
        and returns the highest priority action.
        
        Args:
            predicates (set): Current world state predicates
            agent_role (str): 'offensive' or 'defensive'
        
        Returns:
            tuple: (action_name, priority_score)
        """
        applicable_actions = []
        
        if agent_role == 'offensive':
            # POWER MODE: Greedy food collection (Highest Priority)
            if ('power_mode_active' in predicates and 
                'food_available' in predicates and
                'is_pacman' in predicates):
                applicable_actions.append(('power_mode_attack', 150))
            
            # Strategic Retreat (High Priority when in danger)
            if ('is_pacman' in predicates and 
                'carrying_significant_food' in predicates and
                'being_chased' in predicates and
                'power_mode_active' not in predicates):
                applicable_actions.append(('strategic_retreat', 100))
            
            # Strategic Retreat (Moderate Priority when carrying food safely)
            elif ('is_pacman' in predicates and 
                  'carrying_significant_food' in predicates):
                applicable_actions.append(('strategic_retreat', 80))
            
            # Secure Power Capsule (Opportunistic)
            if ('power_capsule_available' in predicates and 
                'at_home' in predicates):
                applicable_actions.append(('secure_power_capsule', 70))
            
            # Aggressive Attack (When safe and no power mode)
            if ('food_available' in predicates and 
                'territory_secure' in predicates and
                'being_chased' not in predicates and
                'power_mode_active' not in predicates):
                applicable_actions.append(('aggressive_attack', 60))
            
            # Cautious Attack (Default when power mode not active)
            if 'food_available' in predicates and 'power_mode_active' not in predicates:
                applicable_actions.append(('cautious_attack', 40))
        
        elif agent_role == 'defensive':
            # Intercept Invader (Highest Priority)
            has_invader = any('enemy_is_pacman' in p for p in predicates)
            if has_invader and 'at_home' in predicates:
                applicable_actions.append(('intercept_invader', 100))
            
            # Cooperative Intercept (if teammate also defending)
            if has_invader:
                applicable_actions.append(('cooperative_intercept', 90))
            
            # Patrol Chokepoints (Default)
            if 'at_home' in predicates and 'territory_secure' in predicates:
                applicable_actions.append(('patrol_chokepoints', 50))
            
            # Active Defense (when territory not secure)
            if 'at_home' in predicates and 'territory_secure' not in predicates:
                applicable_actions.append(('active_defense', 70))
        
        if not applicable_actions:
            return ('default_behavior', 0)
        
        # Return the action with highest priority
        return max(applicable_actions, key=lambda x: x[1])

# --------------------------------------------------------------------------------------
# PARTICLE FILTER CLASS FOR ENEMY TRACKING (OPTIMIZED)
# --------------------------------------------------------------------------------------

class ParticleFilter:
    """
    Optimized particle filter for tracking opponent positions probabilistically.
    
    Uses 250 particles (reduced from 500 for efficiency) with diversity monitoring
    to prevent particle deprivation. Implements Bayesian filtering with noisy
    distance observations.
    
    Attributes:
        agent_index (int): Index of the agent using this filter
        num_particles (int): Number of particles (250)
        legal_positions (list): All legal board positions
        particles (list): Current particle distribution
    """
    
    def __init__(self, agent_index, num_particles, legal_positions):
        """
        Initialize particle filter with uniform distribution.
        
        Args:
            agent_index (int): Index of the agent using this filter
            num_particles (int): Number of particles to maintain
            legal_positions (list): All legal board positions
        """
        self.agent_index = agent_index
        self.num_particles = num_particles
        self.legal_positions = legal_positions
        self.particles = None
        self.initialize_particles()

    def initialize_particles(self):
        """Initialize particles uniformly across all legal positions."""
        self.particles = random.choices(self.legal_positions, k=self.num_particles)

    def observe(self, noisy_distance, gameState):
        """
        Update beliefs based on noisy distance observation using Bayesian filtering.
        Includes diversity check to prevent particle deprivation.
        
        Args:
            noisy_distance (int): Noisy Manhattan distance to opponent
            gameState: Current game state
        """
        if not self.particles:
            return
        
        my_pos = gameState.getAgentPosition(self.agent_index)
        weights = util.Counter()
        
        # Calculate weight for each particle based on observation likelihood
        for p in self.particles:
            true_distance = util.manhattanDistance(my_pos, p)
            weights[p] += gameState.getDistanceProb(true_distance, noisy_distance)
            
        if weights.totalCount() == 0:
            self.initialize_particles()
            return
        
        # Check diversity before resampling to prevent particle deprivation
        unique_positions = len(set(self.particles))
        diversity_ratio = unique_positions / self.num_particles
        
        # If diversity is too low, inject random particles
        if diversity_ratio < 0.1:  # Less than 10% diversity
            num_random = int(self.num_particles * 0.2)  # Add 20% random particles
            random_particles = random.choices(self.legal_positions, k=num_random)
            self.particles = random.choices(list(weights.keys()), 
                                          weights=list(weights.values()), 
                                          k=self.num_particles - num_random) + random_particles
        else:
            # Normal resampling based on weights
            self.particles = random.choices(list(weights.keys()), 
                                          weights=list(weights.values()), 
                                          k=self.num_particles)

    def elapse_time(self, walls):
        """
        Predict next particle positions by simulating random movement.
        
        Args:
            walls: Wall configuration of the game board
        """
        if not self.particles:
            return
        
        new_particles = []
        for p in self.particles:
            # Each particle can stay or move to adjacent position
            possible_positions = [p] + Actions.getLegalNeighbors(p, walls)
            new_particles.append(random.choice(possible_positions))
        self.particles = new_particles

    def get_belief_distribution(self):
        """
        Returns normalized probability distribution over enemy positions.
        
        Returns:
            Counter: Belief distribution (position -> probability)
        """
        belief = util.Counter()
        for p in self.particles:
            belief[p] += 1
        belief.normalize()
        return belief
    
    def get_most_likely_position(self):
        """
        Returns the most likely position of the enemy.
        
        Returns:
            tuple: Most likely (x, y) position or None
        """
        if not self.particles:
            return None
        belief = self.get_belief_distribution()
        return belief.argMax()

# --------------------------------------------------------------------------------------
# BASE AGENT CLASS
# --------------------------------------------------------------------------------------

class BaseAgent(CaptureAgent):
    """
    Base agent class implementing the core architecture:
    
    1. PDDL-based high-level strategic planning
    2. A* search for low-level pathfinding with risk-adjusted costs
    3. Particle filters for probabilistic enemy tracking
    4. Dynamic risk assessment based on game phase
    5. Team coordination via shared blackboard
    
    This class provides common functionality for both offensive and defensive agents.
    Subclasses must implement get_role() and execute_strategic_action().
    """
    
    # Shared blackboard for team coordination
    BLACKBOARD = {}

    def registerInitialState(self, gameState):
        """
        Initialize agent at game start. Sets up particle filters, risk thresholds,
        and team coordination structures.
        
        Args:
            gameState: Initial game state
        """
        super().registerInitialState(gameState)
        
        # General agent setup
        self.start_position = gameState.getAgentPosition(self.index)
        self.legal_positions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
        
        # Enemy tracking setup (OPTIMIZED: 250 particles instead of 500)
        self.num_particles = 250
        self.enemy_trackers = {}
        for opponent_index in self.getOpponents(gameState):
            self.enemy_trackers[opponent_index] = ParticleFilter(
                self.index, self.num_particles, self.legal_positions
            )
            
        # Team Coordination Setup with cleanup mechanisms
        if 'claimed_food' not in BaseAgent.BLACKBOARD:
            BaseAgent.BLACKBOARD['claimed_food'] = {}
        if 'claim_timestamps' not in BaseAgent.BLACKBOARD:
            BaseAgent.BLACKBOARD['claim_timestamps'] = {}
        if 'game_phase' not in BaseAgent.BLACKBOARD:
            BaseAgent.BLACKBOARD['game_phase'] = 'early'
        if 'turn_count' not in BaseAgent.BLACKBOARD:
            BaseAgent.BLACKBOARD['turn_count'] = 0
            
        # Dynamic risk thresholds that adapt to game phase
        self.risk_thresholds = {
            'early': {'escape_carrying': 8, 'danger_threshold': 30},
            'mid': {'escape_carrying': 5, 'danger_threshold': 40},
            'late': {'escape_carrying': 3, 'danger_threshold': 50}
        }

    def chooseAction(self, gameState):
        """
        Main decision-making loop. Integrates PDDL planning, particle filtering,
        and A* pathfinding to select optimal action.
        
        Process:
        1. Update game phase and cleanup stale data
        2. Update enemy position beliefs (particle filters)
        3. PDDL high-level planning (strategic action selection)
        4. Execute strategic action (goal selection)
        5. A* low-level planning (path to goal)
        6. Return first action in path
        
        Args:
            gameState: Current game state
        
        Returns:
            Direction: Action to take (North, South, East, West, or Stop)
        """
        # Step 0: Update game phase and cleanup
        self.update_game_phase(gameState)
        self.cleanup_food_claims()
        
        # Step 1: Update Beliefs (Particle Filters)
        self.update_enemy_beliefs(gameState)
        
        # Step 2: PDDL High-Level Planning
        predicates = PDDLPlanner.get_world_state(gameState, self)
        strategic_action, priority = PDDLPlanner.evaluate_actions(predicates, self.get_role())
        
        # Step 3: Execute Strategic Action (Goal Selection)
        target_position = self.execute_strategic_action(strategic_action, gameState)

        # Step 4: Compute Low-Level Plan (A* Path)
        actions = self.get_low_level_plan_astar(gameState, target_position)
        
        # Step 5: Execute Move
        action = Directions.STOP
        if actions and len(actions) > 0:
            action = actions[0]
            
        # Update blackboard with current action/intent for team coordination
        BaseAgent.BLACKBOARD[self.index] = {
            'action': action, 
            'target': target_position,
            'strategic_action': strategic_action
        }
        
        return action
    
    def update_game_phase(self, gameState):
        """
        Update the game phase based on turn count and food remaining.
        Phases: early (exploration), mid (aggressive), late (conservative).
        
        Args:
            gameState: Current game state
        """
        BaseAgent.BLACKBOARD['turn_count'] += 1
        turn = BaseAgent.BLACKBOARD['turn_count']
        
        food_remaining = len(self.getFood(gameState).asList())
        total_food = len(self.getFood(gameState).asList()) + gameState.getAgentState(self.index).numCarrying
        
        # Phase determination based on turns and food percentage
        if turn < 100 or (total_food > 0 and food_remaining > total_food * 0.6):
            BaseAgent.BLACKBOARD['game_phase'] = 'early'
        elif turn < 250 or (total_food > 0 and food_remaining > total_food * 0.3):
            BaseAgent.BLACKBOARD['game_phase'] = 'mid'
        else:
            BaseAgent.BLACKBOARD['game_phase'] = 'late'
    
    def cleanup_food_claims(self):
        """
        Remove stale food claims (older than 10 turns) to prevent memory leaks
        and ensure dynamic coordination.
        """
        current_turn = BaseAgent.BLACKBOARD.get('turn_count', 0)
        claims = BaseAgent.BLACKBOARD.get('claimed_food', {})
        timestamps = BaseAgent.BLACKBOARD.get('claim_timestamps', {})
        
        # Find and remove claims older than 10 turns
        stale_claims = [food for food, turn in timestamps.items() 
                       if current_turn - turn > 10]
        
        for food in stale_claims:
            if food in claims:
                del claims[food]
            del timestamps[food]

    def is_on_home_side(self, pos, gameState):
        """
        Check if a position is on our home territory.
        
        Args:
            pos (tuple): (x, y) position
            gameState: Current game state
        
        Returns:
            bool: True if position is on home side
        """
        mid_x = gameState.data.layout.width // 2
        if self.red:
            return pos[0] < mid_x
        else:
            return pos[0] >= mid_x

    def update_enemy_beliefs(self, gameState):
        """
        Update particle filters for all opponents. Uses exact positions when
        visible, particle filter prediction for hidden enemies.
        
        Args:
            gameState: Current game state
        """
        noisy_distances = gameState.getAgentDistances()
        for opponent_index in self.getOpponents(gameState):
            tracker = self.enemy_trackers[opponent_index]
            
            # Use exact position from game state when enemy is visible
            opponent_pos = gameState.getAgentPosition(opponent_index)
            if opponent_pos is not None:
                # Enemy is visible - reset particles to exact position
                tracker.particles = [opponent_pos] * self.num_particles
            else:
                # Enemy is hidden - use particle filter
                tracker.elapse_time(gameState.getWalls())
                tracker.observe(noisy_distances[opponent_index], gameState)
    
    def get_role(self):
        """
        Returns the agent's role. Must be overridden by subclasses.
        
        Returns:
            str: 'offensive' or 'defensive'
        """
        util.raiseNotDefined()
    
    def execute_strategic_action(self, action_name, gameState):
        """
        Translates a PDDL strategic action into a concrete goal position.
        Must be overridden by subclasses.
        
        Args:
            action_name (str): PDDL action name
            gameState: Current game state
        
        Returns:
            tuple: Target (x, y) position
        """
        util.raiseNotDefined()

    def assess_danger(self, gameState):
        """
        Assesses current danger level based on visible and hidden enemies.
        Uses exact positions when available, particle filter estimates otherwise.
        
        Args:
            gameState: Current game state
        
        Returns:
            int: Danger score (0-100+), higher = more dangerous
        """
        my_pos = gameState.getAgentPosition(self.index)
        danger_score = 0
        
        # Check all opponents for threats
        for opponent_index in self.getOpponents(gameState):
            opponent = gameState.getAgentState(opponent_index)
            opponent_pos = gameState.getAgentPosition(opponent_index)
            
            # Only consider danger from ghosts (not enemy Pacmen)
            if not opponent.isPacman:
                if opponent_pos is not None:
                    # Enemy is VISIBLE - use exact position with high confidence
                    dist = self.getMazeDistance(my_pos, opponent_pos)
                    if opponent.scaredTimer < 5:  # Only fear non-scared ghosts
                        if dist <= 1: danger_score += 100
                        elif dist <= 2: danger_score += 50
                        elif dist <= 3: danger_score += 20
                        elif dist <= 5: danger_score += 10
                else:
                    # Enemy is HIDDEN - use particle filter with lower confidence
                    most_likely_pos = self.enemy_trackers[opponent_index].get_most_likely_position()
                    if most_likely_pos:
                        dist = self.getMazeDistance(my_pos, most_likely_pos)
                        if dist <= 3:
                            danger_score += 15  # Lower penalty due to uncertainty
        
        return danger_score

    def get_low_level_plan_astar(self, gameState, goal_pos):
        """
        Computes optimal path using A* search with dynamic risk-adjusted costs.
        
        Cost function balances:
        - Base movement cost (1 per step)
        - Risk penalty from nearby ghosts (dynamic based on game phase)
        - Heuristic (maze distance to goal)
        
        Args:
            gameState: Current game state
            goal_pos (tuple): Target (x, y) position
        
        Returns:
            list: Sequence of Directions to reach goal
        """
        if goal_pos is None:
            return [Directions.STOP]

        start_pos = gameState.getAgentPosition(self.index)
        
        # A* Search Implementation
        frontier = util.PriorityQueue()
        start_node = (start_pos, [], 0)  # (position, path, cost)
        frontier.push(start_node, 0)
        
        visited = set()
        
        while not frontier.isEmpty():
            current_pos, path, current_cost = frontier.pop()
            
            # Goal test
            if current_pos == goal_pos:
                return path
            
            if current_pos in visited:
                continue
            
            visited.add(current_pos)
            
            # Expand successors
            successors = Actions.getLegalNeighbors(current_pos, gameState.getWalls())
            for next_pos in successors:
                action = Actions.vectorToDirection(
                    (next_pos[0] - current_pos[0], next_pos[1] - current_pos[1])
                )
                new_path = path + [action]
                
                # Dynamic risk-adjusted cost
                risk_penalty = self.get_risk_penalty(next_pos, gameState)
                step_cost = 1 + risk_penalty
                new_cost = current_cost + step_cost
                
                # Heuristic: Maze distance to goal
                heuristic = self.getMazeDistance(next_pos, goal_pos)
                
                priority = new_cost + heuristic
                frontier.push((next_pos, new_path, new_cost), priority)
        
        # No path found
        return [Directions.STOP]

    def get_risk_penalty(self, position, gameState):
        """
        Calculates risk penalty for a position based on proximity to ghosts.
        Uses dynamic thresholds based on game phase. Prioritizes exact
        enemy positions when available.
        
        Args:
            position (tuple): Position to evaluate
            gameState: Current game state
        
        Returns:
            float: Risk penalty to add to path cost
        """
        phase = BaseAgent.BLACKBOARD.get('game_phase', 'early')
        danger_threshold = self.risk_thresholds[phase]['danger_threshold']
        
        penalty = 0
        
        # Check all opponents for risk
        for opponent_index in self.getOpponents(gameState):
            opponent = gameState.getAgentState(opponent_index)
            opponent_pos = gameState.getAgentPosition(opponent_index)
            
            # Only ghosts are dangerous (not enemy Pacmen)
            if not opponent.isPacman:
                if opponent_pos is not None:
                    # Enemy is VISIBLE - use exact position with high penalty
                    dist = self.getMazeDistance(position, opponent_pos)
                    if opponent.scaredTimer < 5:  # Only fear non-scared ghosts
                        if dist <= 1: penalty += 1000  # Critical danger
                        elif dist <= 2: penalty += 200  # High danger
                        elif dist <= 3: penalty += 50   # Moderate danger
                        elif dist <= 5: penalty += 10   # Low danger
                else:
                    # Enemy is HIDDEN - use particle filter with lower penalty
                    most_likely_pos = self.enemy_trackers[opponent_index].get_most_likely_position()
                    if most_likely_pos:
                        dist = self.getMazeDistance(position, most_likely_pos)
                        if dist <= 2:
                            penalty += 20  # Reduced due to uncertainty
                        elif dist <= 3:
                            penalty += 10
        
        return penalty

# --------------------------------------------------------------------------------------
# SPECIALIZED AGENT CLASSES
# --------------------------------------------------------------------------------------

class OffensiveAgent(BaseAgent):
    """
    Offensive agent specialized in food collection and scoring.
    
    Strategy:
    - Exploits power capsules for greedy food collection
    - Ignores ghosts during power mode to maximize food gathering
    - Returns home when carrying significant food or in danger
    - Uses dynamic risk assessment for safe navigation
    - Coordinates with teammate to avoid targeting same food
    
    Key Features:
    - Power mode exploitation (capsule-based aggression)
    - Strategic retreat based on food carried and danger
    - Team coordination via food claiming mechanism
    """
    
    def get_role(self):
        """Return agent role for PDDL planning."""
        return 'offensive'
    
    def execute_strategic_action(self, action_name, gameState):
        """
        Translates PDDL strategic actions into concrete goals for offensive agent.
        
        Actions:
        - power_mode_attack: Greedy food collection while enemies are scared
        - strategic_retreat: Return home with collected food
        - secure_power_capsule: Go get power capsule
        - aggressive_attack/cautious_attack: Normal food collection
        
        Args:
            action_name (str): PDDL action name
            gameState: Current game state
        
        Returns:
            tuple: Target (x, y) position
        """
        my_state = gameState.getAgentState(self.index)
        my_pos = my_state.getPosition()
        
        # POWER MODE: Greedy food collection (ignore ghosts, eat everything)
        if action_name == 'power_mode_attack':
            food_list = self.getFood(gameState).asList()
            if food_list:
                # Check if any enemies are still scared
                enemies_scared = False
                min_scared_time = float('inf')
                for opp_idx in self.getOpponents(gameState):
                    opp_state = gameState.getAgentState(opp_idx)
                    if opp_state.scaredTimer > 0:
                        enemies_scared = True
                        min_scared_time = min(min_scared_time, opp_state.scaredTimer)
                
                if enemies_scared:
                    # GREEDY MODE: Get closest food, ignore all risk
                    closest_food = min(food_list, 
                                     key=lambda f: self.getMazeDistance(my_pos, f))
                    return closest_food
        
        # Strategic Retreat: Return home safely
        if action_name == 'strategic_retreat':
            # Find safest entry point to home territory
            home_positions = [p for p in self.legal_positions 
                            if self.is_on_home_side(p, gameState)]
            if home_positions:
                mid_x = gameState.data.layout.width // 2
                boundary_x = mid_x - 1 if self.red else mid_x
                boundary_positions = [p for p in home_positions if p[0] == boundary_x]
                
                if boundary_positions:
                    # Return to closest safe boundary position
                    return min(boundary_positions, 
                             key=lambda p: self.getMazeDistance(my_pos, p) + 
                                          self.get_risk_penalty(p, gameState))
                
                # Fallback: any home position
                return min(home_positions, 
                         key=lambda p: self.get_risk_penalty(p, gameState))
        
        # Secure Power Capsule: Go get capsule for power mode
        elif action_name == 'secure_power_capsule':
            capsules = self.getCapsules(gameState)
            if capsules:
                return min(capsules, key=lambda c: self.getMazeDistance(my_pos, c))
        
        # Aggressive/Cautious Attack: Normal food collection
        elif action_name in ['aggressive_attack', 'cautious_attack']:
            food_list = self.getFood(gameState).asList()
            if food_list:
                # Team Coordination: Avoid claiming same food as teammate
                claims = BaseAgent.BLACKBOARD.get('claimed_food', {})
                timestamps = BaseAgent.BLACKBOARD.get('claim_timestamps', {})
                current_turn = BaseAgent.BLACKBOARD.get('turn_count', 0)
                
                # Remove our old claims
                old_claims = [f for f, agent in claims.items() if agent == self.index]
                for f in old_claims:
                    del claims[f]
                    if f in timestamps:
                        del timestamps[f]
                
                # Find unclaimed food
                unclaimed_food = [f for f in food_list if f not in claims]
                if not unclaimed_food:
                    unclaimed_food = food_list  # All claimed, ignore claims
                
                # Select best food (balance distance and safety)
                risk_weight = 2 if action_name == 'cautious_attack' else 5
                best_food = min(unclaimed_food, 
                              key=lambda f: self.getMazeDistance(my_pos, f) + 
                                           self.get_risk_penalty(f, gameState) * risk_weight)
                
                # Claim this food for coordination
                claims[best_food] = self.index
                timestamps[best_food] = current_turn
                
                return best_food
        
        # Default: return home
        return self.start_position

class DefensiveAgent(BaseAgent):
    """
    Defensive agent specialized in territory protection and invader interception.
    
    Strategy:
    - Intelligent patrol based on food density clusters
    - Guards high-value food clusters and entrance chokepoints
    - Time-boxed pursuit to prevent overcommitment
    - Dynamic zone recalculation as food distribution changes
    - Real-time adaptation to food loss and threats
    
    Key Features:
    - Food clustering algorithm for strategic positioning
    - Multi-factor patrol zone scoring (recency, distance, priority, threats)
    - Entrance points weighted 2x higher to prevent incursions
    - Pursuit timeout (10 turns) to maintain territory coverage
    - Automatic zone updates when food is eaten
    """
    
    def registerInitialState(self, gameState):
        """
        Initialize defensive agent with patrol zones and tracking.
        
        Sets up:
        - Food cluster detection and patrol zones
        - Visit history for dynamic patrol
        - Pursuit tracking for time-boxed chasing
        
        Args:
            gameState: Initial game state
        """
        super().registerInitialState(gameState)
        
        # Food cluster and patrol zone setup
        self.patrol_zones = []  # List of (type, position, priority)
        self.last_visited = {}  # Track when each zone was last visited
        self.patrol_target = None
        self.initialize_patrol_zones(gameState)
        
        # Pursuit tracking for time-boxed pursuit (Challenge 2)
        self.pursuing_enemy = None
        self.pursuit_start_turn = None
        self.max_pursuit_turns = 10  # Maximum turns to chase before returning
        
    def initialize_patrol_zones(self, gameState):
        """
        Initialize patrol zones based on food clusters and entrance points.
        
        Challenge 1 Solution: Prioritize top 3 food clusters + main entrance only
        Challenge 3 Solution: Weight entrance points 2x higher
        
        Process:
        1. Cluster defending food into groups
        2. Select top 3 largest clusters
        3. Calculate cluster centers as patrol points
        4. Identify best entrance points by visibility
        5. Add entrance points with 2x priority weight
        
        Args:
            gameState: Current game state
        """
        food_defending = self.getFoodYouAreDefending(gameState).asList()
        
        # Step 1: Cluster food positions (radius = 5 steps)
        food_clusters = self.cluster_food_positions(food_defending, gameState, cluster_radius=5)
        
        # Step 2: Get top 3 food clusters by size (Challenge 1: Limit territory coverage)
        top_clusters = food_clusters[:3] if len(food_clusters) >= 3 else food_clusters
        
        # Step 3: Add food cluster centers as patrol zones
        for cluster in top_clusters:
            center = self.get_cluster_center(cluster, gameState)
            priority = len(cluster) * 3  # Priority proportional to food density
            self.patrol_zones.append(('food_cluster', center, priority))
        
        # Step 4: Get boundary entrance points
        mid_x = gameState.data.layout.width // 2
        boundary_x = mid_x - 1 if self.red else mid_x
        boundary_points = [p for p in self.legal_positions if p[0] == boundary_x]
        
        # Step 5: Select main entrance points with best visibility
        entrance_candidates = []
        for pos in boundary_points:
            visibility = self.get_visibility_score(pos, gameState)
            entrance_candidates.append((pos, visibility))
        
        # Sort by visibility and take top positions
        entrance_candidates.sort(key=lambda x: x[1], reverse=True)
        num_entrances = min(5, len(entrance_candidates))
        
        # Step 6: Add entrance points with 2x weight (Challenge 3: Prioritize entrances)
        for pos, visibility in entrance_candidates[:num_entrances]:
            priority = 20  # Base entrance priority (2x higher than avg food cluster of ~10)
            self.patrol_zones.append(('entrance', pos, priority))
        
        # Initialize visit history
        current_turn = BaseAgent.BLACKBOARD.get('turn_count', 0)
        for zone_type, pos, priority in self.patrol_zones:
            self.last_visited[pos] = current_turn - 100  # Mark as not visited recently
    
    def cluster_food_positions(self, food_list, gameState, cluster_radius=5):
        """
        Groups nearby food into clusters using distance-based clustering (BFS).
        
        Algorithm:
        1. For each unvisited food, start a new cluster
        2. Use BFS to find all food within cluster_radius
        3. Add them to the current cluster
        4. Sort clusters by size (largest first)
        
        Args:
            food_list (list): List of food positions to cluster
            gameState: Current game state
            cluster_radius (int): Maximum distance for food to be in same cluster
        
        Returns:
            list: List of clusters, where each cluster is a list of positions
                  Sorted by cluster size (descending)
        """
        if not food_list:
            return []
        
        clusters = []
        visited = set()
        
        for food in food_list:
            if food in visited:
                continue
            
            # Start new cluster with BFS
            cluster = [food]
            visited.add(food)
            
            # BFS to find all nearby food
            queue = [food]
            while queue:
                current = queue.pop(0)
                for other_food in food_list:
                    if other_food not in visited:
                        dist = self.getMazeDistance(current, other_food)
                        if dist <= cluster_radius:
                            cluster.append(other_food)
                            visited.add(other_food)
                            queue.append(other_food)
            
            clusters.append(cluster)
        
        # Sort clusters by size (largest = most important)
        clusters.sort(key=len, reverse=True)
        return clusters
    
    def get_cluster_center(self, cluster, gameState):
        """
        Find the best central position for a food cluster.
        Uses the position with minimum total distance to all food in cluster.
        
        Args:
            cluster (list): List of food positions in the cluster
            gameState: Current game state
        
        Returns:
            tuple: Best central (x, y) position
        """
        if not cluster:
            return self.start_position
        
        best_pos = cluster[0]
        min_total_dist = float('inf')
        
        # Check each food position as potential center
        for candidate in cluster:
            total_dist = sum(self.getMazeDistance(candidate, food) for food in cluster)
            if total_dist < min_total_dist:
                min_total_dist = total_dist
                best_pos = candidate
        
        return best_pos
    
    def get_visibility_score(self, position, gameState):
        """
        Calculate visibility score for a position (number of visible positions).
        Higher score = better vantage point for early enemy detection.
        
        Args:
            position (tuple): Position to evaluate
            gameState: Current game state
        
        Returns:
            int: Number of positions visible from this location
        """
        visible_count = 0
        walls = gameState.getWalls()
        
        # Check positions within vision range (5 steps)
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                check_pos = (position[0] + dx, position[1] + dy)
                
                # Check if position is legal
                if (0 <= check_pos[0] < walls.width and 
                    0 <= check_pos[1] < walls.height and
                    not walls[check_pos[0]][check_pos[1]]):
                    
                    # Simple visibility: Manhattan distance <= 5
                    if abs(dx) + abs(dy) <= 5:
                        visible_count += 1
        
        return visible_count
        
    def get_role(self):
        """Return agent role for PDDL planning."""
        return 'defensive'
    
    def execute_strategic_action(self, action_name, gameState):
        """
        Translates PDDL strategic actions into concrete goals for defensive agent.
        Enhanced with food-density awareness and time-boxed pursuit.
        
        Actions:
        - intercept_invader/cooperative_intercept/active_defense: Chase enemies
        - patrol_chokepoints: Intelligent patrol of food clusters and entrances
        
        Challenge 2 Solution: Time-boxed pursuit (10 turn maximum)
        
        Args:
            action_name (str): PDDL action name
            gameState: Current game state
        
        Returns:
            tuple: Target (x, y) position
        """
        my_pos = gameState.getAgentPosition(self.index)
        current_turn = BaseAgent.BLACKBOARD.get('turn_count', 0)
        
        if action_name in ['intercept_invader', 'cooperative_intercept', 'active_defense']:
            # Find invaders in our territory
            invaders = [a for a in self.getOpponents(gameState) 
                       if gameState.getAgentState(a).isPacman]
            
            if invaders:
                # Prioritize visible invaders using exact game state positions
                invader_positions = []
                for i in invaders:
                    inv_pos = gameState.getAgentPosition(i)
                    if inv_pos is not None:
                        invader_positions.append((i, inv_pos))
                
                if invader_positions:
                    # Challenge 2: Time-box pursuit to prevent overcommitment
                    if self.pursuing_enemy is not None:
                        # Check if pursuit has exceeded time limit
                        turns_pursuing = current_turn - self.pursuit_start_turn
                        if turns_pursuing > self.max_pursuit_turns:
                            # Timeout - abandon chase, return to patrol
                            self.pursuing_enemy = None
                            self.pursuit_start_turn = None
                            return self.get_patrol_target(my_pos, gameState)
                    
                    # Start or continue pursuit of closest invader
                    closest_invader = min(invader_positions, 
                                        key=lambda x: self.getMazeDistance(my_pos, x[1]))
                    
                    # Update pursuit tracking
                    if self.pursuing_enemy != closest_invader[0]:
                        self.pursuing_enemy = closest_invader[0]
                        self.pursuit_start_turn = current_turn
                    
                    return closest_invader[1]
                
                # If no visible invaders but we know they exist (hidden),
                # use particle filter as backup
                for inv_idx in invaders:
                    if gameState.getAgentPosition(inv_idx) is None:
                        likely_pos = self.enemy_trackers[inv_idx].get_most_likely_position()
                        if likely_pos:
                            # Start pursuit of hidden enemy
                            if self.pursuing_enemy is None:
                                self.pursuing_enemy = inv_idx
                                self.pursuit_start_turn = current_turn
                            return likely_pos
            else:
                # No invaders - reset pursuit tracking
                self.pursuing_enemy = None
                self.pursuit_start_turn = None
            
            # Check if food was just eaten (investigate recent threat location)
            last_eaten = self.get_last_eaten_food(gameState)
            if last_eaten:
                return last_eaten
        
        elif action_name == 'patrol_chokepoints':
            # No active threats - do intelligent patrol
            # Reset pursuit tracking
            self.pursuing_enemy = None
            self.pursuit_start_turn = None
            
            # Get dynamic patrol target based on food clusters and entrances
            return self.get_patrol_target(my_pos, gameState)
        
        # Default: return to start
        return self.start_position
    
    def get_patrol_target(self, my_pos, gameState):
        """
        Choose next patrol point using multi-factor scoring system.
        
        Scoring Factors:
        1. Recency: Zones not visited recently get higher scores
        2. Distance: Closer positions slightly preferred
        3. Priority: Food density and entrance importance (Challenge 3: entrances 2x)
        4. Teammate: Avoid clustering with teammate
        5. Threats: Boost priority for areas where food was recently eaten
        
        Args:
            my_pos (tuple): Current agent position
            gameState: Current game state
        
        Returns:
            tuple: Target (x, y) patrol position
        """
        current_turn = BaseAgent.BLACKBOARD.get('turn_count', 0)
        
        # Check if we've reached our current patrol target
        if self.patrol_target and my_pos == self.patrol_target:
            # Mark as visited
            self.last_visited[self.patrol_target] = current_turn
            self.patrol_target = None
        
        # If we don't have a target, select the best one
        if self.patrol_target is None:
            best_zone = None
            best_score = -float('inf')
            
            for zone_type, position, base_priority in self.patrol_zones:
                score = 0
                
                # Factor 1: Recency (zones not visited recently = higher score)
                time_since_visit = current_turn - self.last_visited.get(position, 0)
                score += time_since_visit * 2
                
                # Factor 2: Distance (closer positions slightly preferred)
                distance = self.getMazeDistance(my_pos, position)
                score -= distance * 0.5
                
                # Factor 3: Priority (food density or entrance importance)
                # Challenge 3: Entrances already have 2x higher base priority (20 vs ~10)
                score += base_priority * 5
                
                # Factor 4: Teammate coverage (avoid clustering)
                teammates = [i for i in self.getTeam(gameState) if i != self.index]
                if teammates:
                    teammate_pos = gameState.getAgentPosition(teammates[0])
                    if teammate_pos:
                        teammate_dist = self.getMazeDistance(position, teammate_pos)
                        if teammate_dist < 5:
                            score -= 50  # Strong penalty for being too close
                
                # Factor 5: Check if food at this cluster was recently eaten
                if zone_type == 'food_cluster':
                    if self.food_recently_lost_near(position, gameState):
                        score += 30  # Boost priority for areas under attack
                
                if score > best_score:
                    best_score = score
                    best_zone = position
            
            self.patrol_target = best_zone
        
        return self.patrol_target
    
    def food_recently_lost_near(self, position, gameState, radius=5):
        """
        Check if food was recently eaten near a position.
        Used to boost patrol priority in threatened areas.
        
        Args:
            position (tuple): Position to check
            gameState: Current game state
            radius (int): Distance threshold
        
        Returns:
            bool: True if food was lost nearby
        """
        last_eaten = self.get_last_eaten_food(gameState)
        if last_eaten:
            dist = self.getMazeDistance(position, last_eaten)
            return dist <= radius
        return False
    
    def get_last_eaten_food(self, gameState):
        """
        Checks if our food was eaten since the last turn.
        
        Real-time Update: When significant food loss detected (>2 food),
        triggers zone recalculation to adapt to new food distribution.
        
        Args:
            gameState: Current game state
        
        Returns:
            tuple: Position of eaten food, or None
        """
        history_key = f"food_defending_{self.index}"
        current_food = self.getFoodYouAreDefending(gameState).asList()
        
        last_food = BaseAgent.BLACKBOARD.get(history_key)
        
        if last_food and len(last_food) > len(current_food):
            eaten_food = list(set(last_food) - set(current_food))
            BaseAgent.BLACKBOARD[history_key] = current_food
            
            if eaten_food:
                # REAL-TIME UPDATE: Recalculate zones if major food loss
                # This ensures patrol adapts to changing food distribution
                if len(eaten_food) > 2:
                    self.recalculate_patrol_zones(gameState)
                return eaten_food[0]
        
        BaseAgent.BLACKBOARD[history_key] = current_food
        return None
    
    def recalculate_patrol_zones(self, gameState):
        """
        Dynamically update patrol zones as food distribution changes.
        
        Real-time Adaptation: When food is eaten (enemy dies, respawns with food),
        the food distribution changes. This method recalculates clusters to focus
        defense on remaining high-value areas.
        
        Process:
        1. Keep entrance zones (always important)
        2. Recalculate food clusters with remaining food
        3. Get new top 3 clusters
        4. Rebuild patrol zones
        
        This ensures the defender adapts to:
        - Enemy deaths (food respawns in new locations)
        - Progressive food consumption
        - Changing strategic importance of areas
        
        Args:
            gameState: Current game state
        """
        # Keep entrance zones (always important)
        entrance_zones = [(t, p, pr) for t, p, pr in self.patrol_zones 
                         if t == 'entrance']
        
        # Recalculate food clusters with remaining food
        food_defending = self.getFoodYouAreDefending(gameState).asList()
        food_clusters = self.cluster_food_positions(food_defending, gameState, 
                                                   cluster_radius=5)
        
        # Get top 3 clusters (Challenge 1: Limit coverage)
        top_clusters = food_clusters[:3] if len(food_clusters) >= 3 else food_clusters
        
        # Rebuild patrol zones
        new_zones = entrance_zones  # Start with entrance zones
        
        for cluster in top_clusters:
            center = self.get_cluster_center(cluster, gameState)
            priority = len(cluster) * 3
            new_zones.append(('food_cluster', center, priority))
        
        # Update patrol zones
        self.patrol_zones = new_zones
        
        # Update visit history for new zones
        current_turn = BaseAgent.BLACKBOARD.get('turn_count', 0)
        for zone_type, pos, priority in self.patrol_zones:
            if pos not in self.last_visited:
                self.last_visited[pos] = current_turn - 50  # Mark as moderately old