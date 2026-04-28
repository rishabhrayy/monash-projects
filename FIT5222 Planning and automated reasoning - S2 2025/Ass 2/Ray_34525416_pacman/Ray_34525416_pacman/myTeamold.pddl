; Pacman Domain for FIT5222 - Enhanced for Advanced Strategy
(define (domain pacman-challenge)
    (:requirements :strips :typing)

    (:types 
        agent
        enemy - agent
        team - agent
        ally - team
        current_agent - team
    )

    (:predicates 
        ; --- World State Predicates ---
        (food_available)
        (power-capsule-available)
        (territory_secure) ; True if no enemies are currently Pac-Man

        ; --- Agent State Predicates ---
        (is_pacman ?a - agent)
        (is_scared ?a - agent)
        (at_home ?a - team)
        (food_in_backpack ?a - team)
        (carrying-significant-food ?a - team) ; Carrying more than a threshold

        ; --- Relational Predicates ---
        (enemy_near ?e - enemy ?t - team)
        (teammate_attacking ?t - ally)
        (teammate_defending ?t - ally)
        (teammate-being-chased ?t - ally)
    )

    ; --- High-Level Strategic Actions ---

    (:action aggressive-attack
        :parameters (?a - current_agent)
        :precondition (and 
            (food_available)
            (territory_secure)
        )
        :effect (and 
            (not (food_available)) ; Goal is to eat all food
        )
    )

    (:action secure-power-capsule
        :parameters (?a - current_agent)
        :precondition (and
            (power-capsule-available)
            (at_home ?a)
        )
        :effect (and
            (not (power-capsule-available))
        )
    )

    (:action strategic-retreat
        :parameters (?a - current_agent)
        :precondition (and 
            (is_pacman ?a)
            (carrying-significant-food ?a)
        )
        :effect (and 
            (at_home ?a)
            (not (is_pacman ?a))
            (not (food_in_backpack ?a))
        )
    )

    (:action intercept-invader
        :parameters (?a - current_agent ?e - enemy)
        :precondition (and
            (at_home ?a)
            (is_pacman ?e)
        )
        :effect (and
            (not (is_pacman ?e))
        )
    )
    
    (:action cooperative-intercept
        :parameters (?a - current_agent ?t - ally ?e - enemy)
        :precondition (and
            (at_home ?a)
            (at_home ?t)
            (is_pacman ?e)
            (teammate_defending ?t) ; Teammate is also defending
        )
        :effect (and
            (not (is_pacman ?e))
        )
    )

    (:action patrol-chokepoints
        :parameters (?a - current_agent)
        :precondition (and 
            (at_home ?a)
            (territory_secure)
        )
        :effect (and 
            ; This is a continuous goal, so the effect is maintaining the precondition
            (territory_secure)
        )
    )
)