# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import random
import time
import os
import util
from captureAgents import CaptureAgent
from game import Directions, Actions
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first='OffensiveAgent', second='DefensiveAgent'):
    """
    This function should return a list of two agents that will form the
    team, initialized using firstIndex and secondIndex as their agent
    index numbers.
    """
    return [eval(first)(firstIndex), eval(second)(secondIndex)]

# --------------------------------------------------------------------------------------
# PARTICLE FILTER CLASS FOR ENEMY TRACKING
# --------------------------------------------------------------------------------------

class ParticleFilter:
    """
    A particle filter to track a single opponent agent.
    """
    def __init__(self, agent_index, num_particles, legal_positions):
        self.agent_index = agent_index
        self.num_particles = num_particles
        self.legal_positions = legal_positions
        self.particles = None
        self.initialize_particles()

    def initialize_particles(self):
        """Initializes particles uniformly across all legal positions."""
        self.particles = random.choices(self.legal_positions, k=self.num_particles)

    def observe(self, noisy_distance, gameState):
        """
        Update beliefs based on the noisy distance observation.
        This involves weighting and resampling particles.
        """
        if not self.particles: return
        
        my_pos = gameState.getAgentPosition(self.agent_index)
        weights = util.Counter()
        
        for p in self.particles:
            true_distance = util.manhattanDistance(my_pos, p)
            # The weight is the probability of observing the noisy distance given the particle's position
            weights[p] += gameState.getDistanceProb(true_distance, noisy_distance)
            
        if weights.totalCount() == 0:
            self.initialize_particles()
            return
            
        # Resample new particles based on the weights
        self.particles = random.choices(list(weights.keys()), weights=list(weights.values()), k=self.num_particles)

    def elapse_time(self, walls):
        """
        Predict the next state of the particles by simulating one step of random movement.
        """
        if not self.particles: return
        
        new_particles = []
        for p in self.particles:
            possible_positions = [p] + Actions.getLegalNeighbors(p, walls)
            new_particles.append(random.choice(possible_positions))
        self.particles = new_particles

    def get_belief_distribution(self):
        """Returns a Counter object representing the belief distribution over enemy positions."""
        belief = util.Counter()
        for p in self.particles:
            belief[p] += 1
        belief.normalize()
        return belief

# --------------------------------------------------------------------------------------
# BASE AGENT CLASS
# --------------------------------------------------------------------------------------

