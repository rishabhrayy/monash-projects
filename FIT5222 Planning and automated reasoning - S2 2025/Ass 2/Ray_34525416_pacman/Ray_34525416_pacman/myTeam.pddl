; Pacman Domain for FIT5222 - Enhanced for Advanced Strategy
; Now fully integrated with Python implementation
(define (domain pacman-challenge)
    (:requirements :strips :typing :negative-preconditions)

    (:types 
        agent
        enemy - agent
        team - agent
        ally - team
        current_agent - team
        position
    )

    (:predicates 
        ; --- World State Predicates ---
        (food_available)
        (power_capsule_available)
        (territory_secure) ; True if no enemies are currently Pac-Man in our territory

        ; --- Agent State Predicates ---
        (is_pacman ?a - agent)
        (is_scared ?a - agent)
        (at_home ?a - team)
        (in_enemy_territory ?a - team)
        (food_in_backpack ?a - team)
        (carrying_significant_food ?a - team) ; Carrying >= 5 food items
        (being_chased ?a - team) ; Under immediate threat

        ; --- Relational Predicates ---
        (enemy_near ?e - enemy ?t - team) ; Enemy within 5 steps
        (enemy_is_pacman ?e - enemy) ; Enemy is in Pacman form
        (enemy_scared ?e - enemy) ; Enemy is scared from power capsule
        
        ; --- Team Coordination ---
        (teammate_attacking ?t - ally)
        (teammate_defending ?t - ally)
        (teammate_being_chased ?t - ally)
        
        ; --- Game Phase ---
        (early_game)
        (mid_game)
        (late_game)
    )

    ; --- High-Level Strategic Actions for OFFENSIVE Agent ---

    (:action aggressive-attack
        :parameters (?a - current_agent)
        :precondition (and 
            (food_available)
            (territory_secure)
            (not (being_chased ?a))
            (at_home ?a)
        )
        :effect (and 
            (in_enemy_territory ?a)
            (is_pacman ?a)
            ; Agent will attempt to collect food
        )
    )

    (:action cautious-attack
        :parameters (?a - current_agent)
        :precondition (and 
            (food_available)
            (at_home ?a)
            ; Can attack even when not fully secure, but more carefully
        )
        :effect (and 
            (in_enemy_territory ?a)
            (is_pacman ?a)
        )
    )

    (:action secure-power-capsule
        :parameters (?a - current_agent)
        :precondition (and
            (power_capsule_available)
            (in_enemy_territory ?a)
        )
        :effect (and
            (not (power_capsule_available))
            ; Enemies become scared (handled in game engine)
        )
    )

    (:action strategic-retreat
        :parameters (?a - current_agent)
        :precondition (and 
            (is_pacman ?a)
            (carrying_significant_food ?a)
        )
        :effect (and 
            (at_home ?a)
            (not (is_pacman ?a))
            (not (food_in_backpack ?a))
            (not (carrying_significant_food ?a))
            ; Food is scored
        )
    )
    
    (:action emergency-retreat
        :parameters (?a - current_agent)
        :precondition (and 
            (is_pacman ?a)
            (being_chased ?a)
            (food_in_backpack ?a)
        )
        :effect (and 
            (at_home ?a)
            (not (is_pacman ?a))
            (not (food_in_backpack ?a))
            (not (carrying_significant_food ?a))
            (not (being_chased ?a))
        )
    )

    ; --- High-Level Strategic Actions for DEFENSIVE Agent ---

    (:action intercept-invader
        :parameters (?a - current_agent ?e - enemy)
        :precondition (and
            (at_home ?a)
            (enemy_is_pacman ?e)
            (not (is_scared ?a))
        )
        :effect (and
            (not (enemy_is_pacman ?e))
            ; Enemy returns to ghost form if caught
        )
    )
    
    (:action cooperative-intercept
        :parameters (?a - current_agent ?t - ally ?e - enemy)
        :precondition (and
            (at_home ?a)
            (at_home ?t)
            (enemy_is_pacman ?e)
            (teammate_defending ?t)
            (not (is_scared ?a))
            (not (is_scared ?t))
        )
        :effect (and
            (not (enemy_is_pacman ?e))
            ; Coordinated defense - higher success rate
        )
    )

    (:action patrol-chokepoints
        :parameters (?a - current_agent)
        :precondition (and 
            (at_home ?a)
            (territory_secure)
            (not (is_pacman ?a))
        )
        :effect (and 
            ; Maintains territory security through presence
            (territory_secure)
        )
    )
    
    (:action active-defense
        :parameters (?a - current_agent)
        :precondition (and 
            (at_home ?a)
            (not (territory_secure))
            (not (is_pacman ?a))
        )
        :effect (and
            ; Actively hunt invaders
            ; Effect handled by intercept actions
        )
    )
    
    (:action chase-scared-enemy
        :parameters (?a - current_agent ?e - enemy)
        :precondition (and
            (is_pacman ?a)
            (enemy_scared ?e)
            (enemy_near ?e ?a)
        )
        :effect (and
            (not (enemy_scared ?e))
            ; Score bonus points for eating scared ghost
        )
    )

    ; --- Strategic Coordination Actions ---
    
    (:action coordinate-attack
        :parameters (?a - current_agent ?t - ally)
        :precondition (and
            (at_home ?a)
            (teammate_attacking ?t)
            (food_available)
            (not (being_chased ?t))
        )
        :effect (and
            (teammate_attacking ?a)
            (in_enemy_territory ?a)
            ; Both agents attack simultaneously
        )
    )
    
    (:action coordinate-defense
        :parameters (?a - current_agent ?t - ally)
        :precondition (and
            (at_home ?a)
            (teammate_defending ?t)
            (not (territory_secure))
        )
        :effect (and
            (teammate_defending ?a)
            ; Cover different areas of defense
        )
    )
    
    (:action cover-retreat
        :parameters (?a - current_agent ?t - ally)
        :precondition (and
            (at_home ?a)
            (teammate_being_chased ?t)
            (is_pacman ?t)
        )
        :effect (and
            (in_enemy_territory ?a)
            ; Distract enemies while teammate escapes
        )
    )

    ; --- Adaptive Strategy Actions ---
    
    (:action aggressive-endgame
        :parameters (?a - current_agent)
        :precondition (and
            (late_game)
            (food_available)
            ; Take more risks in endgame
        )
        :effect (and
            (in_enemy_territory ?a)
            (is_pacman ?a)
        )
    )
    
    (:action conservative-lead
        :parameters (?a - current_agent)
        :precondition (and
            (late_game)
            (at_home ?a)
            ; Play defensively when ahead
        )
        :effect (and
            (teammate_defending ?a)
            (territory_secure)
        )
    )
)