class BaseAgent(CaptureAgent):
    """
    A base agent that implements the core architecture:
    1. A* Search for low-level pathfinding.
    2. A Particle Filter for probabilistic enemy tracking.
    3. Rule-based goal selection for high-level strategy.
    """
    # Shared dictionary for team coordination
    BLACKBOARD = {}

    def registerInitialState(self, gameState):
        super().registerInitialState(gameState)
        
        # General agent setup
        self.start_position = gameState.getAgentPosition(self.index)
        self.legal_positions = [p for p in gameState.getWalls().asList(False) if p[1] > 1]
        
        # Enemy tracking setup
        self.num_particles = 500
        self.enemy_trackers = {}
        for opponent_index in self.getOpponents(gameState):
            self.enemy_trackers[opponent_index] = ParticleFilter(self.index, self.num_particles, self.legal_positions)
            
        # Team Coordination Setup
        if 'claimed_food' not in BaseAgent.BLACKBOARD:
            BaseAgent.BLACKBOARD['claimed_food'] = {}

    def chooseAction(self, gameState):
        """The main decision-making loop."""
        # --- 1. Update Beliefs ---
        self.update_enemy_beliefs(gameState)
        
        # --- 2. Choose High-Level Goal ---
        target_position = self.get_goal(gameState)

        # --- 3. Compute Low-Level Plan (A* Path) ---
        actions = self.get_low_level_plan_hs(gameState, target_position)
        
        # --- 4. Execute Move ---
        action = Directions.STOP
        if actions and len(actions) > 0:
            action = actions[0]
            
        # Update blackboard with current action/intent
        BaseAgent.BLACKBOARD[self.index] = {'action': action, 'target': target_position}
        
        return action

    def update_enemy_beliefs(self, gameState):
        """Update the particle filters for all opponents."""
        noisy_distances = gameState.getAgentDistances()
        for opponent_index in self.getOpponents(gameState):
            tracker = self.enemy_trackers[opponent_index]
            
            # If we can see the opponent, reset particles to their exact location
            opponent_pos = gameState.getAgentPosition(opponent_index)
            if opponent_pos:
                tracker.particles = [opponent_pos] * self.num_particles
            else:
                # Otherwise, predict and update based on noisy distance
                tracker.elapse_time(gameState.getWalls())
                tracker.observe(noisy_distances[opponent_index], gameState)
                
    def get_goal(self, gameState):
        """
        Placeholder for rule-based goal selection.
        This method MUST be overridden by subclasses.
        """
        util.raiseNotDefined()

    def get_low_level_plan_hs(self, gameState, goal_pos):
        """
        Computes a low-level plan using A* search with a risk-adjusted cost function.
        """
        if goal_pos is None:
            return [Directions.STOP]

        start_pos = gameState.getAgentPosition(self.index)
        
        # --- A* Search Implementation ---
        frontier = util.PriorityQueue()
        start_node = (start_pos, [], 0) # (position, path_so_far, cost_so_far)
        frontier.push(start_node, 0)
        
        visited = set()
        
        while not frontier.isEmpty():
            current_pos, path, current_cost = frontier.pop()
            
            if current_pos == goal_pos:
                return path # We found the goal

            if current_pos in visited:
                continue
                
            visited.add(current_pos)
            
            successors = Actions.getLegalNeighbors(current_pos, gameState.getWalls())
            for next_pos in successors:
                action = Actions.vectorToDirection( (next_pos[0]-current_pos[0], next_pos[1]-current_pos[1]) )
                new_path = path + [action]
                
                # --- Intelligent Cost Function ---
                # Base cost is 1, but add a heavy penalty for risk.
                risk_penalty = self.get_risk_penalty(next_pos, gameState)
                step_cost = 1 + risk_penalty
                
                new_cost = current_cost + step_cost
                
                # Heuristic: Maze distance to the goal
                heuristic = self.getMazeDistance(next_pos, goal_pos)
                
                priority = new_cost + heuristic
                frontier.push((next_pos, new_path, new_cost), priority)
                
        return [Directions.STOP] # Return Stop if no path is found

    def get_risk_penalty(self, position, gameState):
        """
        Calculates a risk penalty for a given position based on proximity to ghosts.
        """
        penalty = 0
        
        # Risk from visible ghosts
        for opponent_index in self.getOpponents(gameState):
            opponent = gameState.getAgentState(opponent_index)
            if not opponent.isPacman and opponent.getPosition() is not None:
                dist = self.getMazeDistance(position, opponent.getPosition())
                if opponent.scaredTimer < 5: # Only fear non-scared ghosts
                    if dist <= 1: penalty += 1000 # Very high risk
                    elif dist <= 3: penalty += 50  # Moderate risk
        
        # Risk from hidden ghosts (using the particle filter)
        for opponent_index in self.getOpponents(gameState):
            if gameState.getAgentPosition(opponent_index) is None: # If the opponent is hidden
                belief = self.enemy_trackers[opponent_index].get_belief_distribution()
                # Sum probabilities of the ghost being dangerously close
                for pos, prob in belief.items():
                    if self.getMazeDistance(position, pos) <= 2:
                        penalty += prob * 20 # Add risk proportional to belief
        return penalty

# --------------------------------------------------------------------------------------
# SPECIALIZED AGENT CLASSES
# --------------------------------------------------------------------------------------

class OffensiveAgent(BaseAgent):
    """
    An agent specialized in attacking and scoring.
    """
    def get_goal(self, gameState):
        """
        Implements the rule-based expert system for the offensive agent's goal selection.
        Prioritizes escaping over scoring.
        """
        my_state = gameState.getAgentState(self.index)
        my_pos = my_state.getPosition()
        food_list = self.getFood(gameState).asList()
        
        # --- Rule 1: ESCAPE (Highest Priority) ---
        is_threatened = self.get_risk_penalty(my_pos, gameState) > 20
        if my_state.isPacman and (my_state.numCarrying > 3 or is_threatened):
            # Find the safest entry point to our home territory
            home_positions = [p for p in self.legal_positions if p[0] == self.start_position[0]]
            if home_positions:
                safest_home_pos = min(home_positions, key=lambda p: self.get_risk_penalty(p, gameState))
                return safest_home_pos
                
        # --- Rule 2: GET CAPSULE (Opportunistic) ---
        capsules = self.getCapsules(gameState)
        if capsules:
            closest_capsule = min(capsules, key=lambda c: self.getMazeDistance(my_pos, c))
            if self.getMazeDistance(my_pos, closest_capsule) < 5:
                return closest_capsule

        # --- Rule 3: ATTACK FOOD (Default Behavior) ---
        if food_list:
            # --- Team Coordination ---
            # Exclude food claimed by our teammate
            claimed = BaseAgent.BLACKBOARD.get('claimed_food', {})
            unclaimed_food = [f for f in food_list if f not in claimed]
            
            if not unclaimed_food:
                unclaimed_food = food_list # If all food is claimed, ignore claims

            # Find the best food to target (balance distance and safety)
            best_food = min(unclaimed_food, key=lambda f: self.getMazeDistance(my_pos, f) + self.get_risk_penalty(f, gameState) * 5)
            
            # Claim this food on the blackboard
            BaseAgent.BLACKBOARD['claimed_food'][best_food] = self.index
            return best_food
            
        # --- Rule 4: RETURN HOME (If no food left) ---
        return self.start_position

class DefensiveAgent(BaseAgent):
    """
    An agent specialized in defending territory and intercepting invaders.
    """
    def get_goal(self, gameState):
        """
        Implements the rule-based expert system for the defensive agent's goal selection.
        Prioritizes intercepting invaders.
        """
        my_pos = gameState.getAgentPosition(self.index)
        invaders = [a for a in self.getOpponents(gameState) if gameState.getAgentState(a).isPacman]
        
        # --- Rule 1: INTERCEPT INVADERS (Highest Priority) ---
        
        if invaders:
            invader_positions = [p for i in invaders if (p := gameState.getAgentPosition(i)) is not None]
    
            if invader_positions:
                closest_invader_pos = min(invader_positions, key=lambda p: self.getMazeDistance(my_pos, p))
                return closest_invader_pos
            
        # --- Rule 2: GUARD LAST KNOWN THREAT ---
        # If food was just eaten, go to that location
        last_eaten_food = self.get_last_eaten_food(gameState)
        if last_eaten_food:
            return last_eaten_food

        # --- Rule 3: PATROL CHOKE POINTS (Default Behavior) ---
        # Patrol the middle of the home territory boundary
        mid_x = (gameState.data.layout.width // 2) - 1 if self.red else (gameState.data.layout.width // 2)
        patrol_points = [p for p in self.legal_positions if p[0] == mid_x]
        
        # Find the patrol point that is currently furthest from our other agent
        teammates = [i for i in self.getTeam(gameState) if i != self.index]
        if teammates:
            teammate_pos = gameState.getAgentPosition(teammates[0])
            if patrol_points and teammate_pos:
                return max(patrol_points, key=lambda p: self.getMazeDistance(p, teammate_pos))
        
        # If all else fails, go to the center of the border
        if patrol_points:
            return patrol_points[len(patrol_points) // 2]
            
        return self.start_position

    def get_last_eaten_food(self, gameState):
        """Checks if our food was eaten since the last turn."""
        history_key = f"food_defending_{self.index}"
        current_food = self.getFoodYouAreDefending(gameState).asList()
        
        last_food = BaseAgent.BLACKBOARD.get(history_key)
        
        if last_food and len(last_food) > len(current_food):
            eaten_food = list(set(last_food) - set(current_food))
            BaseAgent.BLACKBOARD[history_key] = current_food
            return eaten_food[0]
            
        BaseAgent.BLACKBOARD[history_key] = current_food
        return None